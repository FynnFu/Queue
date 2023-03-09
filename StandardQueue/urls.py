from django.urls import path
from StandardQueue.views import *

urlpatterns = [
    path('', index, name='index'),
    path('connection/', connection, name='connection'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('change-name/<str:user_id>/', change_name, name='change_name'),
    path('create-queue/', create_queue, name='create_queue'),
    path('delete-queue/', delete_queue, name='delete_queue'),
    path('clear-cookies/<str:name>/', clear_cookies, name='clear_cookie'),
    path('join-the-queue/<str:name>/', join_the_queue, name='join_the_queue'),
    path('hide-user/<str:move>/<str:user_id>', move_user, name='hide_user'),
]
