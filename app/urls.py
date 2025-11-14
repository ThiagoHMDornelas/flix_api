from django.contrib import admin
from django.urls import path
from genres.views import GenreCreateListView, GenreRetrieveUpdateDestroyView #genre_create_list_view, genre_detail_view, 
from actors.views import ActorCreateListView, ActorRetrieveUpdateDestroyView
from movies.views import MovieCreateListView, MovieRetrieveUpdateDestroyView



urlpatterns = [
    path('admin/', admin.site.urls),
      
    # *** GENRE ***
    path('genres/', GenreCreateListView.as_view(), name='genre-create-list'),
    # path('genres/', genre_create_list_view, name='genre-create-list'),
    path('genres/<int:pk>/', GenreRetrieveUpdateDestroyView.as_view(), name='genre-detail-list'), 
    # path('genres/<int:pk>/', genre_detail_view, name='genre-detail-list'),   
    
    # *** ACTOR ***
    path('actors/', ActorCreateListView.as_view(), name='actor-create-list'),
    path('actors/<int:pk>/', ActorRetrieveUpdateDestroyView.as_view(), name='actor-detail-list'),
    
    # *** MOVIE *** 
    path('movies/', MovieCreateListView.as_view(), name='movie-create-list'),
    path('movies/<int:pk>', MovieRetrieveUpdateDestroyView.as_view(), name='movie-detail-list')
]
