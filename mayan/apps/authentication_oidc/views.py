from django.shortcuts import resolve_url

from mozilla_django_oidc.views import OIDCAuthenticationCallbackView


class MayanOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    @property
    def success_url(self):
        next_url = self.request.session.get('oidc_login_next', None)
        return next_url or resolve_url(
            self.get_settings('LOGIN_REDIRECT_URL', '/')
        )
