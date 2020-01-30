from flask import Flask, json
import logging

def log_exception(sender, exception, **extra):
    sender.logger.debug('Got exception during processing: %s', exception)


def create_app(config_file):
    #Instantiating Flask and appling config
    app = Flask(__name__)
    app.config.from_object(config_file)

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    #Or db = SQLAlchemy(app) then use this db ref in model definition
    from model import db
    db.init_app(app)

    @app.route('/')
    def index():
        pass

    @app.route('/isAlive')
    def is_alive():
        res = app.response_class(
            response=json.dumps('Case Service API is healthy'),
            mimetype='application/json'
        )
        
        return res

    return app

if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True, host='0.0.0.0', port='8000')