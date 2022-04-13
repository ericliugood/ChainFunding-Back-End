from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects


class SearcherSerializer(ModelSerializer):
    class Meta:
        model = FundingProjects
        fields = '__all__'
        