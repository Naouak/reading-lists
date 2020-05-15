# Library and Book backlog manager

A web app to manage your reading lists.

**Note that this is not production ready yet. Use at your own risks.**

## Set up

```shell script
cd backend/
pip -r requirements.txt install
cp .env.sample .env
python manage.py migrate
python manage.py createsuperuser
python manage.py setup


# edit .env with your values
cd ../frontend/
npm ci
cp .env.sample .env
# edit .evn with your values
```

## Start

```shell script
cd backend/ && python manage.py runserver 8000
cd frontend/ && npm run dev
```

The app should be available on http://localhost:3000/