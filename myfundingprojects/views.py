from mydatabase.models import UserDatas, FundingProjects, FundingShares , SoldPrices
from myfundingprojects.serializers import FundingProjectsSerializer, FundingSharesSerializer , SoldPricesSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from myapi.response import *
from myapi.message import *


class FundingProjectsViewSet(viewsets.ModelViewSet):

    # set serializer class
    def get_serializer_class(self):
        if self.action == 'create_funding':  # For project
            return FundingProjectsSerializer
        if self.action == 'add_shares':  # For shares
            return FundingSharesSerializer
        if self.action == 'add_sold_shares':
            return SoldPricesSerializer

        return FundingProjectsSerializer

    # set queryset
    def get_queryset(self):  # added string
        return FundingProjects.objects.filter(fundraiser=UserDatas.objects.get(id=self.request.user.id))

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_funding(self, request, *args, **kwargs):
        data = request.data

        try:
            new_funding = FundingProjects.objects.create(
                fundraiser=UserDatas.objects.get(id=self.request.user.id),
                nftId=data['nftId'],
                nftContractAddress=data['nftContractAddress'],
                nftName=data['nftName'],
                startTime=data['startTime'],
                endTime=data['endTime'],
                token=data['token'],
                buyPrice=data['buyPrice'],
                sellPrice=data['sellPrice'],
                gasPrice=data['gasPrice'])
            new_funding.save()
            return success()
        except Exception as e:
            print(e)
            return err(Msg.Err.FundingProject.create)

    def get_queryset(self):  # added string
        return FundingProjects.objects.filter(fundingshares__userData_id=UserDatas.objects.get(id=self.request.user.id))

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def add_shares(self, request, *args, **kwargs):
        data = request.data
        projectid = data['fundingProject']
        share = data['share']
        try:
            new_shares = FundingShares.objects.create(
                userData_id=UserDatas.objects.get(id=self.request.user.id).id,
                fundingProject_id=projectid,
                share=share
            )
            new_shares.save()
            return success()
        except Exception as e:
            print(e)
            return err(Msg.Err.Shares.create)

    
    def get_queryset(self):  # added string
        return FundingShares.objects.filter(userData_id=UserDatas.objects.get(id=self.request.user.id))

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def add_sold_shares(self, request, *args, **kwargs):
        data = request.data
        user_id = self.request.user.id


        fundingShares_id = data['fundingShares']
        price = data['price']

        

        try:
            
            
            new_soldPrices = SoldPrices.objects.create(
            fundingShares_id=fundingShares_id,
            price=price
            )
            
            new_soldPrices.save()
            return success()


        except Exception as e:
            print(e)
            return err(Msg.Err.Shares.create)




    @action(detail=False, permission_classes=[IsAuthenticated])
    def find_shares(self, request):
        data = request.query_params

    @action(detail=False, permission_classes=[IsAuthenticated])
    def add_evaluation(self, request):
        data = request.query_params

    @action(detail=False, permission_classes=[IsAdminUser])
    def admin(self, request):
        data = request.query_params

