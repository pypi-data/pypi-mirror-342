from django.db import models
from .model_field import JSONField, CodeField


# Create your models here.


class RouteExec(models.Model):
    table_name = models.TextField(blank=True, null=True,
                                  help_text='the table name. eg: danwei. ONLY needed if inspected_from_db=1')
    inspected_from_db = models.IntegerField(blank=True, null=True, help_text='是否需要将库中表导入为django的model。1，0. eg: 0 ')
    is_managed = models.TextField(blank=True, null=True,
                                  help_text='导出数据的managed属性. True或False。只有在inspected_from_db=1时才有效')

    route = models.TextField(blank=True, null=True, help_text='the route name. eg: /Danwei')
    table_big_name = models.TextField(blank=True, null=True, help_text='the model name of a table. eg: Danwei')
    ordering_fields = JSONField(blank=True, null=True, help_text='可用排序字段，数组，每个项是字符串. eg:["id", "name"]')
    ordering = JSONField(blank=True, null=True, help_text='默认排序字段，数组，每个项是字符串. eg:["id", "name"]')

    import_py_code = models.TextField(blank=True, null=True,
                                      help_text='needed if the model need to import from somewhere else. eg:from django.auth import User')
    foreign_key_ro = JSONField(blank=True, null=True, help_text='外键关联的只读内容. eg: {"article_name":"article.name"}')
    no_need_login = models.IntegerField(blank=True, null=True, help_text='访问是否需要登陆。1，0. eg: 0 ')
    search_fields = JSONField(blank=True, null=True, help_text='可用排序字段，数组，每个项是字符串. eg: ["name", "zhujima"]')

    model_object_list = JSONField(blank=True, null=True, help_text='可显示字段. eg: ["id", "name", "daima"]')

    filter_keys = JSONField(blank=True, null=True,
                            help_text='过滤项. eg: [{"filter_name": "name", "field_name": "name", "filter_type": "text", "lookup_expr": "icontains"}]')
    foreign_slug_kf = JSONField(blank=True, null=True,
                                help_text='一对多外键关联的字段列表. eg: {"StatKucun_wuliao": ["kucun", "jinjia"]}')

    foreign_key_id = JSONField(blank=True, null=True,
                               help_text='此属性只读，无需修改。 外键定义.关联删除属性：')
    params = JSONField(blank=True, null=True, help_text='AUTO-GENERATED FIELD. DO NOT EDIT THIS MANUALLY.')
    desc = models.TextField(blank=True, null=True, help_text="表功能描述. eg: this is the rest description")

    class Meta:
        managed = True
        verbose_name_plural = 'REST接口列表'
        db_table = 'rest_admin_table_crud'


class ComputedField(models.Model):
    route_exec = models.ForeignKey(RouteExec, on_delete=models.CASCADE)
    func_text = CodeField(blank=True, null=True, help_text="py函数.eg: def jine(self):return 0")

    class Meta:
        managed = True
        verbose_name_plural = '计算函数字段'
        db_table = 'rest_admin_table_crud_computed_field'

class DbTableToRest(models.Model):
    table_name = models.TextField(blank=True, null=True,
                                  help_text='表名')
    in_app_name = models.TextField(blank=True, null=True,
                                  help_text='表所在的app')
    model_name = models.TextField(blank=True, null=True,
                                  help_text='表的model名')
    has_api = models.IntegerField(blank=True, null=True, help_text='是否已经生成了api')

    t_type = models.TextField(blank=True, null=True,
                                  help_text='table/view')

    class Meta:
        managed = True
        verbose_name_plural = 'table列表'
        db_table = 'rest_admin_table_crud_to_rest'
