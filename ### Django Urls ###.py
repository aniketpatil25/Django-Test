### Django Urls ###
from django.urls import path
from . import views

urlpatterns = [
    path("clients/register/", views.register_client),
    path("clients/", views.get_clients),
    path("clients/<int:client_id>/", views.update_client),
    path("clients/<int:client_id>/projects/", views.add_project),
    path("my-projects/", views.my_projects),
]
