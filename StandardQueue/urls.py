from django.urls import path
from StandardQueue.views import *

urlpatterns = [
    path('', index, name='index'),
    path('create-queue/', create_queue, name='create_queue'),
    path('delete-queue/', delete_queue, name='delete_queue'),
    path('join-the-queue/<str:name>/', join_the_queue, name='join_the_queue'),
    path('leave-the-queue/<str:name>/', leave_the_queue, name='leave_the_queue')
]
