from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from account.serializers import AccountSerializer

from database.models import UserDatas

class AccountViewSet(ModelViewSet):
    queryset = UserDatas.objects.all()
    serializer_class = AccountSerializer

