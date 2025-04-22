__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import routers
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filter
import django_filters
import django_filters.rest_framework


'''
    封装 对表的增删改查 rest_api
'''



# curr_view = my_rest_apiB(PickNumber, 'PickNumber', ["id", 'team_name', 'pick_number', 'team'], {'team_name':'team.name'}, {'team':Team})
def my_rest_viewsetB(model_object,model_class_name, model_obj_list='__all__', foreign_key_ro={}, foreign_key_id={}, filter_fieldsA=(),
                     no_need_login = False, optional_fields1=[], search_fieldsA=[], orderingA=[], ordering_fieldsA=[], filter_keys=[], foreign_slug_kf={}):
    """

    :param model_object: django的数据模型
    :param model_class_name:数据模型的名称，用于生成代码名称，一般是model_object的字符串
    :param model_obj_list: 可查看的字段列表['id','name']. 可以是 '__all__'代表所有字段
    :param foreign_key_ro:只读外键内容：{'team_name': 'team.name', }
    :param foreign_key_id: 只读外键类型{'team':Team}
    :param filter_fields: 可搜索字段 ['id','team','name']
    :param no_need_login: 是否需要登录认证
    :param optional_fields1: 字段是否是可选，用于数据库写入设置
    :return:
    """
    if filter_keys is None:
        filter_keys=[]
    if (foreign_key_ro is not None) and (len(foreign_key_ro)>0) and (model_obj_list is not None) and (model_obj_list!='__all__'):
        for i in foreign_key_ro:
            if i not in model_obj_list:
                model_obj_list.append(i)
    if (foreign_key_id is not None) and (len(foreign_key_id) > 0) and (model_obj_list is not None) and (
            model_obj_list != '__all__'):
        for i in foreign_key_id:
            if i not in model_obj_list:
                model_obj_list.append(i)

    def add_foreign_serializer(ModName, fields_list):
        class TrackSerializer(serializers.ModelSerializer):
            class Meta:
                model = globals()[ModName]
                fields = fields_list

        TrackSerializer.__name__=ModName+"_in_"+model_class_name
        return TrackSerializer

    def AddVarFunc(self, foreign_key_ro, foreign_key_id, foreign_slug_kf):
        if foreign_key_ro is not None:
            for i in foreign_key_ro:
                #setattr(self, i, serializers.CharField(source=foreign_key_ro[i], read_only=True))
                self[i]=serializers.CharField(source=foreign_key_ro[i], read_only=True)
        if foreign_key_id is not None:
            for i in foreign_key_id:
                #setattr(self, i,
                #        serializers.PrimaryKeyRelatedField(queryset=foreign_key_id[i].objects.all(), read_only=False))
                self[i]=serializers.PrimaryKeyRelatedField(queryset=foreign_key_id[i].objects.all(), read_only=False, required=False, allow_null=True)

        if foreign_slug_kf is not None:
            for i in foreign_slug_kf:
                self[i] = add_foreign_serializer(i.split('_')[0], foreign_slug_kf[i])(many=True, read_only=True)
                #self[i] = serializers.SlugRelatedField( many=True,
                #                        read_only=True,
                #                        slug_field=foreign_slug_kf[i])

        return 'A'

    class TeamPickNumberSerializer(serializers.ModelSerializer):
        useless_cc = AddVarFunc(locals(), foreign_key_ro, foreign_key_id, foreign_slug_kf)

        #team_name = serializers.CharField(source='team.name', read_only=True)  # team_name 用于页面显示文字
        #team = serializers.PrimaryKeyRelatedField(queryset=model_object.objects.all(), read_only=False)  # team_id  用于修改数据库
        class Meta:
            model = model_object
            fields = model_obj_list
            #fields = '__all__'
            extra_kwargs = {i: {"required": False, "allow_null": True} for i in optional_fields1}

    class GoodsFilter(django_filters.rest_framework.FilterSet):
        for i in filter_keys:
            if ('filter_type' not in i) or ('filter_name' not in i) or ('field_name' not in i) or (
                    'lookup_expr' not in i):
                print('WARN:filter no type will not effect', i, model_class_name)
                continue
            if i['filter_type'] == 'number':
                locals()[i['filter_name']] = django_filters.NumberFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'text':
                locals()[i['filter_name']] = django_filters.CharFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'bool':
                locals()[i['filter_name']] = django_filters.BooleanFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'date_range':
                locals()[i['filter_name']] = django_filters.DateFromToRangeFilter(field_name=i['field_name'], lookup_expr='range')
            elif i['filter_type'] == 'time_range':
                locals()[i['filter_name']] = django_filters.TimeRangeFilter(field_name=i['field_name'],
                                                                              lookup_expr='range')
            elif i['filter_type'] == 'date':
                locals()[i['filter_name']] = django_filters.DateFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'time':
                locals()[i['filter_name']] = django_filters.TimeFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'datetime':
                locals()[i['filter_name']] = django_filters.DateTimeFilter(field_name=i['field_name'], lookup_expr=i['lookup_expr'])
            elif i['filter_type'] == 'isodatetime':
                locals()[i['filter_name']] = django_filters.IsoDateTimeFilter(field_name=i['field_name'],
                                                                       lookup_expr=i['lookup_expr'])
            else:
                print('WARN: unknown filter type:', i['filter_type'], model_class_name, i)

        class Meta:
            model = model_object
            fields = [fk1['filter_name'] for fk1 in filter_keys]

    GoodsFilter.__name__= model_class_name+'SFilter'


    class TeamPickNumberView(viewsets.ModelViewSet):
        filterset_class = GoodsFilter
        #filter_fields = filter_fieldsA

        queryset = model_object.objects.all()
        serializer_class = TeamPickNumberSerializer
        filter_backends = [django_filters.rest_framework.DjangoFilterBackend,rest_framework_filter.SearchFilter, rest_framework_filter.OrderingFilter]#,rest_framework_filter.SearchFilter, rest_framework_filter.OrderingFilter)
        search_fields = search_fieldsA
        ordering = orderingA
        ordering_fields = ordering_fieldsA

    if no_need_login:
        # print('no_need_login for:', model_class_name)
        TeamPickNumberView.authentication_classes = ()
        TeamPickNumberView.permission_classes = ()
    TeamPickNumberView.__name__= model_class_name+'View'
    TeamPickNumberSerializer.__name__ = model_class_name+'Serial'
    return TeamPickNumberView




from rest_framework.renderers import JSONRenderer
class EmberJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'status':0,'msg':'',  'data':{ 'items': data}}
        return super(EmberJSONRenderer, self).render(data, accepted_media_type, renderer_context)




