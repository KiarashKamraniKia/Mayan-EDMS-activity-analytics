from django.urls import include, path, re_path

from .views import MayanOIDCAuthenticationCallbackView

passthru_urlpatterns = [
    re_path(
        r'^oidc/', include('mozilla_django_oidc.urls')
    )
]

urlpatterns = [
    path(
        'oidc/callback/', MayanOIDCAuthenticationCallbackView.as_view(),
        name='oidc_authentication_callback'
    )
]
