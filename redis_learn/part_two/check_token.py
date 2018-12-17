# 构建一个Fake Web Retailer网站的后台
import time
QUIT = False
LIMIT = 10000000


def check_token(conn, token):
    return conn.hget('login:', token)


def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hset('login:', token, user)    # 维持令牌与登陆用户之间的映射
    conn.zadd('recent:', token, timestamp)    # 记录令牌最后一次出现的时间
    if item:
        conn.zadd('viewd:' + token, item, timestamp)    # 记录浏览的商品
        conn.zremrangebyrank('viewed:' + token, 0, -26)    # 移除旧的记录，只保留用户最后浏览的25个商品


def clean_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')    # 找出目前已有令牌的数量
        if size <= LIMIT:
            time.sleep(1)
            continue
        end_index = min(size - LIMIT, 100)
        tokens = conn.zrange('recent:', 0, end_index-1)    # 获取需要移除的令牌ID

        session_keys = []
        for token in tokens:
            session_keys.append('viewed:' + token)    # 为被删除的令牌构建键名

        conn.delete(*session_keys)
        conn.hdel('login:', *tokens)
        conn.zrem('recent:', *tokens)
