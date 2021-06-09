"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls



urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('api.urls', namespace="api")),
    path('account/', include('account.urls', namespace="account")),
    path('cart/', include('cart.urls', namespace="cart")),
    path('blog/', include('blog.urls', namespace="blog")),

    # Documentation and Schema
    path('openapi', get_schema_view(
        title="Corecare API",
        description="Documentation for Corecare API",
        version="1.0.0"
    ), name='openapi-schema'),
    path('', include_docs_urls(title="Corecare API"))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
