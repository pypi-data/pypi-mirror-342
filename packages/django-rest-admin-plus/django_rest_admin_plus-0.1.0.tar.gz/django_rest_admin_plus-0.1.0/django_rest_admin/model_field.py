# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import json
from django.db import models


class JSONField(models.TextField):
    #__metaclass__ = models.SubfieldBase
    description = "this is a json Text"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self,connection):
        return super().db_type(connection)
    def to_python(self, value):
        v = models.TextField.to_python(self, value)
        try:
            return json.loads(v)
        except:
            return '{}'
        return v
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return json.dumps(value)



class CodeField(models.TextField):
    #__metaclass__ = models.SubfieldBase
    description = "this is a code Text"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self,connection):
        return super().db_type(connection)

    #
    #def from_db_value(self, value, expression, connection):
    #    #ret = super().from_db_value(value, expression, connection)
    #    return self.to_python(value)


    def to_python(self, value):
        v = models.TextField.to_python(self, value)
        return v
    #
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return str(value)

