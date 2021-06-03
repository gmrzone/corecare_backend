from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PostListPagination(PageNumberPagination):
    def get_page_size(self, request):
        size = request.query_params.get('size')
        if size:
            return size
        return super().get_page_size(request)

    def get_paginated_response(self, data):

        return Response({
            "links": {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'post_count': self.page.paginator.count,
            'posts': data   
        })