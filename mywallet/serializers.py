from rest_framework.serializers import ModelSerializer,SerializerMethodField
from mydatabase.models import WalletAddress,TransferLogs,Wallet,TransferLogsUser


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

class TransferLogsUserSerializer(ModelSerializer):

    from_username = SerializerMethodField()

    to_username = SerializerMethodField()

    class Meta:
        model=TransferLogsUser
        fields = ['id','from_username','to_username','amount','token','time']

    def get_from_username(self,obj):
        return obj.fromUserData.username
    
    def get_to_username(self,obj):
        return obj.toUserData.username





