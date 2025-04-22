from  django.contrib import messages
from django.contrib import admin
from .models import RouteExec,ComputedField,DbTableToRest
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, include
from django.http import HttpResponse,HttpResponseRedirect

from .update_models import update_models
from .json_widget import JsonEditorWidget, CodeEditorWidget
from .model_field import JSONField, CodeField
from .update_rest import update_rest
from .get_app_url_base import get_app_url_base
from .set_table_default_value import set_table_default_value
from .update_table_list import update_table_list

# Register your models here.


class ComputedFieldAdmin(admin.TabularInline):
    model = ComputedField


class DbTableToRestAdmin(admin.ModelAdmin):
    change_list_template = "html/table_to_rest_list.html"

    actions = ["selected_table_to_api"]

    def selected_table_to_api(self, request, queryset):
        for i in queryset:
            table_rcd_id = i.id
            self.add_table_to_api(request, table_rcd_id)
        return
    selected_table_to_api.short_description ='添加api'


    def update_table_action(self, request):
        message_to_show = update_table_list(request)
        self.message_user(request, message_to_show)
        return HttpResponseRedirect("../")

    def add_table_to_api(self,request, id):
        rex = RouteExec()
        rex.table_name = DbTableToRest.objects.get(id=id).table_name
        rex.save()
        message_to_show = set_table_default_value(rex)
        self.message_user(request, message_to_show)

        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_table/', self.update_table_action),
            path('add_table_api/<int:id>/', self.add_table_to_api),
        ]
        return my_urls + urls

    def button2_link(self, obj):
        button_html = """<a class="changelink" href=add_table_api/%d/>添加api</a>""" % (obj.id)
        return format_html(button_html)

    button2_link.short_description = "添加此表为api"

    list_display = ['id', 'table_name','in_app_name',  'model_name', 'has_api', 't_type', 'button2_link']
    formfield_overrides = {
            JSONField: {'widget': JsonEditorWidget},
            CodeField: {'widget': CodeEditorWidget},
        }

    class Media:
        css = {
            'all': ( 'django_rest_admin/jsoneditor.css',)
        }
        js = ('django_rest_admin/jsoneditor.js', 'django_rest_admin/jquery-3.6.0.min.js')





class RouteExecAdmin(admin.ModelAdmin):
    inlines = [ComputedFieldAdmin, ]
    change_list_template = "html/auto_refresh_list.html"

    def update_rest_action(self, request):
        message_to_show = update_rest(request)
        if message_to_show=='ok':
            self.message_user(request, message_to_show, level=messages.INFO)
        else:
            self.message_user(request, message_to_show, level=messages.WARNING)
        return HttpResponseRedirect("../")

    def set_table_default(self, request, id):
        #message_to_show = update_rest(request)
        message_to_show = set_table_default_value(RouteExec.objects.get(id=id))
        self.message_user(request, message_to_show)
        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_rest/', self.update_rest_action),
            path('set_table_default/<int:id>/', self.set_table_default),
        ]
        return my_urls + urls

    def button_link(self, obj):
        try:
            app_base = get_app_url_base()
            button_html = """<a class="changelink" href=""" + app_base + """%s/>打开</a>""" % (obj.route)
        except Exception as e:
            from django.conf import settings
            if hasattr(settings,'DJANGO_REST_ADMIN_TO_APP'):
                button_html = '<a class="changelink" />请设置%s.urls到项目urls.py中,然后点击 生成RestAPI</a>'%settings.DJANGO_REST_ADMIN_TO_APP
            else:
                button_html = '<a class="changelink" />请设置settings.DJANGO_REST_ADMIN_TO_APP</a>'
        return format_html(button_html)

    button_link.short_description = "打开"

    def button2_link(self, obj):
        button_html = """<a class="changelink" href=set_table_default/%d/>填充</a>""" % (obj.id)
        return format_html(button_html)

    button2_link.short_description = "自动填充空项"

    list_display = ['id', 'route', 'table_name', 'button2_link',  'button_link']
    formfield_overrides = {
            JSONField: {'widget': JsonEditorWidget},
            CodeField: {'widget': CodeEditorWidget},
        }

    class Media:
        css = {
            'all': ( 'django_rest_admin/jsoneditor.css',)
        }
        js = ('django_rest_admin/jsoneditor.js', 'django_rest_admin/jquery-3.6.0.min.js')


admin.site.register(DbTableToRest, DbTableToRestAdmin)
admin.site.register(RouteExec, RouteExecAdmin)

