# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import io
from .models import RouteExec, ComputedField
import json
from django.http import HttpResponse



def parse_params(params_str):
    ret_dict = {}
    if params_str is None:
        return ret_dict
    if len(params_str) == 0:
        return ret_dict

    if isinstance(params_str, dict):
        return params_str
    try:
        ret_dict = json.loads(params_str)
    except Exception as e:
        print(e)
        print('param parse error')
        print(params_str)

    return ret_dict


def foreign_key_gen(table_name, related_name, del_type='CASCADE'):
    """
    del_type: CASCADE SET_NULL DO_NOTHING

    """

    return "models.ForeignKey(to=" + table_name + ", db_constraint=False, on_delete=models."+del_type+", blank=True, null=True, related_name='" + related_name + "')"

def str_to_obj(obj):
    if obj is None:
        return obj
    return json.loads(obj)


def params_foreign_key_id_update(one_r):
    if one_r['foreign_key_id'] is None:
        return one_r
    if one_r['foreign_key_id'] == '':
        return one_r
    fk = str_to_obj(one_r['foreign_key_id'])
    need_save = 0
    for i in fk:
        if isinstance(fk[i], str):
            fk[i] = [fk[i], 'CASCADE']
            need_save = 1

    if need_save:
        one_r['foreign_key_id'] = json.dumps(fk, indent=2)

    return one_r


def params_update_list(all_one_list):
    all_one_list2=[]
    for i in all_one_list:
        i=params_updata(i)
        all_one_list2.append(i)
    return all_one_list2


def params_updata(one_r: dict):
    one_r = params_foreign_key_id_update(one_r)

    params = {
        'foreign_key_id': str_to_obj(one_r['foreign_key_id']),
        'foreign_key_ro': str_to_obj(one_r['foreign_key_ro']),
        'foreign_slug_kf': str_to_obj(one_r['foreign_slug_kf']),
        'ordering_fields': str_to_obj(one_r['ordering_fields']),
        'ordering': str_to_obj(one_r['ordering']),
        'no_need_login': one_r['no_need_login'],
        'search_fields': str_to_obj(one_r['search_fields']),
        'filter_keys': str_to_obj(one_r['filter_keys']),
        'model_object_list': str_to_obj(one_r['model_object_list'])
    }

    for i in list(params.keys()):
        if params[i] is None:
            del params[i]
    one_r['params'] = json.dumps(params)
    return one_r


