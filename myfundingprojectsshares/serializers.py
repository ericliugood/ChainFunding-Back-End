from rest_framework.serializers import ModelSerializer,SerializerMethodField
from mydatabase.models import  FundingShares as Share ,SharesSold,SharesSolded
from django.db.models import Sum

class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['id','fundingProject', 'share']

class FundingSharesSoldSerializer(ModelSerializer):
    
    class Meta:
        model = SharesSold
        fields = ['id','fundingProject', 'share','price','token']
class FundingSharesSoldSerializer2(ModelSerializer):
    shares_sold_sum = SerializerMethodField()
    shares_sold_sum_scale = SerializerMethodField()
    class Meta:
        model = SharesSold
        fields = ['id','fundingProject', 'share','price','token','shares_sold_sum','shares_sold_sum_scale']
    def get_shares_sold_sum(self,obj):
        if obj.enabled == True:
            a = SharesSolded.objects.filter(sharesSold=obj).aggregate(share=Sum('share'))['share'] or 0
            return a
        return obj.price
    def get_shares_sold_sum_scale(self,obj):
        if obj.enabled == True:
            a = SharesSolded.objects.filter(sharesSold=obj).aggregate(share=Sum('share'))['share'] or 0
            return a/obj.price
        return obj.price/obj.price

class FundingSharesSoldedSerializer(ModelSerializer):
    class Meta:
        model = SharesSolded
        fields = ['id','share','sharesSold']