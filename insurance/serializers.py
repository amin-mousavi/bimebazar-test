from pyexpat import model
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Insurance, Discount
from .models import INSURANCE_TYPE


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')

class DiscountSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices = INSURANCE_TYPE)
    class Meta:
        model = Discount
        fields = ('type',)

class DiscountSerializerForGet(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices = INSURANCE_TYPE)
    user = UserSerializer()
    class Meta:
        model = Discount
        exclude = ('id', )

# class InsuranceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Insurance
#         fields = '__all__'