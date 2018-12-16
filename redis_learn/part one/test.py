import redis

if __name__ == '__main__':
    conn = redis.Redis(host='localhost', port=6379)
    conn.zadd("zset_name", {'a1': 6})