from rest_framework.serializers import ModelSerializer,SerializerMethodField
from mydatabase.models import FundingProjects as Project, FundingShares as Share ,SharesSold ,LikeLists
from django.db.models import Sum


class FundingProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice','stopPrice','lowest_share']

class FundingProjectsSerializer4(ModelSerializer):
    shares_sum = SerializerMethodField()
    shares_sum_scale = SerializerMethodField()
    shares_can_buy = SerializerMethodField()
    fundraiser_name = SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id','nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice','stopPrice','lowest_share','shares_sum','shares_can_buy','shares_sum_scale','fundraiser_name']
    def get_shares_sum(self,obj):
        if obj.status == 1:
            a = Share.objects.filter(hands=1,enabled=True,fundingProject=obj).aggregate(share=Sum('share'))['share'] or 0
            return a
        return obj.buyPrice
    def get_shares_can_buy(self,obj):
        if obj.status == 1:
            a = Share.objects.filter(hands=1,enabled=True,fundingProject=obj).aggregate(share=Sum('share'))['share'] or 0
            return obj.buyPrice-a
        return 0
    def get_shares_sum_scale(self,obj):
        if obj.status == 1:
            a = Share.objects.filter(hands=1,enabled=True,fundingProject=obj).aggregate(share=Sum('share'))['share'] or 0
            return a/obj.buyPrice
        return 1
    def get_fundraiser_name(self,obj):
        return obj.fundraiser.username


        

class FundingProjectsSerializer2(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice','stopPrice','lowest_share']

class FundingProjectsSerializer3(ModelSerializer):
    class Meta:
        model = Project
        fields = ['buyPrice','sellPrice', 'endTime']


class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['fundingProject', 'share']

class SoldPricesSerializer(ModelSerializer):
    class Meta:
        model = SharesSold
        fields = ['fundingShares', 'price']

class UserLikeListsSerializer(ModelSerializer):
    
    class Meta:
        model=LikeLists
        fields = ['fundingProject']
