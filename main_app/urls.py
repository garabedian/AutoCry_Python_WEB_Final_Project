from django.urls import path
from main_app.views import list_items, details_or_comment_item, like_item, edit_item, delete_item, create_item, \
    landing_page

urlpatterns = [
    path('', landing_page, name='landing'),
    path('item/', list_items, name='list items'),
    path('item/details/<int:pk>/', details_or_comment_item, name='item details or comment'),
    path('item/like/<int:pk>/', like_item, name='like item'),
    path('item/edit/<int:pk>/', edit_item, name='edit item'),
    path('item/delete/<int:pk>/', delete_item, name='delete item'),
    path('item/create/', create_item, name='create item'),
]
