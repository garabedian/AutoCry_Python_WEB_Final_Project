from django.urls import path
from main_app.views import list_items, details_or_comment_item, like_item, edit_item, delete_item, create_item, \
    landing_page, contact_us, ListItemsView, DeleteItemView, ListItemsRestView, DetailItemRestView

urlpatterns = [
    path('', landing_page, name='landing'),
    # path('item/', list_items, name='list items'),                                  # FBV
    path('item/', ListItemsView.as_view(), name='list items'),                     # CBV
    path('item/details/<int:pk>/', details_or_comment_item, name='item details or comment'),
    path('item/api/', ListItemsRestView.as_view()),                                # REST
    path('item/api/<int:pk>/', DetailItemRestView.as_view()),                      # REST
    # slug is use for custom path building through ASCII strings (no matter in this case)
    # path('item/details/<int:pk>/<str:slug>/', details_or_comment_item, name='item details or comment'),
    path('item/like/<int:pk>/', like_item, name='like item'),
    path('item/edit/<int:pk>/', edit_item, name='edit item'),
    # path('item/delete/<int:pk>/', delete_item, name='delete item'),                # FBV
    path('item/delete/<int:pk>/', DeleteItemView.as_view(), name='delete item'),   # CBW
    path('item/create/', create_item, name='create item'),
    path('contact/', contact_us, name='contact us'),
]
