from rest_framework.pagination import PageNumberPagination


class PageNumberPaginator(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current'] = self.page.number
        response.data['total'] = self.page.paginator.num_pages
        return response
