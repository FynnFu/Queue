from django.urls import path
from StandardQueue.views import *

urlpatterns = [
    path('', index, name='index'),
    path('join-the-queue/', join_the_queue, name='join_the_queue'),
    path('leave-the-queue/', leave_the_queue, name='leave_the_queue')
]