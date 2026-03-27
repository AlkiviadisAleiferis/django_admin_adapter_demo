from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class DashboardAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                "data": "simple data text",
            },
            status=status.HTTP_200_OK,
        )
