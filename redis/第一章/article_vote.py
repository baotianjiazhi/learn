import time
import redis

ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432
ARTICLES_PER_PAGE = 25


# 文章投票功能
def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS  # 七天前的时间
    if conn.zscore("time:", article) < cutoff:
        '''
            zscore返回有序集 key 中，成员member的score 值
            比较文章的时间和七天前的时间如果小于则失效
        '''
        return

    article_id = article.partition(":")[-1]
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', VOTE_SCORE, article)    # 书中这两个写反了，应该是加分是amount，文章是value
        conn.hincrby(article, 'votes', 1)


# 文章发布功能
def post_article(conn, user, title, link):
    article_id = str(conn.incr('article:'))  # 文章id自动加一

    voted = 'voted:' + article_id
    conn.sadd(voted, user)  # 把发布文章的用户添加到文章的投票用户里
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id
    print(type(article))
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })

    conn.zadd('score:', {article: now + VOTE_SCORE})    # 源码中要求传入的是map
    conn.zadd('time:', {article: now})

    return article_id


# 获取评分最高和最新发布的文章
def get_articles(conn, page, order='score:'):
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    '''返回有序集 key 中，指定区间内的成员。其中成员的位置按 score 值递减(从大到小)来排列'''
    ids = conn.zrevrange(order, start, end)
    articles = []
    for id in ids:
        article_data = conn.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)

    return articles


# 对文章进行分组
def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn, group, page, order='score:'):
    key = order + group
    if not conn.exists(key):
        conn.zinterstore(key,
                         ['group:' + group, order],
                         aggregate='max',
                         )
        conn.expire(key, 60)
    return get_articles(conn, page, key)