from django.urls import path

from . import views

app_name = "things"

urlpatterns = [
    path("things/", views.ThingList.as_view(), name="list"),
    path("things/create/", views.ThingCreate.as_view(), name="create"),
    path("things/retrieve/<str:pk>/", views.ThingRetrieve.as_view(), name="retrieve"),
    path("things/update/<str:pk>/", views.ThingUpdate.as_view(), name="update"),
    path("things/delete/<str:pk>/", views.ThingDelete.as_view(), name="delete"),
]
