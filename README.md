### ITLan's "Short URL" async fastapi test task

## 1.1 Features:
- Asynchronous PostgreSQL queries
- Short links with expiration date

## 1.2 Task requirements endpoints
- list of links `GET /links/?limit={limit}&offset={offset}`
- create short link `POST /links/`
- follow the short link `GET /{link_name}/`

## 1.3 Example and deployed project

1. Visit and check docs`https://97y3sv.deta.dev/docs/`
2. Post `{
  "days_to_expire": 90,
  "destination_url": "https://youtube.com"
}` to `https://97y3sv.deta.dev/links/`
3. You will receive such response body`{
  "url": "https://97y3sv.deta.dev/unW6a4",
  "expires_at": "2023-04-21T15:06:38.394660"
}`
4. If you follow the `https://97y3sv.deta.dev/unW6a4` you will be redirected to `https://youtube.com`
5. List of created short links you can find at `https://97y3sv.deta.dev/links/?limit=10&offset=0`


## 1.4 Local installation:

Python3 and PostgreSQL should be installed

Venv:
- Install venv `python3 -m venv venv`
- Activate venv `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
   
DB and run server:
- Create DB: user:`postgres`, password:`postgres`, host:`localhost`, dbname: `shorturl` and uncomment `SQLALCHEMY_DATABASE_URL` in db/database.py or create db with the custom creds and specify them there
- Launch server `uvicorn main:app --reload`
- Restore data `psql shorturl < db.dump`
- Check api endpoints docs:  `http://127.0.0.1:8000/docs`