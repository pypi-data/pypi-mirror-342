# django_rest_admin_plus
在django_rest_admin的基础上，解决外键仅支持sqlite3的问题，兼容mysql和postgresql

Adding table CRUD rest api with admin ui and without coding.

requirements:

1. django
2. djangorestframework
3. django-filter


install:

1. pip install django_rest_admin
2. add django app:
   in django project setttings.py file:
   INSTALLED_APPS list, add:
```
    'rest_framework',
    'django_filters',
    'django_rest_admin',
```

3. start restapi app(the app name can change by user):

```
 python manage.py startapp myRestApiApp
```
  add myRestApiApp to INSTALLED_APPS:

```
    'myRestApiApp',
``` 
4 setings.py set apiapp
write below in settings.py:

add this line in settings.py

```
DJANGO_REST_ADMIN_TO_APP='myRestApiApp'
```


5. create admin user using command:
```python manage.py createsuperuser```

6. start project using:

``` python manage.py runserver 0.0.0.0:8000 ```

7. login to /admin/
   in django_rest_admin --REST接口列表 --click button --生成RestAPI
    
8. add urls:

```
from django.urls import include
urlpatterns=[
path('api/', include ('myRestApiApp.urls')), #<<--add this line in the list

]
```

9. finished!



use:
1. add table in your db:
  this could be down in navicat or some other db editors.
  of course you could coding in django,too.
  
2. open admin page: http://127.0.0.1/admin/

	![admin-page](doc/admin_page.png)

   after login, their should be a table:Table-REST-CRUD.
   press Add. 
   
   the option MUST be filled:
   
   ```
   A. route: the route name. eg: /Danwei
   B. Table big name: the model name of a table. eg: Danwei
   C. Table name: the table name. eg: danwei. ONLY needed if inspected_from_db=1
   D. Inspected from db: set to 1 if table is just from db, not from django model. otherwise set to 0.
   ```
   
   press Save
   
3. press RefreshRestAPI BUTTON in the list.
4. the django project will restart automaticly if you use debug mode.
    and then the rest api is generated already.
	press OpenApi button to test the api.
	
	![admin-page](doc/rest_test_page.png)
   

   







