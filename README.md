# Project: Social Network

## Service: Social Network Backend API

### Description:
- This code aims to build a simple REST API-based social network in Django where users can sign up, create text posts, and view, like, and dislike the posts of other users.

### Features:
- User 
  - CRUD
  - Login
  - Signup
  - Activation
  - Change Password
- Posts 
  - CRUD
  - Filters
  - likes
- JWT Authentication
- Email services
- Swagger
- Celery
- AbstractAPI 

### Deployment
- Heroku 

### Contents
The main structure of the project is as follows:

```bash  
.
├── config
│ ├── asgi.py
│ ├── celery.py
│ ├── common
│ │ ├── configuration_manager
│ │ │ ├── conf_files
│ │ │ │ └── local.env
│ │ │ ├── configuration_manager_base.py
│ │ │ ├── configuration_manager_env_file.py
│ │ │ ├── configuration_manager_secret_manager.py
│ ├── __init__.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── emails
│ ├── admin.py
│ ├── apps.py
│ ├── __init__.py
│ ├── migrations
│ ├── models.py
│ ├── tasks.py
│ ├── templates
│ │ ├── factory.py
│ │ ├── __init__.py
│ │ ├── template.py
│ │ └── verification.py
│ ├── tests.py
│ └── views.py
├── manage.py
├── posts
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── __init__.py
│ ├── manager.py
│ ├── migrations
│ ├── models.py
│ ├── serializers.py
│ ├── swagger.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── README.md
├── requirements.txt
├── services
│ └── utils.py
├── static
├── staticfiles
└── users
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── management
    │├── commands
    ││ ├── createsu.py
    │  ├── __init__.py
    │ ├── __init__.py
    ├── manager.py
    ├── middleware.py
    ├── migrations
    ├── models.py
    ├── serializers.py
    ├── swagger.py
    ├── tasks.py
    ├── tests.py
    ├── urls.py
    └── views.py

```


### Usage
- ###### Create new environment 
```
  ~$ git clone repo
  ~$ cd social_network
  ~$ python3 -m venv .venv
  ~$ source .venv/bin/activate
```
- ###### Install requirements.txt
```
  (.venv):~$ python3 -m pip install -r requirements.txt
```

- ###### Postgres Database
```
    Add your postgres credentials in 
    config/configuration_manager/conf_files/local.env
```

    
- ###### Migrate to database
```
  (.venv):~$ python manage.py makemigrations users
  (.venv):~$ python manage.py makemigrations posts
  (.venv):~$ python manage.py migrate
```

- ###### Create Super User Account
```
  (.venv):~$ python manage.py createsu
  credentials found in users/management/commands/createsu.py
  
  username: admin
  password: admin
  email: admin@gmail.com
```

#### Celery Configurations

- #### Setup Redis
```
  $ sudo apt update
  $ sudo apt install redis
  $ redis-server
```

- #### Test redis is working (Should return PONG)
```
  redis-cli
  $ 127.0.0.1:6379> ping
  $ PONG
  $ 127.0.0.1:6379>
```

#### Testing
```
  (.venv):~$ python manage.py test users
  (.venv):~$ python manage.py test posts
  (.venv):~$ python manage.py test emails
```

#### Running the server

```
  (.venv):~$ python manage.py runserver
```

##### From a new terminal window
```
  (.venv):~$ python -m celery -A config worker -l info
```
 ##### Test requests from swagger
```
  Swagger endpoint: http://127.0.0.1:8000/
  Authorize with access token retrieved from
  login/signup endpoints
```

### Note:
- To get user holidays based on his ip, this ip should be public ip and unfortunately running server on local (i.e. 127.0.0.1) would produce private ip which produces errors, to handle this you can hard-code your public ip in users/views.py signup endpoint 

### Next steps ...
- Create logging system
  - Create Queue (i.e AWS SQS) for handling requests
  - Configure Elastic search for handling logs
- Customize Rest response to return message in user preference language
- Deployment process (i.e. AWS ElasticBeanstalk)




