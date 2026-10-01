from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    # *** DOCS ***
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # *** AUTENTICAÇÃO ***
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
