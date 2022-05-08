from rest_framework.serializers import ModelSerializer
from mydatabase.models import WalletAddress,UserDatas

class WalletAddressSerializer(ModelSerializer):
    
    class Meta:
        model=WalletAddress
        fields = ['userData','walletType','walletAddress']

class WalletAddress2Serializer(ModelSerializer):
    
    class Meta:
        model=WalletAddress
        fields = ['walletType','walletAddress']


