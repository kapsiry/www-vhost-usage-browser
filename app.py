#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import environ as env
from functools import wraps
from datetime import timedelta
from datetime import datetime

from sqlobject import AND

from flask import *

from model import *

app = Flask(__name__)

@app.route('/')
def index():
    # Person.select(Person.q.firstName=="John")
    day_before_yesterday = datetime.now() - timedelta(days=2)

    usages = Usage.select(AND(
        Usage.q.date >= day_before_yesterday,
        Usage.q.date <= datetime.now()),
        orderBy="-bytes")
    return render_template('index.html', usages=usages)


if __name__ == "__main__":
    sqlhub.processConnection = connectionForURI(env['DATABASE_URL'])
    app.debug = True
    if len(sys.argv) > 1:
        app.run(host="0.0.0.0", port=int(sys.argv[1]))
    else:
        app.run()
