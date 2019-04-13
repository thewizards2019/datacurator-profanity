from flask import Flask
import requests

# create_app wraps the other functions to set up the project

def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)

    @app.route("/profanity")
    def profanity(self):
        content = "my message fuck" # make sure this is the actual tweet
        url = "https://www.purgomalum.com/service/containsprofanity?text={}".format(content)
        profanity = requests.get(url=url)
        return {"profanity": bool(profanity.content)}

        

    return app
