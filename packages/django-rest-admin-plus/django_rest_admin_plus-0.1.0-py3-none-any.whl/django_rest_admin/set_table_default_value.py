__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from .get_table_foreignkey_param import get_table_fields, get_table_foreignkey_param
import json
import re
from .models import DbTableToRest, RouteExec
from django.conf import settings

def set_table_default_value(obj_to_mod):
    """
    如果某些参数没设置，则设置默认值
    """
    i = obj_to_mod
    if i.table_name is None or i.table_name=='':
        return 'nothing to change'

    if not hasattr(settings, 'DJANGO_REST_ADMIN_TO_APP'):
        return 'please set DJANGO_REST_ADMIN_TO_APP in settings.py first'

    table_infos = DbTableToRest.objects.filter(table_name=obj_to_mod.table_name).all()
    if (len(table_infos)==0) or (table_infos[0].in_app_name is None) or (table_infos[0].in_app_name =='') or  (table_infos[0].in_app_name =='django_rest_admin') or (table_infos[0].in_app_name==settings.DJANGO_REST_ADMIN_TO_APP):
        if i.inspected_from_db is None:
            i.inspected_from_db=1
        i.import_py_code=None

        if (i.is_managed is None) or (i.is_managed==''):
            if (len(table_infos)==0) or table_infos[0].t_type!='view':
                i.is_managed='True'
            else:
                i.is_managed = 'False'

        if (i.table_big_name is None) or (i.table_big_name==''):
            i.table_big_name = re.sub(r'[^a-zA-Z0-9]', '', i.table_name.title())

    else:
        #其他app中的表，直接import
        app_name = table_infos[0].in_app_name
        i.import_py_code = 'from '+app_name+'.models import '+table_infos[0].model_name+'\n'
        if i.inspected_from_db is None:
            i.inspected_from_db=0
        i.is_managed='False'
        i.table_big_name = table_infos[0].model_name

    if (i.route is None) or (i.route ==''):
        route = '/' + re.sub(r'[^a-zA-Z0-9]', '', i.table_name.title())
        rindex=0
        while len(RouteExec.objects.filter(route = route).all())>0 :
            route = '/' + re.sub(r'[^a-zA-Z0-9]', '', i.table_name.title())+"_"+str(rindex)
            rindex+=1
        i.route = route


    if i.foreign_key_id is None or (i.foreign_key_id=='') or (len(i.foreign_key_id)==0):
        i.foreign_key_id = get_table_foreignkey_param(i.table_name)
    if i.ordering_fields is None:
        field_list = get_table_fields(i.table_name)
        i.ordering_fields = field_list
    if i.ordering is None:
        field_list = get_table_fields(i.table_name)
        i.ordering =  field_list
    if i.search_fields is None:
        #搜索项不能有外键
        field_list = get_table_fields(i.table_name, 0)
        i.search_fields = field_list
    if i.no_need_login is None:
        i.no_need_login = 1

    if (i.foreign_key_ro is None) or (i.foreign_key_ro=='') or (len(i.foreign_key_ro)==0):
        foreign_key = get_table_foreignkey_param(i.table_name,1)
        i.foreign_key_ro={}
        for j in foreign_key:
            field_list = get_table_fields(foreign_key[j][2], 0)
            for k in field_list:
                if len(j)>3:
                    if j[-3:]=='_id':
                        j=j[:-3]
                i.foreign_key_ro[str(j)+'_' + str(k)] = str(j)+'.' + str(k)


    if (i.filter_keys is None) or (i.filter_keys =='') or (len(i.filter_keys)==0):
        i.filter_keys=[{
            'filter_name':'id',
            'field_name':'id',
            'filter_type':'number',
            'lookup_expr':'exact'
        }]


    if i.model_object_list is None:
        field_list = get_table_fields(i.table_name)
        i.model_object_list = field_list



    i.save()
    return 'ok'