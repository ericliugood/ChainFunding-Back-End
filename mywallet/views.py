from mydatabase.models import WalletAddress,UserDatas
from mywallet.serializers import WalletAddressSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response



class WalletAddressViewSet(viewsets.ModelViewSet):
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







        



