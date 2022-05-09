from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects


class FundingProjectsSerializer(ModelSerializer):
    
    class Meta:
        model=FundingProjects
        fields = ['id','nftId','startTime','endTime','token','buyPrice','sellPrice','gasPrice']