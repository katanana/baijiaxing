from django.conf.urls import url,include

from baijia import views

urlpatterns = [

    url('^index/',views.index,name='index')
   ]