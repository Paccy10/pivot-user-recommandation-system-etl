import os
import psycopg2
import unicodedata
import json
from dotenv import load_dotenv

from sql.insert import (
    insert_users_table_sql,
    insert_hashtags_table_sql,
    insert_tweets_table_sql,
)

load_dotenv()

allowed_languages = ["ar", "en", "fr", "in", "pt", "es", "tr", "ja"]
seen_tweet_ids = []
seen_user_ids = []
seen_hashtag_records = []


def get_excluded_hashtags():
    """Read hashtags data file line by line, decode the texts, push it into an array and return it"""

    excluded_hashtags = []
    file = open("hashtags.data.txt", "r")
    lines = file.readlines()
    for line in lines:
        tag = unicodedata.normalize("NFKD", "{0}".format(line.strip())).encode(
            "ascii", "ignore"
        )
        # Remove empty strings
        if tag.decode():
            excluded_hashtags.append(tag.decode())

    return excluded_hashtags


def get_tweet_hashtags(cur, hashtags, tweet_id, user_id):
    """Get tweet hashtags, check if they are not in excluded hashtags, save it into database and return array of tweet hashtags"""

    tags = []
    excluded_hashtags = get_excluded_hashtags()
    for tag in hashtags:
        if "{0}".format(tag["text"]) not in excluded_hashtags:
            tags.append("{0}".format(tag["text"]))
            ht = {
                "tweet_id": tweet_id,
                "user_id": user_id,
                "hashtag_name": "{0}".format(tag["text"]),
            }
            if ht not in seen_hashtag_records:
                seen_hashtag_records.append(ht)
                hashtag_table_values = [tweet_id, user_id, "{0}".format(tag["text"])]

                cur.execute(insert_hashtags_table_sql, hashtag_table_values)

    return tags


def save_users(cur, json_tweet, transformed_values):
    """Save users into the database"""

    user = json_tweet["user"]
    retweeted_status = json_tweet.get("retweeted_status")
    user_id = user.get("id")
    reply_to_user_id = transformed_values[8]

    # Save user if the user id does not exist in seen_user_ids
    if user_id not in seen_user_ids:
        seen_user_ids.append(user_id)
        screen_name = user.get("screen_name")
        description = user.get("description")
        name = user.get("name")
        user_created_at = user.get("created_at")

        user_values = [
            user_id,
            screen_name,
            "{0}".format(description) if description else None,
            name,
            user_created_at,
        ]

        cur.execute(insert_users_table_sql, user_values)

    # Save user if the reply_to_user_id does not exist in seen_user_ids
    if reply_to_user_id and reply_to_user_id not in seen_user_ids:
        seen_user_ids.append(reply_to_user_id)
        in_reply_to_screen_name = json_tweet.get("in_reply_to_screen_name")

        user_values = [reply_to_user_id, in_reply_to_screen_name, None, None, None]

        cur.execute(insert_users_table_sql, user_values)

    # Save user if there is a retweet status and retweeet_to_user_id does not exist in seen_user_ids
    if retweeted_status:
        retweeet_to_user_id = retweeted_status["user"].get("id")

        if retweeet_to_user_id not in seen_user_ids:
            seen_user_ids.append(retweeet_to_user_id)
            screen_name = retweeted_status["user"].get("screen_name")
            description = retweeted_status["user"].get("description")
            name = retweeted_status["user"].get("name")
            user_created_at = retweeted_status["user"].get("created_at")
            user_values = [
                retweeet_to_user_id,
                screen_name,
                "{0}".format(description) if description else None,
                name,
                user_created_at,
            ]

            cur.execute(insert_users_table_sql, user_values)


def process_tweets_file(cur):
    with open("tweets.data.txt", "r") as file:
        for i, line in enumerate(file):
            try:
                tweet = json.loads(line)

                # Get values from tweet json object
                id = tweet.get("id")
                id_str = tweet.get("id_str")
                created_at = tweet.get("created_at")
                text = tweet.get("text")
                hashtags = tweet["entities"].get("hashtags")
                user = tweet["user"]
                user_id = user.get("id")
                user_id_str = user.get("id_str")
                user_screen_name = user.get("screen_name")
                user_description = user.get("description")
                retweeted_status = tweet.get("retweeted_status")
                in_reply_to_user_id = tweet.get("in_reply_to_user_id")
                in_reply_to_screen_name = tweet.get("in_reply_to_screen_name")
                in_reply_to_status_id = tweet.get("in_reply_to_status_id")
                lang = tweet.get("lang")

                # Skip malformed tweets
                if (
                    not id
                    or not id_str
                    or not created_at
                    or not text
                    or not hashtags
                    or not user_id
                    or not user_id_str
                    or id in seen_tweet_ids
                    or lang not in allowed_languages
                    or (hashtags and len(hashtags) == 0)
                ):
                    continue

                else:
                    seen_tweet_ids.append(id)

                    reply_to_tweet_id = None
                    reply_to_user_id = None
                    tweet_type = None
                    retweet_to_tweet_id = None
                    retweet_to_user_id = None

                    # Check if a tweet is a reply
                    if in_reply_to_user_id and in_reply_to_status_id:
                        tweet_type = "reply"
                        reply_to_tweet_id = in_reply_to_status_id
                        reply_to_user_id = in_reply_to_user_id

                    # Check if a tweet is a retweet
                    if retweeted_status:
                        tweet_type = "retweet"
                        retweet_to_tweet_id = retweeted_status.get("id")
                        retweet_to_user_id = retweeted_status["user"].get("id")

                    text = "{0}".format(text)
                    user_description = (
                        "{0}".format(user_description) if user_description else None
                    )
                    hash_tags = ",".join(get_tweet_hashtags(cur, hashtags, id, user_id))
                    values = [
                        id,
                        created_at,
                        text,
                        user_id,
                        user_screen_name,
                        user_description,
                        tweet_type,
                        reply_to_tweet_id,
                        reply_to_user_id,
                        retweet_to_tweet_id,
                        retweet_to_user_id,
                        hash_tags,
                    ]

                    cur.execute(insert_tweets_table_sql, values)

                    # Save users
                    save_users(cur, tweet, values)

            except ValueError:
                continue

            print(f"Processing line {i} completed.✅")


def main():

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    conn = psycopg2.connect(
        host=host, port=port, user=user, dbname=dbname, password=password
    )
    cur = conn.cursor()
    process_tweets_file(cur)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
