### ITLan's "Short URL" async fastapi test task

## 1.1 Features:
- Asynchronous PostgreSQL queries
- Short links with an expiration date

## 1.2 Task requirements endpoints
- list of links `GET /links/?limit={limit}&offset={offset}`
- create short link `POST /links/`
- follow the short link `GET /{link_name}/`

## 1.3 Example and deployed project

1. Visit and check docs`https://97y3sv.deta.dev/docs/`
2. Post `{"days_to_expire": 90, "destination_url": "https://youtube.com"}` to `https://97y3sv.deta.dev/links/`
3. You will receive such response body`{"url": "https://97y3sv.deta.dev/unW6a4", "expires_at": "2023-04-21T15:06:38.394660"}`
4. If you follow the `https://97y3sv.deta.dev/unW6a4` you will be redirected to `https://youtube.com`
5. List of created short links you can find at `https://97y3sv.deta.dev/links/?limit=10&offset=0`


## 1.4 Local installation:

Python3 and PostgreSQL should be installed

Venv:
- Install venv `python3 -m venv venv`
- Activate venv `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
   
DB and run server:
- Create DB: user:`postgres`, password:`postgres`, host:`localhost`, dbname: `shorturl` or create a db with the custom creds and specify them in `config.py` in `SQLALCHEMY_DATABASE_URL`
- Launch server `uvicorn main:app --reload`
- Restore data `psql shorturl < db.dump`
- Check API endpoints docs:  `http://127.0.0.1:8000/docs`

## 1.5 Implementation details

Short url includes 6 characters. Each character is a lowercase letter/uppercase letter/digit. Total unique combinations = 66^6 ~ 82.6 * 10^9. If a collision is happening, url is created upon a destination url + salt to avoid it.

Current implementation keep short url unique. It is not possible to get the same short url that was created before.
Alternative possible implementations:
- Reuse created short urls if they are expired for other destination urls.
- Dynamic length of the short url, for example, start with 4 and increase if many collisions will happen.