# ETL (Extract Transform Load)

This script is responsible for extracting data from a .txt file dataset, transforms it and load it into a PostgreSQL database.

## Prerequisites

```
- Python 3.10.2
```

## Installation and setup

- Clone the repo

```
git clone https://github.com/Paccy10/pivot-user-recommandation-system-etl.git

```

- Download python

```
https://www.python.org/downloads/
```

- Create the virtual environment

```
python -m venv venv
```

- Activate virtual environment

  - MacOS and Linux

  ```
  source venv/bin/activate
  ```

  - Windows

  ```
  .\venv\Scripts\activate
  ```

- Install dependencies

```
pip install -r requirements.txt
```

- Add the dataset file in the root folder and rename it to "tweets.data.txt"

- Add the hashtags file in the root folder and rename it to "hashtags.data.txt"

- Create a PostgreSQL database

- Make a copy of the .env.sample file and rename it to .env and update the variables accordingly

- Create tables

```
python db.py
```

## Running the ETL

- Running script

```
python main.py
```
