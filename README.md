

#Packages used for this projects are as follows: flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-migrate flask-restful flask-script psycopg2==2.7.7


#Postgres DB
docker run --rm --name pg-docker -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres

#Migrating DB
python manage.py db init
python manage.py db migrate
python manage.py db upgrdate
