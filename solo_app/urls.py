from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('new', views.new),
    path('create', views.create),
    path('go_to/<int:group_id>', views.group),
    path('favorite/<int:group_id>', views.joinGroup),
    path('process_message/<int:group_id>', views.post_mess),
    path('user/<int:user_id>', views.user_profile),
    path('create_testimony/<int:user_id>', views.create_testimony)
]