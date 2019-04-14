from flask import Flask
import requests
import json
from confluent_kafka import Consumer
from confluent_kafka import Producer

# create_app wraps the other functions to set up the project


def create_app(config=None, testing=False, cli=True):
    """
    Application factory, used to create application
    """
    app = Flask(__name__, static_folder=None)
    app.port = 5003

    # @app.route("/profanity")
    # def profanity(self):
    #     content = "my message fuck" # make sure this is the actual tweet
    #     url = "https://www.purgomalum.com/service/containsprofanity?text={}".format(content)
    #     profanity = requests.get(url=url)
    #     return {"profanity": profanity.content.decode('UTF8')}

    c = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "content_curator_twitter_group_21",
            "auto.offset.reset": "earliest",
        }
    )

    p = Producer({"bootstrap.servers": "localhost:9092"})

    c.subscribe(["content_curator_twitter"])

    while True:
        msg = c.poll()

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        # print('Received message: {}'.format(msg.value().decode('utf-8')))
        try:
            m = json.loads(msg.value().decode("utf-8"))
            if "content" in m.keys():
                content = m["content"]
                url = "https://www.purgomalum.com/service/containsprofanity?text={}".format(
                    content
                )
                profanity = requests.get(url=url)
                profanity_value = json.dumps(
                    {"profanity": profanity.content.decode("utf-8")}
                )
                msg_key = msg.key().decode("utf-8")

                if msg_key is not None:
                    p.produce(
                        topic="content_curator_twitter",
                        key=msg_key,
                        value=profanity_value,
                    )
                    p.flush()
                    print("ADDED:", {"key": msg_key, "value": profanity_value})
        except Exception as e:
            print("ERROR:", e)

    c.close()

    return app
