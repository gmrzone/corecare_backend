from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostListPagination(PageNumberPagination):
    def get_page_size(self, request):
        size = request.query_params.get("size")
        if size:
            return size
        return super().get_page_size(request)

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        post_count = self.page.paginator.count
        page_count = (int(post_count) // int(page_size)).__ceil__()
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "post_count": post_count,
                "page_count": page_count,
                "posts": data,
            }
        )
