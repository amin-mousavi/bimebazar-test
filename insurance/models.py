from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model


INSURANCE_TYPE = (
    ('Third', 'ثالث'),
    ('Body','بدنه'),
)
class Insurance(models.Model):

    type = models.CharField(max_length=25, choices=INSURANCE_TYPE)

    def __str__(self):
        return self.type

class Discount(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.ForeignKey('Insurance', on_delete=models.CASCADE, related_name='insurances')
    amount = models.PositiveBigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.user}-{self.type}'
