# Mahsa Server

## What is Mahsa Server?
TBD

## How to run
1. install docker and docker-compose
2. `docker-compose up -d`

## How to check
* http://localhost (nginx/frontend)
* http://localhost/backend/app/ (django)
* http://localhost/backend/admin/ (django admin)
* http://localhost:9001 (backend supervisord interface)
* http://localhost:6001 (flower - celery task monitoring)

## How to develop
### Frontend
```
cd frontend
npm install
npm run serve
```
### Backend
```
cd backend
virtualenv .env --python=python3.8
source .env/bin/activate
pip3 install -r requirements.txt
```
#### Django
```
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
./manage.py createsuperuser  # create a django superuser (for admin login)
```
#### Endpoints
* Config
  
  ```
  [POST] /backend/app/config/
  [GET] /backend/app/config/<uuid>/
  [GET] /backend/app/config/stats/
  ```
* Report
  ```
  [POST] /backend/app/report/
  ```

#### Celery
* Worker
  ```
  celery -A worker.app worker --loglevel=info
  ```
* Beat Scheduler
  ```
  celery -A worker.app beat --loglevel=info
  ```
* Flower
  ```
  celery -A worker.app flower --loglevel=info
  ```
## Docker Services
* backend: django, celery
* nginx: serves frontend and static files + proxy to backend service via /backend
* redis

## Tech Stack
* backend
  * django
  * celery (running async tasks)
  * supervisor (managing backend processes)
* frontend
  * Vue.js (can be replaced by any frontend framework)
* redis (used for celery)
* sqlite (django database)