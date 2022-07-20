import os
import psycopg2

from sql.create import *
from sql.drop import *

from dotenv import load_dotenv

load_dotenv()

create_tables_queries = [
    create_tweets_table_sql,
    create_users_table_sql,
    create_hashtags_table_sql,
]

drop_tables_queries = [
    drop_tweets_table_sql,
    drop_hashtags_table_sql,
    drop_users_table_sql,
]


def connect_database():
    conn = psycopg2.connect(
        f"host={os.getenv('POSTGRES_HOST')} port={os.getenv('POSTGRES_PORT')} user={os.getenv('POSTGRES_USER')} password={os.getenv('POSTGRES_PASSWORD')} dbname={os.getenv('POSTGRES_DB')}"
    )

    cur = conn.cursor()
    return cur, conn


def drop_tables(cur, conn):
    print("Dropping tables start...")

    for query in drop_tables_queries:
        cur.execute(query)
        conn.commit()

    print("Dropping tables Complete ✅")


def create_tables(cur, conn):
    print("Creating tables start...")

    for query in create_tables_queries:
        cur.execute(query)
        conn.commit()

    print("Creating tables Complete ✅")


def main():
    cur, conn = connect_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
