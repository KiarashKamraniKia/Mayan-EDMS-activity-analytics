from django.urls import re_path

from .views import (
    ServiceWorkerGatewayErrorView, ServiceWorkerScriptView
)

urlpatterns = [
    re_path(
        route=r'^service_worker\.js$', name='service_worker_script',
        view=ServiceWorkerScriptView.as_view()
    ),
    re_path(
        route=r'^service_worker_gateway_error\.html$',
        name='service_worker_gateway_error',
        view=ServiceWorkerGatewayErrorView.as_view()
    )
]
