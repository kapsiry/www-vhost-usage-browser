# WWW vhost usage browser
## Database settings

The application reads its database settings from the environment variable
DATABASE_URL, which is an SQLObject database uri.

## Bootstrapping your environment (using virtualenv)
* `virtualenv --no-site-packages env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
