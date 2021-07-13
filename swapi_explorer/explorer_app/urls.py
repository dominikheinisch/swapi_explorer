from django.urls import path

from .views import FileView, IndexView, CountView


app_name = 'explorer_app'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('file/<str:filename>', FileView.as_view(), name='file'),
    path('file/<str:filename>/count', CountView.as_view(), name='count'),
]
