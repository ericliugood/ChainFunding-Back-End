from rest_framework.serializers import ModelSerializer
from mydatabase.models import WalletAddress,TransferLogs,Wallet


class WalletAddressSerializer(ModelSerializer):
    
    class Meta:
        model=WalletAddress
        fields = ['id','walletAddress']

class WalletSerializer(ModelSerializer):
    
    class Meta:
        model=Wallet
        fields = ['token','amount']

class TransferLogsSerializer(ModelSerializer):

    class Meta:
        model=TransferLogs
        fields = ['id','fromAddress','toAddress','amount','token','time','transferCheck']





