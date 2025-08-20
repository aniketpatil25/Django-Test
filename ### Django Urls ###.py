### Django Urls ###

from django.urls import path
from .views import ClientRegister, ClientList, ClientDetail, ProjectAdd, MyProjects

urlpatterns = [
    path("clients/register/", ClientRegister.as_view()),
    path("clients/", ClientList.as_view()),
    path("clients/<int:client_id>/", ClientDetail.as_view()),
    path("clients/<int:client_id>/projects/", ProjectAdd.as_view()),
    path("my-projects/", MyProjects.as_view()),
]
