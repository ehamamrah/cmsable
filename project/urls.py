from django.contrib import admin
from django.urls import path, include
from project.settings import BASE_DIR
from pathlib import Path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def discover_app_urls():
    """Discover all app URLs in the apps directory."""
    app_urls = {}
    apps_dir = Path(BASE_DIR) / 'apps'
    
    if apps_dir.exists():
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir() and not app_dir.name.startswith('_'):
                # Check for v1/urls.py in the app directory
                v1_urls = app_dir / 'v1' / 'urls.py'
                if v1_urls.exists():
                    app_urls[app_dir.name] = f'apps.{app_dir.name}.v1.urls'
                # Check for v1/urls.py in subdirectories
                elif app_dir.is_dir():
                    for subdir in app_dir.iterdir():
                        if subdir.is_dir() and not subdir.name.startswith('_'):
                            v1_urls = subdir / 'v1' / 'urls.py'
                            if v1_urls.exists():
                                # Use just the subdirectory name for the URL pattern
                                app_urls[subdir.name] = f'apps.{app_dir.name}.{subdir.name}.v1.urls'
    
    return app_urls

# API Versioning
API_VERSIONS = {
    'v1': discover_app_urls()
}

def get_versioned_urlpatterns():
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]

    for version, apps in API_VERSIONS.items():
        version_prefix = f'api/{version}/'

        for app_name, urls_module in apps.items():
            try:
                urlpatterns.append(
                    path(f'{version_prefix}{app_name}/', include(urls_module))
                )
            except Exception as e:
                print(f"Warning: Could not load URLs for {urls_module}: {e}")
    
    return urlpatterns

urlpatterns = get_versioned_urlpatterns()