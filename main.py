import redis

redis_host = 'localhost'
redis_port=6379

# r.set('name','priyanjali')
# value = r.get('name')
# print(value)

def redis_string():
    try:
        r = redis.StrictRedis(
            host = redis_host, port = redis_port, decode_responses = True)
        r.set("name","Priyanjali")
        n = r.get("name")
        print(n)

    except Exception as e:
        print(e)

def redis_integer():
    try:
        r = redis.StrictRedis(
            host = redis_host, port = redis_port, decode_responses = True
        )
        r.set("number","1000")
        real = r.get("number")
        r.incr("number")
        inc = r.get("number")
        print(real)
        print(inc)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    redis_string()
    redis_integer()