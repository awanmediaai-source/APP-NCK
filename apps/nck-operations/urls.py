from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings
from core import views, assistant
urlpatterns=[path('api/assistant/status',assistant.status),path('api/assistant/chat',assistant.chat),path('',views.index),path('api/login',views.signin),path('api/logout',views.signout),path('api/state',views.state),path('api/command',views.command),path('api/export',views.export),re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.BASE_DIR/'static'})]
# shortcut: static files served by Django for localhost demo; use a production server before deployment.
