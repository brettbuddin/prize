# Prize

Uses Twitter's streaming API to listen for specific keywords for a contest. It also tracks retweets of a specified user's tweets that contain those same search terms. This allows users to enter the contest by tweeting with, say, a hashtag and or by retweeting the originating organization's tweets containing said hashtag.

User IDs are accumulated in Redis by date. The key used for each Redis Set looks like: `prize:2012-03-25`

    $ prize --config=~/path/to/file.config
  
    [debug]: Tracking keywords ['superawesomecontest']
    [debug]: Following user ['271196899']
