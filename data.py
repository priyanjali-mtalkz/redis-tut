from flask import *
import requests
import redis
import json

app = Flask(__name__)

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses = True)

@app.route('/')
def get_data():
    try:
        score = [10,20,30,40,50]
        #r.lpush("user",*score)
        return(r.lrange("user",0, -1))
        # return jsonify({'Status':'Success'})
    except Exception as e:
        print(e)
    return jsonify({'Status':'Success'})
@app.route('/nest')
def getData():
    try:
        user_data = {
            'mobile' : 9876543,
            'score' : [10,20,30,25,32]
        }
        r.set('user_data',json.dumps(user_data))
        return json.loads(r.get('user_data'))

    except Exception as e:
        print(e)
    return jsonify({'Status':'Success'})

@app.route('/push')
def pushData():
    try:
        print("20")
        user_data = {
            'mobile' : 9876543,
            'score' : []
        }
        print("hello")
        score = [10,20,30,40,50]
        # obj = json.dumps(user_data)
        # #print(obj)
        # r.lpush("score",*score)
        # json.loads(obj)
        user_data['score'].append(score)
        print(user_data)
        print("1")
        r.set('user_data',json.dumps(user_data))
        return json.loads(r.get('user_data'))


    except Exception as e:
        print(e)
    return jsonify({'Status':'Success'})


if __name__ == '__main__':
    app.run(debug = True)