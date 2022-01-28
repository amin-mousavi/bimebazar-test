from django.urls import path
from .views import DiscountView

urlpatterns = [
    # path('v1/insurance/', InsuranceView.as_view(), name='insurance_list'),
    path('v1/discount/', DiscountView.as_view(), name='discount_list'),
]
