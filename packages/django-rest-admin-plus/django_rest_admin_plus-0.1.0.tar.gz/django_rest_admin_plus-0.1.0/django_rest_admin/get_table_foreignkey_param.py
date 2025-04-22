
import re
import io
from django.db import connection


def get_models_param_from_inspectdb(table_name, add_real_table_name=0):
    """
        {"user":["User", "CASCADE"], "article":["Article", "SET_NULL"]}
    """
    from django.core.management import call_command

    if not table_name:
        return {}

    foreign_key_id = {}

    f = io.StringIO()
    call_command("inspectdb", [table_name], stdout=f)
    models_new = f.getvalue()
    f.close()

    for one_line in models_new.split('\n'):
        if not one_line.strip() or one_line.strip().startswith('#'):
            continue

        one_line_start_space = len(one_line) - len(one_line.lstrip())
        one_line_striped = one_line.strip()
        spt = one_line_striped.split(' ')

        if one_line_start_space == 0 and spt[0] == 'class':
            curr_class_name = spt[1].split('(')[0]
            continue

        curr_field_name = spt[0]
        if curr_field_name == 'id':
            continue

        if len(spt) > 2 and 'models.ForeignKey(' in spt[2]:
            foreign_table_name = spt[2].split('\'')[1]
            foreign_on_delete = spt[3].split('.')[1].strip(',')
            foreign_key_id[curr_field_name] = [foreign_table_name, foreign_on_delete]

    return foreign_key_id


def get_table_fields(table_name, is_with_foreignkey=1):
    """
    返回一个表里的字段名列表，支持 MySQL / SQLite / PostgreSQL
    """
    cursor = connection.cursor()

    if connection.vendor == 'sqlite':
        cursor.execute(f'''PRAGMA table_info("{table_name}")''')
        row_list = cursor.fetchall()
        ret = [i[1] for i in row_list]
        if is_with_foreignkey != 1:
            cursor.execute(f'''PRAGMA foreign_key_list("{table_name}")''')
            row_list = cursor.fetchall()
            for i in row_list:
                if i[3] in ret:
                    ret.remove(i[3])
        return ret

    elif connection.vendor == 'mysql':
        cursor.execute(f'''DESCRIBE `{table_name}`''')
        row_list = cursor.fetchall()
        return [i[0] for i in row_list]

    elif connection.vendor == 'postgresql':
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
        """, [table_name])
        return [row[0] for row in cursor.fetchall()]

    else:
        raise NotImplementedError(f"Unsupported DB vendor: {connection.vendor}")


def get_table_foreignkey_param_using_pragma(table_name, add_real_table_name=0):
    """
    获取外键信息，支持 SQLite、MySQL、PostgreSQL
    """
    foreign_key_id = {}
    if not table_name:
        return {}

    cursor = connection.cursor()

    if connection.vendor == 'sqlite':
        cursor.execute(f'''PRAGMA foreign_key_list("{table_name}")''')
        row_list = cursor.fetchall()
        for row in row_list:
            row_dict = {
                'id': row[0], 'seq': row[1], 'table': row[2], 'from': row[3],
                'to': row[4], 'on_update': row[5], 'on_delete': row[6], 'match': row[7]
            }
            key = row_dict['from']
            value = [
                re.sub(r'[^a-zA-Z0-9]', '', row_dict['table'].title()),
                row_dict['on_delete']
            ]
            if add_real_table_name:
                value.append(row_dict['table'])
            foreign_key_id[key] = value

    elif connection.vendor == 'mysql':
        cursor.execute(f'''
            SELECT
                kcu.COLUMN_NAME, kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME, rc.DELETE_RULE
            FROM
                information_schema.KEY_COLUMN_USAGE AS kcu
            JOIN
                information_schema.REFERENTIAL_CONSTRAINTS AS rc
            ON
                kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
                AND kcu.CONSTRAINT_SCHEMA = rc.CONSTRAINT_SCHEMA
            WHERE
                kcu.TABLE_NAME = %s AND
                kcu.CONSTRAINT_SCHEMA = DATABASE() AND
                kcu.REFERENCED_TABLE_NAME IS NOT NULL
        ''', [table_name])
        for row in cursor.fetchall():
            field, foreign_table, foreign_field, on_delete = row
            value = [
                re.sub(r'[^a-zA-Z0-9]', '', foreign_table.title()),
                on_delete
            ]
            if add_real_table_name:
                value.append(foreign_table)
            foreign_key_id[field] = value

    elif connection.vendor == 'postgresql':
        cursor.execute(f'''
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.delete_rule
            FROM
                information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.constraint_schema = kcu.constraint_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.constraint_schema = tc.constraint_schema
            JOIN information_schema.referential_constraints AS rc
              ON rc.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_name = %s
        ''', [table_name])
        for row in cursor.fetchall():
            field, foreign_table, foreign_field, on_delete = row
            value = [
                re.sub(r'[^a-zA-Z0-9]', '', foreign_table.title()),
                on_delete
            ]
            if add_real_table_name:
                value.append(foreign_table)
            foreign_key_id[field] = value

    else:
        raise NotImplementedError(f"Unsupported DB vendor: {connection.vendor}")

    return foreign_key_id


def get_table_foreignkey_param(table_name, add_real_table_name=0):
    """
    获取外键关系: {"user": ["User", "CASCADE", "user"]}
    """
    key_dict = get_table_foreignkey_param_using_pragma(table_name, add_real_table_name)

    # 处理字段名带 _id 的情况
    for i in list(key_dict.keys()):
        if len(i) > 3 and i.endswith('_id'):
            key_dict[i[:-3]] = key_dict.pop(i)

    # 规范化 on_delete 策略
    for k in list(key_dict.keys()):
        on_delete = key_dict[k][1]
        if on_delete == 'NO ACTION':
            key_dict[k][1] = 'DO_NOTHING'
        elif on_delete == 'SET NULL':
            key_dict[k][1] = 'SET_NULL'
        elif on_delete == 'CASCADE':
            key_dict[k][1] = 'CASCADE'

    return key_dict
