from flask import Flask

from config import Config

from routes.dashboard import dashboard_bp
from routes.dataset import dataset_bp
from routes.embedding import embedding_bp
from routes.schema import schema_bp
from routes.experiment import experiment_bp
from routes.prompt import prompt_bp
from routes.testing import testing_bp

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(dashboard_bp)

app.register_blueprint(dataset_bp)

app.secret_key = "text2sqlstudio"


app.register_blueprint(schema_bp)
app.register_blueprint(
    embedding_bp
)
app.register_blueprint(experiment_bp)

app.register_blueprint(
    prompt_bp
)

app.register_blueprint(testing_bp)

if __name__ == "__main__":

    print(app.url_map)
    app.run(

        debug=True,

        port=5000
    )
    
