from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('', views.index, name="index")
    # path('', views.Youtube.as_view())
    path('', views.PersonView.as_view()),
    path('add/', views.PersonCreateListApi.as_view()),
    path('person/<int:id>/destroy', views.PersonViewRetrieveUpdateDestroy.as_view()),
    path('stats/', views.PersonDummyViews.as_view()),
]
