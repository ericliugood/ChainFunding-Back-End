from mydatabase.models import WalletAddress,UserDatas,TransferLogs
from mywallet.serializers import WalletAddressSerializer,TransferLogsSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated



class WalletAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    serializer_class = WalletAddressSerializer
    queryset = WalletAddress.objects.all()

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(userData=UserDatas.objects.get(id=self.request.user.id))
    def create(self, request, *args, **kwargs):
        walletdata=request.data
        
        try:
                new_wallet = WalletAddress.objects.create(userData=UserDatas.objects.get(id=self.request.user.id),walletType=walletdata['walletType'],walletAddress=walletdata['walletAddress'])
                new_wallet.save()
                return Response(status=status.HTTP_201_CREATED) 
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 



class TransferLogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    serializer_class = TransferLogsSerializer
    queryset = TransferLogs.objects.all()

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(userData=UserDatas.objects.get(id=self.request.user.id))
    def create(self, request, *args, **kwargs):
        transferLogsdata=request.data
        print(transferLogsdata)
        
        try:
                new_transferLogs = TransferLogs.objects.create(userData=UserDatas.objects.get(id=self.request.user.id),
                fromAddress=transferLogsdata['fromAddress'],
                toAddress=transferLogsdata['toAddress'],
                amount=transferLogsdata['amount'],
                token=transferLogsdata['token'],
                time=transferLogsdata['time'] ,
                transferCheck=transferLogsdata['transferCheck'] )
                new_transferLogs.save()
                return Response(status=status.HTTP_201_CREATED) 
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 




        



