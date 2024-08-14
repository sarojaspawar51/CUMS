from rest_framework.pagination import PageNumberPagination
 

# class CustomLimitOffsetPagination(LimitOffsetPagination):
#     default_limit =3
#     max_limit = 100



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100 
    invalid_page_message = 'The requested page is invalid. Please try again with a different page number.'
    out_of_range_page_message = 'This page number is out of range. Please check the page number and try again.' 

