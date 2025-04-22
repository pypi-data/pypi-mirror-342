__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import os
import json
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django_rest_admin.get_app_url_base import get_app_url_base

from .models import RouteExec, ComputedField
from .update_models import update_models,params_update_list,parse_params



def resort_rest_models(all_rest_dict_list):
    all_rest_dict_list_new=[]

    # 先按照inspected和id排序
    all_rest_dict_list.sort(key=lambda x:( 0 if x['inspected_from_db'] is None else x['inspected_from_db'], x['id'] ) )

    #重新设置每个的id
    index=0
    for i in all_rest_dict_list:
        i['id'] =index
        index+=100

    # 排序前，准备好各种数据：
    # model_dict={table_big_name:table_dict,...} 获得每个table_big_name对应的id
    # table_dict['foreign_key_models']=[table_big_name1,...] 依赖关系
    model_dict={}
    for i in all_rest_dict_list:
        model_dict[i['table_big_name']] = i

        i['foreign_key_models'] = []

        if i['inspected_from_db']!=1:
            continue
        if (i['foreign_key_id'] is None) or (i['foreign_key_id'] =='') or (i['foreign_key_id'] =='{}') or (i['foreign_key_id'] =='[]'):
            continue

        if isinstance(i['foreign_key_id'], str):
            fk = json.loads(i['foreign_key_id'])
        elif i['foreign_key_id'] is None:
            fk={}
        else:
            fk = i['foreign_key_id']
        for j in fk:
            i['foreign_key_models'].append(fk[j][0])


    # 根据model_dict 和 table_dict进行排序，顺序由id标识
    for i in all_rest_dict_list:
        i['foreign_key_models_smallest'] = i['id']
        for j in i['foreign_key_models']:
            if j in model_dict:
                if i['foreign_key_models_smallest']<model_dict[j]['id']:
                    i['foreign_key_models_smallest'] = model_dict[j]['id']+1
        if i['foreign_key_models_smallest']>i['id']:
            i['id'] = i['foreign_key_models_smallest']



    all_rest_dict_list.sort(key=lambda x:(  x['id'] ) )

    for i in all_rest_dict_list:
        print(i['id'],  i['table_big_name'], i['foreign_key_models_smallest'])

    return all_rest_dict_list


def update_url_file():
    from django.conf import settings

    path1 = os.path.join(settings.BASE_DIR, settings.DJANGO_REST_ADMIN_TO_APP)
    print('write_to_file-path1:', path1)
    urls_py_file_path = os.path.join(path1, 'urls.py')
    if os.path.exists(urls_py_file_path):
        return
    else:
        path1=os.path.dirname(__file__)
        template_file = os.path.join(path1,'urls_template.py')
        f=open(template_file,'r')
        temp_content = f.read()
        f.close()
        f=open(urls_py_file_path,'w')
        f.write(temp_content)
        f.close()



def write_to_file(to_write_str):

    from django.conf import settings
    path1 = os.path.join(settings.BASE_DIR, settings.DJANGO_REST_ADMIN_TO_APP)
    print('write_to_file-path1:',path1)
    urls_rest_py_file_path = os.path.join(path1,'auto_urls_rest.py')
    print('write_to_file:',urls_rest_py_file_path)
    f_to_w = open(urls_rest_py_file_path,'wb')
    f_to_w.write(to_write_str.encode('utf-8'))
    f_to_w.close()

def list_model_to_dict(all_rest):
    all_rest_dict_list=[]
    for i in all_rest:
        all_rest_dict_list.append(model_to_dict(i))
    return all_rest_dict_list


def none_str(kk):
    return 'None' if kk is None else str(kk)

