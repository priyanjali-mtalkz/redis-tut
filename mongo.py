import redis
import pymongo
from flask import Flask,jsonify,request
import json
from bson.json_util import dumps
from datetime import timedelta
app = Flask(__name__)


# cache = Cache(config={"CACHE_TYPE":"RedisCache","CACHE_REDIS_PORT":6379})
# cache.init_app(app)
cache = redis.StrictRedis(host='localhost',port=6379,decode_responses = True)
client = pymongo.MongoClient("mongodb://localhost:27017")

db = client['Quiz']
coll = db['UserDetails']

# @app.route('/push')
# @cache.cached(timeout=50, key_prefix='all_comments')
# def pushData():
#     try:
#         print("20")
#         user_data = {
#             'mobile' : 9876543,
#             'score' : []
#         }
#         print("hello")
#         score = [10,20,30,40,50]
#         user_data['score'].append(score)
#         print(user_data)
#         print("1")
#         cache.set('user_data',json.dumps(user_data))
#         return json.loads(cache.get('user_data'))
#     except Exception as e:
#         print(e)
#     return jsonify({'Status':'Failed'})

@app.route('/')
# @cache.cached(timeout=50, key_prefix='all_comments')
def home():   
    try: 
        obj = dumps(coll.find())
        result = cache.set('user_data',obj)
        li = json.loads(cache.get('user_data'))
        return jsonify(li)
    except Exception as e:
        print("----ERROR-----",e)
    return jsonify()

@app.route('/add/data',methods = ['POST'])
def addData():
    if request.method == 'POST':
        args = request.args
        mobile_no = str(args.get('mobile'))
        query = request.get_json()
    cache.set(mobile_no,dumps(query))
    cache.expire(mobile_no,timedelta(seconds = 60))
    #coll.insert_one(query)
    return jsonify({"Status":"Insertion successful"})


@app.route('/get/score')
def getscore():
    try:
        args = request.args
        user = str(args.get('mobile'))
        sc = cache.get(user) 
        if sc is None:
            print('Could not find in cache getting data from mongodb')
            obj = dumps(coll.find({'Mobile':user}))
            print('!!!!!!!!!!!!!!!!' ,user)
            cache.set(user,obj)
            cache.expire(user,timedelta(seconds = 60))
            sc = {'Message':'Could not find in cache getting data from mongodb',user : json.loads(cache.get(user))}
            return (sc)
        else:
            print('Found data in cache')
            if cache.exists(user):
                cache.expire(user,timedelta(seconds = 1))
            sc = {'Message':'Found data in cache',user : json.loads(sc)}
            return (sc)
    except Exception as e:
        print("----ERROR-----",e)
    return jsonify()
    

@app.route('/get/cache/data')
def data():  
    try:
        print("Getting data from cache")
        return json.loads(cache.get('user_data'))
    except Exception as e:
        print("----ERROR-----",e)
    return jsonify()

if __name__ == '__main__':
    app.run(debug = True)



