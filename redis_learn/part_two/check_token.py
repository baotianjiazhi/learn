# 构建一个Fake Web Retailer网站的后台
import json
import time

from learn.redis_learn.part_two.unitest import Inventory, extract_item_id, is_dynamic, hash_request

QUIT = False
LIMIT = 10000000


def check_token(conn, token):
    return conn.hget('login:', token)


def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hset('login:', token, user)    # 维持令牌与登陆用户之间的映射
    conn.zadd('recent:', {token: timestamp})    # 记录令牌最后一次出现的时间
    if item:
        conn.zadd('viewd:' + token, {item: timestamp})    # 记录浏览的商品
        conn.zremrangebyrank('viewed:' + token, 0, -26)    # 移除旧的记录，只保留用户最后浏览的25个商品
        conn.zincrby('viewed:', -1, item)

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


def add_to_cart(conn, session, item, count):
    if count <= 0:
        conn.hrem('cart:' + session, item)
    else:
        conn.hset('cart:' + session, item, count)


def clean_full_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue
        end_index = min(size - LIMIT, 100)
        sessions = conn.zrange('recent:', 0, end_index - 1)

        sessions_key = []
        for sess in sessions:
            sessions_key.append('viewed:' + sess)
            sessions_key.append('cart:' + sess)

        conn.delete(*sessions_key)
        conn.hdel('login:', *sessions)
        conn.zrem('recent:', *sessions)


# 缓存函数
def cache_request(conn, request, callback):
    if not can_cache(conn, request):
        return callback(request)

    page_key = 'cache:' + hash_request(request)
    content = conn.get(page_key)

    if not content:
        content = callback(request)
        conn.setex(page_key, 300, content)

    return content


def schedule_row_cache(conn, row_id, delay):
    conn.zadd('delay:', {row_id: delay})
    conn.zadd('schedule:', {row_id: time.time()})


def cache_rows(conn):
    while not QUIT:
        # 尝试获取下一个需要被缓存的数据行以及该行的调度时间戳，返回一个包含零个或一个元祖的列表
        next = conn.zrange('schedule:', 0, 0, withscores=True)
        now = time.time()
        if not next or next[0][1] > now:
            time.sleep(.05)
            continue

        row_id = next[0][0]
        delay = conn.zscore('delay:', row_id)
        if delay <= 0:
            conn.zrem('delay:', row_id)
            conn.zrem('schedule:', row_id)
            conn.delete('inv:' + row_id)
            continue

        row = Inventory.get(row_id)
        conn.zadd('schedule:', {row_id: now + delay})
        conn.set('inv:' + str(row_id), json.dumps(str(row.to_dict())))


def rescale_viewed(conn):
    while not QUIT:
        # 删除所有排名在20000名之后的商品
        conn.zremrangebyrank('viewed:', 0, -20001)
        conn.zinterstore('viewed:', {'viewed:': .5})    # 将浏览次数降低为原来的一半
        time.sleep(300)    # 五分钟之后再执行操作


def can_cache(conn, request):
    item_id = extract_item_id(request)    # 尝试从页面里面取出商品id
    if not item_id or is_dynamic(request):
        return False
    rank = conn.zrank('viewed:', item_id)
    return rank is not None and rank < 10000