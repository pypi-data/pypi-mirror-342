__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from .models import DbTableToRest,RouteExec
from django  import  VERSION
from django.apps import apps

from django.db import models

def update_table_list(request):

    table_name_exception=['sqlite_sequence', 'django_migrations']

    # 查找django中的app中包含的 models
    #apps_to_loop = apps.get_app_configs()
    #for i in apps_to_loop:
    from django.db import connection
    index=0

    # 清空所有记录
    DbTableToRest.objects.all().delete()

    # 添加app中由models的表
    models_to_loop = apps.get_models(include_auto_created=True)
    for i in models_to_loop:
        table_name = i._meta.db_table
        app_name = i._meta.app_label
        model_name =i.__name__
        is_exists=DbTableToRest.objects.filter(table_name=table_name).all()
        if len(is_exists)>0:
            continue

        index+=1
        tab_rcd = DbTableToRest()
        tab_rcd.id=index
        tab_rcd.table_name = table_name
        tab_rcd.in_app_name = app_name
        tab_rcd.has_api = len(RouteExec.objects.filter(table_name = table_name).all())
        tab_rcd.model_name = model_name
        tab_rcd.save()

    # 添加所有的数据库中的table
    sql_str="SELECT name FROM sqlite_master WHERE type='table';"
    cursor = connection.cursor()
    cursor.execute(sql_str)
    row_list = cursor.fetchall()
    for i in  row_list:
        table_name = i[0]
        if table_name in table_name_exception:
            continue

        is_exists=DbTableToRest.objects.filter(table_name=table_name).all()
        if len(is_exists)>0:
            is_exists[0].t_type = 'table'
            is_exists[0].save()
            continue

        index+=1
        tab_rcd = DbTableToRest()
        tab_rcd.id = index
        tab_rcd.t_type = 'table'
        tab_rcd.table_name = table_name
        tab_rcd.in_app_name = None
        tab_rcd.has_api = len(RouteExec.objects.filter(table_name = table_name).all())
        tab_rcd.model_name = None

        tab_rcd.save()

    # 添加所有的数据库中的view
    sql_str = "SELECT name FROM sqlite_master WHERE type='view';"
    cursor = connection.cursor()
    cursor.execute(sql_str)
    row_list = cursor.fetchall()
    for i in row_list:
        table_name = i[0]
        if table_name in table_name_exception:
            continue

        is_exists = DbTableToRest.objects.filter(table_name=table_name).all()
        if len(is_exists) > 0:
            #已经存在，不再操作
            is_exists[0].t_type = 'view'
            is_exists[0].save()
            continue

        index += 1
        tab_rcd = DbTableToRest()
        tab_rcd.id = index
        tab_rcd.t_type = 'view'

        tab_rcd.table_name = table_name
        tab_rcd.in_app_name = None
        tab_rcd.has_api = len(RouteExec.objects.filter(table_name=table_name).all())
        tab_rcd.model_name = None

        tab_rcd.save()












