from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django_admin_adapter.adapter import AdminAPIAdapter

from .file_access import local_media_access
from .views import DashboardAPIView

admin_adapter = AdminAPIAdapter(
    admin.site,
    extra_views={"dashboard": ("dashboard/", DashboardAPIView, None)},
    sidebar_registry=[
        {
            "type": "view",
            "label": "Dashboard",
            "client_view_path": "/",
            "icon": "fa-solid fa-chart-line",
            "view_name": "dashboard",
        },
        {
            "type": "model",
            "label": "Permissions",
            "icon": "fa-solid fa-lock",
            "app_name": "auth",
            "model_name": "permission",
        },
        {
            "type": "model",
            "label": "Groups",
            "icon": "fa-solid fa-users",
            "app_name": "auth",
            "model_name": "group",
        },
        {
            "type": "model",
            "label": "Users",
            "icon": "fa-regular fa-user",
            "app_name": "organization",
            "model_name": "user",
        },
        {
            "type": "dropdown",
            "label": "Real Estate",
            "dropdown_entries": [
                {
                    "type": "model",
                    "label": "Projects",
                    "icon": "fa-solid fa-bars-progress",
                    "app_name": "real_estate",
                    "model_name": "project",
                },
                {
                    "type": "model",
                    "label": "Properties",
                    "icon": "fa-regular fa-house",
                    "app_name": "real_estate",
                    "model_name": "property",
                },
                {
                    "type": "model",
                    "label": "Agreements",
                    "icon": "fa-regular fa-handshake",
                    "app_name": "real_estate",
                    "model_name": "agreement",
                },
            ],
        },
        {
            "type": "dropdown",
            "label": "CRM",
            "dropdown_entries": [
                {
                    "type": "model",
                    "label": "Contacts",
                    "icon": "fa-regular fa-address-book",
                    "app_name": "common",
                    "model_name": "contact",
                },
                {
                    "type": "model",
                    "label": "Emails",
                    "icon": "fa-solid fa-at",
                    "app_name": "common",
                    "model_name": "email",
                },
            ],
        },
    ],
)


urlpatterns = [
    path(
        "media/<str:model_name>/<str:pk>/<str:filename>/",
        # always local media access for serving files
        # even with STPS storage, NGINX takes SAMBA mounted dir
        # as media root
        local_media_access,
        name="media",
    ),
    path("api/", include(admin_adapter.get_urls())),
]

if settings.DEBUG:
    urlpatterns.insert(0, path("profiling/", include("silk.urls", namespace="silk")))
