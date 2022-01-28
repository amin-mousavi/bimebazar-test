from random import choices, choice
from string import ascii_letters
from django.db.models import Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsSuperUser

from .models import Discount, Insurance
from .serializers import (
        DiscountSerializer,
        DiscountSerializerForGet,
        DiscountSuperUserSerializer,
    )

def generate_third_discount():
    third_discounts = [100000, 200000, 1000000]
    tmp = choices(third_discounts, weights=(15, 30, 30), k=1).pop()
    return tmp

def generate_body_discount():
    third_discounts = [500000, 60000, 200000]
    tmp = choices(third_discounts, weights=(15, 45, 40), k=1).pop()
    return tmp

def discount_code():
    letters = ascii_letters
    random_code = ''.join(choice(letters) for i in range(7))
    return random_code


class DiscountView(APIView):

    serializer_class = DiscountSerializer
    serializer_class_get = DiscountSerializerForGet

    def get(self, request, format=None):
        check_exist = Discount.objects.filter(user=request.user)
        if check_exist.exists():
            test = self.serializer_class_get(check_exist, many=True)
            return Response({'discount':test.data}, status=status.HTTP_200_OK)
            
        else:
            return Response({'message':'تخفیفی برای شما ایجاد نشده است'})
        
        return Response({'method':'GET'})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            insurance_type = serializer.validated_data.get('type')
            ### exception
            insurance_test = Insurance.objects.get(type=insurance_type)
            discount_amount = 0
            if insurance_type == 'Third':
                discount_amount = generate_third_discount()

            else:
                discount_amount = generate_body_discount()

            check_exist = Discount.objects.filter(type=insurance_test, user=request.user)
            if check_exist.exists():
                test = self.serializer_class_get(check_exist, many=True)
                response_message = {
                    'message':'شما قبلا یک تخفیف برای این نوع بیمه گرفته اید',
                    'discount': test.data,
                }
                return Response(response_message)
            generated_code = discount_code()
            
            discount_test = Discount.objects.create(
                user = request.user,
                type = insurance_test,
                amount = discount_amount,
                code = generated_code
            )

            test = self.serializer_class_get(discount_test)
            return Response({'discount': test.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ListDiscountForSuperUser(APIView):

    serializer_class = DiscountSuperUserSerializer
    serializer_class_get = DiscountSerializerForGet
    permission_classes = (IsSuperUser,)

    def get(self, request, format=None):
        return Response({'method':'get'})
        

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            date = serializer.validated_data.get('date')
            insurance_type = serializer.validated_data.get('type')
            insurance_test = Insurance.objects.get(type=insurance_type)

            objects = Discount.objects.filter(created_date__hour = date.hour, type=insurance_test)
            total = objects.aggregate(Sum('amount'))
            serialize_object = self.serializer_class_get(objects, many=True)
            return Response({
                'total': total,
                'discounts': serialize_object.data,
                
            })
        
        else:
            return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )