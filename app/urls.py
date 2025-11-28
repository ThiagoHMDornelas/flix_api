from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # *** AUTENTICAÇO ***
    path('api/v1/', include('authentication.urls')),    
    # *** GENRE ***
    path('api/v1/', include('genres.urls')),    
    # *** ACTOR ***
    path('api/v1/', include('actors.urls')),    
    # *** MOVIE *** 
    path('api/v1/', include('movies.urls')),
    # *** REVIEW ***
    path('api/v1/', include('reviews.urls')),
]
