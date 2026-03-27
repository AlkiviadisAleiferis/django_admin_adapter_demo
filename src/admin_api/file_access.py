from django.apps import apps
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

DEFAULT_ADMIN_SITE = admin.site

models_registry = {model._meta.model_name: model for model in apps.get_models()}


class AdminFilePermissionResolver:
    """
    Class for checking the view permissions of an object
    through the admin's process, and the get_queryset/object flow.
    """

    permission_error_class = PermissionDenied

    def __init__(
        self, request, model_name=None, pk=None, admin_site=DEFAULT_ADMIN_SITE
    ):
        if not admin_site.has_permission(request):
            raise self.permission_error_class()

        self.request = request

        # get model
        model = models_registry.get(model_name)

        if model is None:
            raise self.permission_error_class()
        else:
            self.model = model

        # get model admin
        model_admin = admin.site._registry.get(model)

        if model_admin is None:
            raise self.permission_error_class()
        else:
            self.model_admin = model_admin

        if not model_admin.has_view_or_change_permission(request, None):
            raise self.permission_error_class()

        if pk is None:
            raise self.permission_error_class()

        self.object_pk = pk

    def check_object_access(self):
        # if 'none' then dont check object reachability
        if self.object_pk == "none":
            return

        pk = int(self.object_pk) if self.object_pk.isdigit() else self.object_pk
        obj = self.model_admin.get_object(self.request, pk)

        if obj is None:
            raise self.permission_error_class()

        elif not self.model_admin.has_view_permission(self.request, obj):
            raise self.permission_error_class()


def local_media_access(request, model_name, pk, filename):
    """
    When trying to access :
    ``myproject.com/media/...``
    If access is authorized, the `request` will be redirected to
    myproject.com/serve-media/...
    This special URL will be handled by nginx
    with the help of X-Accel-Redirect header
    """
    if request.method != "GET":
        raise PermissionDenied()

    perm_resolver = AdminFilePermissionResolver(request, model_name, pk)
    perm_resolver.check_object_access()

    response = HttpResponse()
    # Content-type will be detected by nginx
    del response["Content-Type"]
    response["X-Accel-Redirect"] = "/serve-media/" + f"{model_name}/{pk}/{filename}"
    return response
