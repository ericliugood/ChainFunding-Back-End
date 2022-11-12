from rest_framework.serializers import ModelSerializer
from mydatabase.models import WalletAddress,TransferLogs


class WalletAddressSerializer(ModelSerializer):
    
    class Meta:
        model=WalletAddress
        fields = ['id','walletAddress']

class TransferLogsSerializer(ModelSerializer):

    class Meta:
        model=TransferLogs
        fields = ['id','fromAddress','toAddress','amount','token','time','transferCheck']





