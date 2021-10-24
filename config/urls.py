"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

from django.conf import settings

from django.views.generic import TemplateView


urlpatterns = [  # attention: use this patterns only for general paths
                 # that are used by all forks from the base-skeleton

     # ! defining Views directly in the urls.py (like the line below) is an anti-pattern. We'll keep it here for simplicity for now.
    path('', TemplateView.as_view(template_name='base.html'), {"TITLE": settings.PROJECT_TITLE}),

    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('apps.users.urls', namespace="users")),
] + [  # the project-specific urlpatterns
    path('', include('apps.things.urls', namespace="things")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # debug toolbar
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
