import threading
import unittest
import urllib.parse  # python3中将urlparse改名为urllib.parse
import uuid
from learn.redis_learn.part_two.check_token import *


def extract_item_id(request):
    parsed = urllib.parse.urlparse(request)
    query = urllib.parse.parse_qs(parsed.query)
    return (query.get('item') or [None])[0]


def is_dynamic(request):
    parsed = urllib.parse.urlparse(request)
    query = urllib.parse.parse_qs(parsed.query)
    return '_' in query


def hash_request(request):
    return str(hash(request))


class Inventory(object):
    def __init__(self, id):
        self.id = id

    @classmethod
    def get(cls, id):
        return Inventory(id)

    def to_dict(self):
        return {'id': self.id, 'data': 'data to cache...', 'cached': time.time()}


class TestCh02(unittest.TestCase):
    def setUp(self):
        import redis
        self.conn = redis.Redis(db=15)

    def tearDown(self):
        conn = self.conn
        to_del = (
                conn.keys('login:*') + conn.keys('recent:*') + conn.keys('viewed:*') +
                conn.keys('cart:*') + conn.keys('cache:*') + conn.keys('delay:*') +
                conn.keys('schedule:*') + conn.keys('inv:*'))
        if to_del:
            self.conn.delete(*to_del)
        del self.conn
        global QUIT, LIMIT
        QUIT = False
        LIMIT = 10000000
        print('\n')
        print('\n')

    def test_login_cookies(self):
        conn = self.conn
        global LIMIT, QUIT
        token = str(uuid.uuid4())

        update_token(conn, token, 'username', 'itemX')
        print("We just logged-in/updated token:", token)

        print("For user:", 'username')
        print('\n')

        print("What username do we get when we look-up that token?")
        r = check_token(conn, token)
        print(r)
        print(self.assertTrue(r))

        print("Let's drop the maximum number of cookies to 0 to clean them out")
        print("We will start a thread to do the cleaning, while we stop it later")

        LIMIT = 0
        t = threading.Thread(target=clean_sessions, args=(conn,))
        t.setDaemon(True)  # to make sure it dies if we ctrl+C quit
        t.start()
        time.sleep(1)
        QUIT = True
        time.sleep(2)
        if t.isAlive():
            raise Exception("The clean sessions thread is still alive?!?")

        s = conn.hlen('login:')
        print("The current number of sessions still available is:", s)
        self.assertFalse(s)

    def test_shoppping_cart_cookies(self):
        conn = self.conn
        global LIMIT, QUIT
        token = str(uuid.uuid4())

        print("We'll refresh our session...")
        update_token(conn, token, 'username', 'itemX')
        print("And add an item to the shopping cart")
        add_to_cart(conn, token, "itemY", 3)
        r = conn.hgetall('cart:' + token)
        print("Our shopping cart currently has:", r)
        print("\n")
        self.assertTrue(len(r) >= 1)
        print("\n")
        "Let's clean out our sessions and carts"
        LIMIT = 0
        t = threading.Thread(target=clean_full_sessions, args=(conn,))
        t.setDaemon(1)  # to make sure it dies if we ctrl+C quit
        t.start()
        time.sleep(1)
        QUIT = True
        time.sleep(2)
        if t.isAlive():
            raise Exception("The clean sessions thread is still alive?!?")

        r = conn.hgetall('cart:' + token)
        print("Our shopping cart now contains:", r)

        self.assertFalse(r)

    def test_cache_request(self):
        conn = self.conn
        token = str(uuid.uuid4())

        def callback(request):
            return "content for " + request

        update_token(conn, token, 'username', 'itemX')
        url = 'http://test.com/?item=itemX'
        print("We are going to cache a simple request against", url)

        result = cache_request(conn, url, callback)
        print("We got initial content:", repr(result))

        print('\n')

        self.assertTrue(result)

        print("To test that we've cached the request, we'll pass a bad callback")

        result2 = cache_request(conn, url, None)
        result2 = result2.decode()
        print("We ended up getting the same response!", repr(result2))

        self.assertEqual(result, result2)

        self.assertFalse(can_cache(conn, 'http://test.com/'))
        self.assertFalse(can_cache(conn, 'http://test.com/?item=itemX&_=1234536'))

    def test_cache_rows(self):
        import pprint
        conn = self.conn
        global QUIT

        print("First, let's schedule caching of itemX every 5 seconds")

        schedule_row_cache(conn, 'itemX', 5)
        print("Our schedule looks like:")
        s = conn.zrange('schedule:', 0, -1, withscores=True)
        pprint.pprint(s)
        self.assertTrue(s)
        print("We'll start a caching thread that will cache the data...")
        t = threading.Thread(target=cache_rows, args=(conn,))
        t.setDaemon(1)
        t.start()

        time.sleep(1)
        print("Our cached data looks like:")

        r = conn.get('inv:itemX')
        print(r)
        repr(r)
        self.assertTrue(r)
        print('\n')
        print("We'll check again in 5 seconds...")

        time.sleep(5)
        print("Notice that the data has changed...")
        r2 = conn.get('inv:itemX')
        print('\n')
        repr(r2)
        print('\n')
        self.assertTrue(r2)
        self.assertTrue(r != r2)

        print("Let's force un-caching")

        schedule_row_cache(conn, 'itemX', -1)
        time.sleep(1)
        r = conn.get('inv:itemX')
        print("The cache was cleared?", not r)
        print(self.assertFalse(r))

        QUIT = True
        time.sleep(2)
        if t.isAlive():
            raise Exception("The database caching thread is still alive?!?")

    # We aren't going to bother with the top 10k requests are cached, as
    # we already tested it as part of the cached requests test.


if __name__ == '__main__':
    unittest.main()