def generate_rest_code(all_rest_dict_list):
    to_write_str=''
    to_write_str +='from django_rest_admin.my_rest_api import my_rest_viewsetB\n'
    to_write_str += 'from .models import *\n'
    to_write_str += 'from .urls import router\n'

    for i in all_rest_dict_list:
        if i['route'] is None:
            continue
        to_write_str+='####################################\n'
        to_write_str += '#for route'+i['route']+'\n'
        if i['import_py_code'] is not None:
            to_write_str += i['import_py_code']+'\n'
        to_write_str += 'routeName="' + i['route']+'"\n'
        to_write_str += """
if routeName[0] == '/':
    routeName = routeName[1:]
tableBName = routeName
"""
        to_write_str +='foreign_key_ro = ' +none_str(i['foreign_key_ro'])+'\n'
        to_write_str += 'foreign_key_id = ' + none_str(i['foreign_key_id']) + '\n'
        to_write_str += 'model_obj_list = ' + none_str(i['model_object_list']) + '\n'
        to_write_str += 'filter_fields = None\n' #+ none_str(i['filter_fields']) + '\n'
        to_write_str += 'no_need_login = ' + none_str(i['no_need_login']) + '\n'
        to_write_str += 'search_fieldsA = ' + none_str(i['search_fields']) + '\n'
        to_write_str += 'ordering = ' + none_str(i['ordering']) + '\n'
        to_write_str += 'ordering_fields = ' + none_str(i['ordering_fields']) + '\n'
        to_write_str += 'filter_keys = ' + none_str(i['filter_keys']) + '\n'
        to_write_str += 'foreign_slug_kf = ' + none_str(i['foreign_slug_kf']) + '\n'

        to_write_str += 'if model_obj_list is None:\n    model_obj_list="__all__"\n'

        to_write_str += 'if foreign_key_id is not None:\n    for i in foreign_key_id:\n        foreign_key_id[i]= globals()[foreign_key_id[i][0]]\n'

        to_write_str +=  "choice_problems = my_rest_viewsetB(" + str(i['table_big_name']) + ", tableBName + 'V',"
        to_write_str += """
               model_obj_list=model_obj_list, no_need_login=no_need_login,
               foreign_key_ro=foreign_key_ro, foreign_key_id=foreign_key_id,
               filter_fieldsA=filter_fields,
               search_fieldsA=search_fieldsA, orderingA=ordering,
               ordering_fieldsA=ordering_fields, filter_keys=filter_keys,
               foreign_slug_kf=foreign_slug_kf)
               \n"""
        to_write_str += '\nrouter.register(routeName, choice_problems) \n'
        to_write_str += '####################################\n'


    return to_write_str


from .get_table_foreignkey_param import get_table_foreignkey_param


def update_rest(request):
    """
    将各rest的依赖关系顺序整理好
    依次输出代码至 urls_rest
    """
    from django.conf import settings
    if not hasattr(settings, 'DJANGO_REST_ADMIN_TO_APP'):
        return """DJANGO_REST_ADMIN_TO_APP in project settings.py should be set. 
        """

    try:
        app_base = get_app_url_base()
    except Exception as e:
        update_url_file()
        return "请设置%s.urls到项目urls.py中,然后点击 生成RestAPI"%settings.DJANGO_REST_ADMIN_TO_APP



    all_rest = RouteExec.objects.all()
    all_rest_dict_list=list_model_to_dict(all_rest)

    all_rest_dict_list = params_update_list(all_rest_dict_list)

    for i in all_rest_dict_list:
        if (i['foreign_key_id'] is None) or (i['foreign_key_id']==''):
            i['foreign_key_id']={}
        elif isinstance(i['foreign_key_id'], str):
            i['foreign_key_id'] = json.loads(i['foreign_key_id'])
        i['foreign_key_id'].update(get_table_foreignkey_param(i['table_name']))


    all_rest_dict_list = resort_rest_models(all_rest_dict_list)

    update_models(all_rest_dict_list)

    to_write_str=generate_rest_code(all_rest_dict_list)
    update_url_file()
    write_to_file(to_write_str)

    return 'ok'
