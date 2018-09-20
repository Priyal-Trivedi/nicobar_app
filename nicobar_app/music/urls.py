from django.conf.urls import url
from .views import ListSongsView, SongsDetail


urlpatterns = [
    url('songs/', ListSongsView.as_view(), name="songs-all"),
    url('songs/<int:pk>/', SongsDetail.as_view(), name="songs-detail"),
]