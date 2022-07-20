create_tweets_table_sql = """CREATE TABLE IF NOT EXISTS tweets
 (tweet_id bigint NOT NULL PRIMARY KEY, created_at timestamp NOT NULL, text varchar NOT NULL, user_id bigint NOT NULL, user_screen_name varchar,
 user_description varchar, tweet_type varchar, reply_to_tweet_id bigint, reply_to_user_id bigint, retweet_to_tweet_id bigint, retweet_to_user_id bigint, hashtags varchar);
 """

create_hashtags_table_sql = """CREATE TABLE IF NOT EXISTS hashtags
 (id SERIAL PRIMARY KEY, tweet_id bigint NOT NULL, user_id bigint NOT NULL, hashtag_name varchar NOT NULL,
 CONSTRAINT tweet_user_hashtag UNIQUE(tweet_id,user_id,hashtag_name));
 """

create_users_table_sql = """CREATE TABLE IF NOT EXISTS users
 (user_id bigint NOT NULL PRIMARY KEY, screen_name varchar NULL, description varchar NULL,
 name varchar NULL, created_at timestamp NULL);
 """
