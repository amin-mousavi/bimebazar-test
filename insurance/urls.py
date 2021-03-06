from django.urls import path
from .views import DiscountView, ListDiscountForSuperUser

urlpatterns = [
    path('v1/discount/', DiscountView.as_view(), name='discount_list'),
    path('v1/discount/superuser/', ListDiscountForSuperUser.as_view(), name='superuser_discount_list'),

]