from datetime import date
import redis
import re
import prize.log as log

class Worker:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host, port=port)

    def _generate_key(self):
        return "prize:%s" % (date.today().isoformat())

    def _store_user_id(self, user_id):
        key     = self._generate_key()
        user_id = str(user_id)

        if not self.redis.sismember(key, user_id):
            self.redis.sadd(key, user_id)

        log.log("%s << %s" % (key, user_id))

    def perform(self, tweet, tracking, following):
        if tweet.has_key('user'):
            is_followed = any(u == tweet['user']['id'] for u in following)
            
            if tweet['retweeted'] and is_followed:
                tracking = map(lambda u: ".*%s.*" % u , tracking)

                if not re.match("|".join(tracking), tweet['text']):
                    return
            
            try:
                self._store_user_id(tweet['user']['id'])
            except:
                log.error('Could not store in redis')
