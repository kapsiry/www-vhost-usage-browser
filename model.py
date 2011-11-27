#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlobject import SQLObject, connectionForURI, sqlhub
from sqlobject import StringCol, DecimalCol, DateCol, ForeignKey


class Usage(SQLObject):
    server = StringCol()
    domain = StringCol()
    date = DateCol(default=datetime.now())

    bytes = DecimalCol(size=20, precision=0)
    hits = DecimalCol(size=10, precision=0)

    def __unicode__(self):
        return '''%(date)s %(domain)s: %(kb).0f kB / %(hits)d requests''' % {
        'date': self.date, 'kb': self.bytes/1000, 'hits': self.hits,
        'domain': self.domain}
