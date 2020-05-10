from rest_framework.pagination import PageNumberPagination


class PageNumberPaginator(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        """
        Overrides parent method to include current page number as well as
        total number of pages to more easily render pagination buttons on
        front end
        """
        response = super().get_paginated_response(data)
        response.data['current'] = self.page.number
        response.data['total'] = self.page.paginator.num_pages
        return response
