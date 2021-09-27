from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointments, name='appointments'),
    path('add', views.add_appointment, name='add_appo'),
    path('new_appo', views.new_appo, name='new_appo'),
    path('<int:appo_id>/delete', views.del_appo, name='delete_appo'),
    path('<int:appo_id>/edit', views.edit_appo, name='edit_appo'),
    path('<int:appo_id>/upd_appo', views.upd_appo, name='upd_appo'),
]