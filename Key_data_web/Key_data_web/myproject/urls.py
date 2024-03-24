"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin


from django.urls import path
from myapp import views

# 根据不同的url地址，映射到不同的views中的处理函数
urlpatterns = [
    path('', views.get_start_w1, name='get_start_w1'),
    path('start1/', views.get_start_w1, name='get_start_w1'),
    path('start2/', views.get_start_w2, name='get_start_w2'),
    path('start3/', views.get_start_w3, name='get_start_w3'),
    path('w1_rep/', views.w1_rep, name='w1_rep'),
    path('w2_rep/', views.w2_rep, name='w2_rep'),
    path('w3_rep/', views.w3_rep, name='w3_rep'),
    path('attack/', views.w_attack, name='w_attack'),
    path('finished/', views.finished_web, name='finished_web'),
]

