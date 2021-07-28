from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK


class AdminCreateMixin:
    serializer_class = NotImplemented
    serializer_success_msg = NotImplemented
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {"status": "ok", "message": self.serializer_success_msg}
            status = HTTP_201_CREATED
        else:
            print(serializer.errors)
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)


class AdminRetriveMixin:

    http_method_names = ["get"]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {
            field: self.kwargs[field]
            for field in self.lookup_fields
            if self.kwargs[field]
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class AdminUpdateMixin:
    serializer_class = NotImplemented
    serializer_success_msg = NotImplemented
    http_method_names = ['patch']

    def update(self, request , *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            data = {"status": "ok", "message": self.serializer_success_msg}
            status = HTTP_200_OK
        else:
            data = {"status": "error", "message": serializer.errors}
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)

class AdminDestroyMixin:
    serializer_class = None
    serializer_success_msg = NotImplemented
    http_method_names = ['delete']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {"status": "ok", "message": self.serializer_success_msg}
        status = HTTP_200_OK
        return Response(data=data, status=status)
