from django.urls import path
from . import views

urlpatterns = [
    path('', views.grid_editor_view, name='grid-editor'),
    path('getdata/', views.getdata, name="getdata"),
    path('api/led-status/', views.update_status, name='update-led-status'),
    path('display/', views.status_display, name='display-status'),
    path("esp32/command/", views.esp32_command, name='set-command'),
    path("esp32/set-blink/", views.set_command, name='set-blink'),
]