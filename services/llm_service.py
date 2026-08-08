import time
import requests

from config import Config


# ==========================================================
# OPENROUTER URL
# ==========================================================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ==========================================================
# HEADERS
# ==========================================================

def get_headers():

    return {

        "Authorization":
            f"Bearer {Config.OPENROUTER_API_KEY}",

        "Content-Type":
            "application/json",

        "HTTP-Referer":
            "http://localhost",

        "X-Title":
            "Text2SQL Studio"

    }


# ==========================================================
# BUILD PAYLOAD
# ==========================================================

def build_payload(

    prompt,

    model,

    temperature=0,

    max_token=2048

):

    return {

        "model": model,

        "messages": [

            {

                "role": "user",

                "content": prompt

            }

        ],

        "temperature": temperature,

        "max_tokens": max_token

    }


# ==========================================================
# CALL OPENROUTER
# ==========================================================

def call_openrouter(payload):

    start = time.time()

    response = requests.post(
        OPENROUTER_URL,
        headers=get_headers(),
        json=payload,
        timeout=300
    )

    latency = round(time.time() - start, 3)

    

    

    response.raise_for_status()

    return response.json(), latency

# ==========================================================
# PARSE RESPONSE
# ==========================================================

def parse_response(

    response,

    latency

):

    sql = ""

    usage = response.get(

        "usage",

        {}

    )

    if response.get("choices"):

        sql = (

            response["choices"][0]

            ["message"]

            ["content"]

            .strip()

        )

    return {

        "sql": clean_sql(sql),

        "prompt_tokens":

            usage.get(

                "prompt_tokens",

                0

            ),

        "completion_tokens":

            usage.get(

                "completion_tokens",

                0

            ),

        "total_tokens":

            usage.get(

                "total_tokens",

                0

            ),

        "latency":

            latency,

        "raw":

            response

    }


# ==========================================================
# GENERATE SQL
# ==========================================================

def generate_sql(

    prompt,

    model,

    temperature=0,

    max_token=2048

):

    payload = build_payload(

        prompt,

        model,

        temperature,

        max_token

    )

    response, latency = call_openrouter(

        payload

    )

    return parse_response(

        response,

        latency

    )
    
import re

def clean_sql(sql: str):

    sql = sql.strip()

    sql = re.sub(
        r"^```sql\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r"^```",
        "",
        sql
    )

    sql = re.sub(
        r"```$",
        "",
        sql
    )

    return sql.strip()