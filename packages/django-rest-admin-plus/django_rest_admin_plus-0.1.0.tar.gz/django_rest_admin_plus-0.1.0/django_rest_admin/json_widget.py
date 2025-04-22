# coding:utf-8

__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

import json

from django.forms import Widget, widgets
from django.utils.safestring import mark_safe

widgets.TextInput

class JsonEditorWidget(Widget):

    """
    在 django  admin 后台中使用  jsoneditor 处理 JSONField

    TODO：有待改进, 这里使用 % 格式化，使用 format 会抛出 KeyError 异常
        """

    html_template = """
        <div id='%(name)s_editor_holder' style='padding-left:170px'></div>
    
        <textarea hidden readonly class="vLargeTextField" cols="40" id="id_%(name)s" name="%(name)s" rows="20">%(value)s</textarea>
    
    <style type="text/css">
    .jsoneditor-mode-code {
      height: 500px;
    }
  </style>

    
        <script type="text/javascript">
            var element = document.getElementById('%(name)s_editor_holder');
            var json_value = %(value)s;
    
            var %(name)s_editor = new JSONEditor(element, {
                onChange: function() {
                    var textarea = document.getElementById('id_%(name)s');
                    var json_changed = JSON.stringify(%(name)s_editor.get());
                    textarea.value = json_changed;
                },
                mode: 'code',
                modes: ['code', 'form', 'text', 'tree', 'view', 'preview'], // allowed modes
            });
    
            %(name)s_editor.set(json_value)
            %(name)s_editor.expandAll()
        </script>
        """


    def __init__(self, attrs=None):
        super().__init__(attrs)


    def render(self, name, value, attrs=None, renderer=None):
        #print('JsonEditorWidget render')
        if isinstance(value, str):
            value = json.loads(value)
        elif isinstance(value, dict):
            value=value

        if renderer is None:
            renderer = self.get_default_renderer()

        #return mark_safe(renderer.render(template_name, context))


        result = self.html_template % {'name': name, 'value': json.dumps(value), }
        return mark_safe(result)


class CodeEditorWidget(Widget):
    """
    在 django  admin 后台中使用  jsoneditor 处理 JSONField

    TODO：有待改进, 这里使用 % 格式化，使用 format 会抛出 KeyError 异常
        """

    html_template = """
        <div id='%(name)s_editor_holder' style='padding-left:170px'></div>

        <textarea hidden readonly class="vLargeTextField" cols="40" id="id_%(name)s" name="%(name)s" rows="20">%(value)s</textarea>

    <style type="text/css">
    .jsoneditor-mode-code {
      height: 500px;
    }
  </style>


        <script type="text/javascript">
            var element = document.getElementById('%(name)s_editor_holder');
            var json_value = %(value)s;

            var %(name)s_editor = new JSONEditor(element, {
                onChange: function() {
                    var textarea = document.getElementById('id_%(name)s');
                    var json_changed = %(name)s_editor.get();
                    textarea.value = json_changed;
                },
                mode: 'code',
                modes: ['code', 'form', 'text', 'tree', 'view', 'preview'], // allowed modes
            });

            %(name)s_editor.set(json_value)
            %(name)s_editor.expandAll()
        </script>
        """

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # print('JsonEditorWidget render')
        #value = value

        if renderer is None:
            renderer = self.get_default_renderer()

        # return mark_safe(renderer.render(template_name, context))

        result = self.html_template % {'name': name, 'value': value, }
        return mark_safe(result)
