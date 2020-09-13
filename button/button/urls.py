"""button URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Button API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.button.com/policies/terms/",
#         contact=openapi.Contact(email="contact@button.local"),
#         license=openapi.License(name="Test License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('button_api.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('swagger/', schema_view.with_ui('swagger',
    #                                      cache_timeout=0), name='schema-swagger-ui'),
    # path('^redoc/', schema_view.with_ui('redoc',
    #                                     cache_timeout=0), name='schema-redoc'),

    # path('api/password_reset/',
    #      include('django_rest_passwordreset.urls', namespace='password_reset')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
