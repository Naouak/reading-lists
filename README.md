# Library and Book backlog manager

A web app to manage your reading lists.

## Features

 * Import Marvel Unlimited available issues to build a list of books
 * Create a reading list by adding and ordering issues
 * Mark books as read to progress your reading lists
 * Automatically fill reading list with new issues from series.
 * Support multiple readings for a same book
 
It's basically my own [panelhive](https://app.panelhive.io) catered to my own needs and wishes.

## What it doesn't do

 * Support multiple users (and it is not planned)
 * Have UI to manage books/series
 * No efforts has been made in terms of accessibility

**Note that this *may* not be production ready yet. Use at your own risks.**
I'm currently using it on my own and it's working fine but I can't ensure anything about the stability or the security.

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
# edit .env with your values
NODE_OPTIONS=--openssl-legacy-provider npm run build
# That NODE_OPTIONS is necessary for nuxt2 build on later node versions. Blame Nuxt
```

## Start for development

```shell script
cd backend/ && python manage.py runserver 8000
cd frontend/ && npm run dev
```

The app should be available on http://localhost:3000/

## Consideration for production

Here is my production infrastructure, use it as your own risks:

On a dev vps on scaleway, I use nginx for SSL termination. SSL is managed using certbot and letsencrypt.

One DNS entry/virtualhost going to django through UWSGI.

One DNS entry/virtualhost going to the dist directory of the frontend.

I use memcached for the cache and mariadb for the database.

Django is run using a virtualenv I created directly in the backend directory.

When I deploy a new version I basically do:

```bash
git pull

cd backend/
source venv/bin/activate
python manage.py migrate
sudo /etc/init.d/uwsgi reload

cd ../frontend/
npm run-script build
```

I set up a cron to checkout new issues from marvel-api like this:

```bash
python manage.py checkout_marvel comics
```