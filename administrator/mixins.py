from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.response import Response


class AdminCreateMixin:
    serializer_class = NotImplemented
    serializer_success_msg = NotImplemented
    http_method_names = ['post']

    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {
                "status": "ok",
                "message": self.serializer_success_msg
            }
            status = HTTP_201_CREATED
        else:
            print(serializer.errors)
            data = {
                "status": "error",
                "message": serializer.errors
            }
            status = HTTP_406_NOT_ACCEPTABLE
        return Response(data=data, status=status)



