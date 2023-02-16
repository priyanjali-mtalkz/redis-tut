from flask import *
import requests
import redis


redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses = True)

app = Flask(__name__)
@app.route('/')
def home():
    r.set("note","Welcome")
    n = r.get("note")
    return n

@app.route("/universities")
def get_universities():
    API_URL = "http://universities.hipolabs.com/search?country="
    search = request.args.get('country')
    r = requests.get(f"{API_URL}{search}")
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(debug = True)