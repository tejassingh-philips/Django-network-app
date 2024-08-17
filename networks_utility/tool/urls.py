from django.urls import path 
from . import views
urlpatterns = [
    path('',views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('monitor/',views.monitor_view,name='monitor'),
    path('logout/',views.logout_view,name='logout'),
    path('get-watched-clients/', views.get_watched_clients, name='get_watched_clients'),
    path('add-client-recipient/', views.add_client_recipient, name='add_client_recipient'),
    path('delete-client-recipient/', views.delete_client_recipient, name='delete_client_recipient'),
    path('export_excel/',views.export_excel,name='export_excel')
]