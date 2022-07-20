insert_tweets_table_sql = """INSERT INTO tweets
 (tweet_id, created_at, text, user_id, user_screen_name, user_description, tweet_type, reply_to_tweet_id, reply_to_user_id, retweet_to_tweet_id, retweet_to_user_id, hashtags) 
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
"""

insert_hashtags_table_sql = """INSERT INTO hashtags
 (tweet_id, user_id, hashtag_name) 
 VALUES (%s, %s, %s)
 ON CONFLICT DO NOTHING;
"""

insert_users_table_sql = """INSERT INTO users
 (user_id, screen_name, description, name, created_at) 
 VALUES (%s, %s, %s, %s, %s)
 ON CONFLICT DO NOTHING;
"""
