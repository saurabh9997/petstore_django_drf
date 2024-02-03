### What is this repository for? ###

This is the python repo for petstore service.
There are 1 major component to this:

* Django App: REST APIs

### How do I get set up? ###

#### Local

Create & Activate a Virtual Environment

```commandline
sudo pip install virtualenv
virtualenv ~/Projects/venv/petstore-env -p python3.9
source ~/Projects/venv/petstore-env/bin/activate
```

Installing Requirements

```commandline
pip install -r requirements.txt
```

Migrate Script

```commandline
python manage.py makemigrations 
python manage.py migrate
```

Start the Django Application

```commandline
python manage.py runserver
```
