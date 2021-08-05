from flask import Flask

from api.login import login_api
from api.team_api import team_api
from api.member_api import member_api
from api.submit_api import submit_api
from api.balloon_api import balloon_api
from api.contest_api import contest_api
from api.management_api import management_api
import util
from datetime import timedelta
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "renyizifuchuan"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.register_blueprint(login_api)
app.register_blueprint(team_api)
app.register_blueprint(member_api)
app.register_blueprint(submit_api)
app.register_blueprint(balloon_api)
app.register_blueprint(contest_api)
app.register_blueprint(management_api)




@app.route('/')
def hello_world():
    return 'Hello World!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2017, debug=True)
