from django.urls import path

from . import views

urlpatterns = [
	path('info/<name>', views.info, name='course_info'),
	path('search', views.search, name='course_search'),
]