def update_models(all_rest_dict_list):
    """
    更新模型文件
    1 读取routeexec种的表名，使用命令inspected生成默认表结构
    2 替换foreign_key 字段
    3 去掉id字段。id如果存在，会导致django程序错误。针对部分表导出后有id的问题
    """
    from django.core.management import call_command
    from django.conf import settings
    import os

    path1 = os.path.join(settings.BASE_DIR, settings.DJANGO_REST_ADMIN_TO_APP)
    file_name = os.path.join(path1,'models.py')

    print(file_name)

    #保存inspectdb数据到stringio.
    f = io.StringIO()

    f.write("from django.contrib.auth.models import User\n")
    #f.write("from AmisNavigationBar.models import AmisNavigation\n")

    table_list = []
    for i in all_rest_dict_list:
        if i['inspected_from_db'] !=1:
            continue
        table_list.append(i['table_name'])
        if i['import_py_code'] is not None:
            f.write(i['import_py_code']+'\n')

    #去除重复的table
    table_list = list(set(table_list))
    if len(table_list) > 0:
        call_command("inspectdb", table_list, stdout=f)
    else:
        f.write('#no table exist in route_exec\n')
    # 所有数据读出到字符串变量：models_new
    models_new = f.getvalue()
    f.close()


    # 此变量用户下面的model外键更改
    # key:className
    # value:{ foreign_key_id中的key _id : foreign_key_id_value  }
    foreign_key_dict2 = {}
    for one_r in all_rest_dict_list:
        # if one_r.re_type == 'table':
        #one_r = params_updata(one_r)
        params = parse_params(one_r['params'])
        if one_r['inspected_from_db'] != 1:
            continue
        if 'foreign_key_id' in params:
            foreign_key_dict2[one_r['table_big_name']] = {}
            for k in params['foreign_key_id']:
                foreign_key_dict2[one_r['table_big_name']][k] = params['foreign_key_id'][k]

    print('update_models foreign_key_dict2:', foreign_key_dict2)

    all_rest_dict_dict={i['table_big_name']:i for i in all_rest_dict_list}

    # 当前model名
    curr_class_name = ''
    f2 = open(file_name, 'w+')
    for one_line in models_new.split('\n'):
        #每行分析处理
        if len(one_line.strip()) == 0:
            # 空行
            f2.write(one_line + "\n")
            continue
        one_line_start_space = len(one_line) - len(one_line.lstrip())
        one_line_striped = one_line.strip()
        if one_line_striped[0] == '#':
            # 注释
            f2.write(one_line + "\n")
            continue

        spt = one_line_striped.split(' ')
        if len(spt) == 0:
            # 没有空格，不认识的行??
            f2.write(one_line + "\n")
            continue

        if (one_line_start_space==0) and (spt[0] == 'class'):
            # 获取类名
            curr_class_name = spt[1].split('(')[0]
            f2.write(one_line + "\n")
            continue

        elif spt[0] == 'class':
            #内部类，在内部类之前，先放入计算属性值
            re1 = RouteExec.objects.filter(table_big_name=curr_class_name, inspected_from_db=1).all()
            if len(re1)<1:
                print('skip this table',curr_class_name, len(re1))
                f2.write(one_line + "\n")
                continue
            cf = ComputedField.objects.filter(route_exec=re1[0]).all()
            for cfi in cf:
                f2.write(' ' * one_line_start_space+cfi.func_text.replace('\r\n','\n'))
                f2.write(' ' * one_line_start_space+"\n")

            f2.write(one_line + "\n")
            continue

        curr_field_name = spt[0]
        if curr_field_name=='id':
            #id自动去除，避免djanog错误
            f2.write(' ' * one_line_start_space )
            f2.write('#' + one_line)
            f2.write('\n')
            continue


        # managed处理
        if curr_field_name == 'managed' and len(spt) == 3:
            if curr_class_name not in all_rest_dict_dict:
                #此class未找到，直接忽略
                print('django_rest_admin:skip class:', curr_class_name)
                f2.write(one_line + "\n")
                continue
            if 'is_managed' not in all_rest_dict_dict[curr_class_name]:
                # 此class未找到，直接忽略
                print('django_rest_admin:skip class2:', curr_class_name)
                f2.write(one_line + "\n")
                continue
            curr_param = all_rest_dict_dict[curr_class_name]['is_managed']
            if curr_param=='True':
                # 不是需要的字段，直接复制
                f2.write(' ' * one_line_start_space + "managed = True\n")
            else:
                # 不是需要的字段，直接复制
                f2.write(' ' * one_line_start_space + "managed = False\n")
            continue

        if curr_class_name not in foreign_key_dict2:
            # 当前class没有外键
            f2.write(one_line + "\n")
            continue

        # 当前class的所有外键
        foreign_key_dict = foreign_key_dict2[curr_class_name]

        # 当前字段是外键
        if curr_field_name in foreign_key_dict:
            # 此行要替换为外键代码

            f2.write(' ' * one_line_start_space)
            f2.write(curr_field_name.replace('_id', ''))
            f2.write(' = ')
            print(curr_class_name, curr_field_name, foreign_key_dict[curr_field_name][0])
            if foreign_key_dict[curr_field_name][0] == curr_class_name:
                itable_name = '"self"'
            else:
                itable_name = foreign_key_dict[curr_field_name][0]

            irelated_name = curr_class_name +'_'+ curr_field_name.replace('_id', '')
            print('irelated_name', irelated_name)
            idel_typ = foreign_key_dict[curr_field_name][1]
            f2.write(foreign_key_gen(itable_name, irelated_name, idel_typ))
            f2.write('\n')
            continue


        f2.write(one_line + "\n")
        continue

    # model写完。此处添加receiver
    file_name_receiver = os.path.join(path1,'models_receiver.py')
    if os.path.exists(file_name_receiver):
        f_recv = open(file_name_receiver, 'r')
        f2.write(f_recv.read())

    f2.close()

    return 'ok'
