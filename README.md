Plivo Realtime Conference Demo
=====================

Clone this repo:

    $ git clone git@github.com:bevenky/plivo_conference_demo.git
    $ cd plivo_conference_demo


Deploying to Heroku
---------------------

    $ heroku create <app_name> -s cedar
    $ git push heroku master
    $ heroku scale web=1
    $ heroku ps
    $ heroku open
