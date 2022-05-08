from rest_framework.serializers import ModelSerializer
from mydatabase.models import WalletAddress


class WalletAddressSerializer(ModelSerializer):
    
    class Meta:
        model=WalletAddress
        fields = ['walletType','walletAddress']


