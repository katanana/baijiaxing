from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from django.urls import reverse

from baijia.models import Baijiaxing


def index(request):
    if request.method=='GET':
     all_name=Baijiaxing.objects.all()
     names=[]
     for item in all_name:
        name=item.name
        name_url=item.name_url
        names.append(name)


    return render(request,'index.html',{'names':names})


