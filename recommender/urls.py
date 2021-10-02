from django.urls import path

from .views import home, animeRecommend

app_name = 'recommender'
urlpatterns = [
    path('',home,name='home'),
    path('an-recommend/',animeRecommend,name='an-recommend'),
]

