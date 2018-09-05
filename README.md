## Mporter (Mentor Reporter)

<p align="center">
    <img src="https://imgur.com/zc455hVl.png"/>
</p>

*Try it out here: [https://mporter.co](https://mporter.co)*

[![Build Status](https://travis-ci.org/abhn/Mporter.svg?branch=master)](https://travis-ci.org/abhn/Mporter)
[![codecov](https://codecov.io/gh/abhn/Mporter/branch/master/graph/badge.svg?token=fofAGeN2Od)](https://codecov.io/gh/abhn/Mporter) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple flask project for easy reporting daily/weekly/monthly updates to one's mentor. You need to simply add tasks the way you write commit messages, and Mporter will take care of delivering an email to your mentors at a preset time.

### Demo
[https://mporter.co](https://mporter.co)

### One Click Installer
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/abhn/mporter)

### Index
- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Vocabulary](#vocabulary)
    - Tasks
    - Mentee
    - Mentor
- [Getting Started](#getting-started)
- [REST API](#rest-api)
    - POST /api/auth
    - POST /api/task
    - GET /api/task
    - POST /api/mentor
    - GET /api/mentor
- [Ingredients](#ingredients)
- [Contributing](#contributing)
- [License](#license)


### Introduction
Have you ever faced the problem of discipline where you had to report your progress with a project or a problem to a person (mentor?), but you totally forgot? I have, and this little project tries to solve that problem.

With **Mporter**, you just have to keep adding your *tasks* (things that you did) and the app handles timely reporting to the people that you add as mentors. 

Yes, think of it like Twitter but with a twist. Instead of you getting the tweets of people you add, the people you add get your tweets (Tasks) instead.

### Features
- **Multiple Mentee-Mentor support**. You can use one instance with your friends with overlap of Mentors in between the Mentees.
- **Login & Register** support for creation and authentication of Mentee accounts.
- **Admin panel** for easy administration of users, tasks etc.
- **Admin roles** are set up to limit the access of admin panel to few people. 
- **RESTFul APIs** for integrating Mporter in your workflow, be it terminal (using curl), phone or browser plugin.
- **Traditional & JWT** based auth to suit wide range of usecases.
- Clutter free UI, easy to use, fully open source.


### Screenshots
A list of tasks welcome you as you log into the app

![Tasks](/tmp/tasks.png?raw=true "tasks screen")

You can find your mentors in the mentors tab.

![Mentor](/tmp/mentors.png?raw=true "mentors screen")

For the admin users, there's a panel for easy CRUD operations

![Admin](/tmp/admin.png?raw=true "admin screen")

### Vocabulary
- **Tasks**: Some piece of work that you did. 
    - *Wrote a blog post and published on X blog* is a task. 
    - *Solved a bug X in application Y* is another. 
    
    On the other hand, 
    - *Studied hard* might not be a good task description (too vague) 
    - *Cleaned my room* is something that your mentor might not be interested in (or maybe they are, you be the judge). 

- **Mentee**: A person who creates and wants to report Tasks
    - Ideally, it would be you, the reader of this readme. 

- **Mentor**: A person who receives your Task reports for the time interval.
    - You can add multiple mentors in the `/mentee` page, which is like your profile page
    
    
### Installation
To use this application, some preliminary steps have to be performed. While most of it is simple command copy-pasting, it can get thick at times. In those times, use Google and search for error messages. 

Following are the steps needed to put this app on [Heroku](https://heroku.com) which is a nice place to host hobby projects, but with little more effort, you can put this up on a private server like [Digital Ocean's droplet](https://www.digitalocean.com/products/droplets/) or even your Raspberry Pi.

1. Clone this repository
2. Create a new app in heroku on hobby tier
3. Create two `Data` instances, which are just `Postgres` database instances. Select the free tier.  One is our prodution database and the other is for running test cases on Travis (optional).
4. In `Elements` menu for your app, you need to enable `RabbitMQ Bigwig` addon. This will be used as our Celery backend to schedule email delivery. Note the `broker url` in the addon's settings page.
5. Now in the `Deploy` tab, select Github and add your cloned repository.
6. Set `automatic deploys` so that every push to your `master` will trigger rebuild and deploy. Do a `manual deploy` once to check things. It will fail, and that's okay.
7. Create an account on [Mailgun](https://www.mailgun.com/) and get their `key` and `sandbox url`. Mailgun will deliver our emails. Note that for the free account, you'll have to manually confirm each account that you are planning to send emails to (ask your mentors to trust that email).
8. We need to set [env variables](https://devcenter.heroku.com/articles/config-vars). To set an environment variable, use the command:
    `$ heroku config:set VAR_NAME=var_value`
    You'll be able to use this variable in your app as `import os; os.environ.get('VAR_NAME')`. Do that for each variable in the list below. For example, `$ heroku config:set MPORTER_SECRET='abcd123'` and so on.
9. Set the following env variables. I have created a corresponding `env.sh` file locally and added it to my `.gitignore` to not pollute my `~/.bashrc`:
    ```bash
    #!/usr/bin/env bash
    
    export FLASK_APP=app
    export MPORTER_SECRET=<some random>
    export RABBITMQ_BIGWIG_URL=<the rabbitmq bigwig url>
    export MAILGUN_API_KEY=<mailgun key>
    export MAILGUN_DOMAIN=<mailgun sandboxurl>
    export DATABASE_URL=<first heroku data addon's url>
    export HEROKU_POSTGRESQL_GRAY_URL=<second heroku data addon's url>
    
    ```
If you're using Heroku (or used the one click installer), all except `MPORTER_SECRET` will already be present. To view the values (and copy them locally), do a `heroku config` in your project directory
10. Click the `deploy manually` button again, and your app should (hopefully) be live. 


### REST API
The app exposes some REST APIs for use via other application (or command line). All APIs are authenticated via JWT, and the JWT can be obtained in exchange of login credentials.

#### `[POST]/api/auth`
- Description: Get an authentication token in exchange of email and password.
- Request: `{email: <user_email>, password: <user_password>}` 
- Response: `{token: <token | null>, success: <True | False>}`

#### `[POST]/api/task`
- Description: Create a new task under the authenticated user.
- Request: `{task: "new task name"}`
- Headers: `Authorization: <token>`
- Response: `{success: <True | False>}`

#### `[GET]/api/task`
- Description: Fetch all tasks for the current day for the authenticated user
- Request: `null`
- Headers: `Authorization: <token>`
- Response: 
```javascript
{
    success: <True | False>, 
    tasks: [
        {task: <task>, at_created: <timestamp>, 
        ...
    ]
}
```

#### `[POST]/api/mentor`
- Description: Add a new mentor for the authenticated user. If mentor doesn't exist, create new mentor.
- Request: `{mentor_name: "new mentor name", mentor_email: "test@mentor.com}`
- Headers: `Authorization: <token>`
- Response: `{success: <True | False>}`

#### `[GET]/api/mentor`
- Description: Fetch all mentors of the authenticated user
- Request: `null`
- Headers: `Authorization: <token>`
- Response:
```javascript
{
    success: <True | False>, 
    mentors: [
        {mentor_name: <name>, mentor_email: <email>, 
        ...
    ]
}
```

### Ingredients
- [Flask-Admin](https://github.com/flask-admin/flask-admin) for the read to use admin pages like those Django gives you.
- [Flask-Security](https://github.com/mattupstate/flask-security) for login/registration logic, session management etc.
- [Celery Python](https://pypi.org/project/celery/) for scheduling asynchronous tasks.
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) for orm
- [Pytest](https://docs.pytest.org/en/latest/) for testing
- [Flask-RESTFul](https://flask-restful.readthedocs.io/en/latest/) for the REST APIs

### TODO
1. Beautify `/mentee` page with some CSS and make it mobile responsive.
2. <strike>Implement REST APIs for extending the functionality to non-web apps.</strike>
2. <strike>Implement JWT auth for authentication of RESTful APIs</strike>
3. Slack bot for posting task as well as receiving task notification
4. PWA


### Contributing
- TODO

### License
MIT
