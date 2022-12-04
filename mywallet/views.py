from django.utils.timezone import now
from mydatabase.models import WalletAddress, TransferLogs,Wallet,TransferLogsUser
from django.contrib.auth.models import User
from django.db.models import Q
from mywallet.serializers import WalletAddressSerializer, TransferLogsSerializer,WalletSerializer,TransferLogsUserSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from mywallet.walletfunction import wfunction
from rest_framework.decorators import action


class WalletAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = WalletAddressSerializer
    queryset = WalletAddress.objects.all()

    def get_queryset(self):  # added string
        return super().get_queryset().filter(userData=User.objects.get(id=self.request.user.id),enabled=True)

    def create(self, request, *args, **kwargs):
        walletdata = request.data

        qe = WalletAddress.objects.filter(walletAddress=walletdata['walletAddress'],enabled=True)
        if qe.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

        


        try:
            new_wallet = WalletAddress.objects.create(userData=User.objects.get(id=self.request.user.id),
                                                      walletAddress=walletdata['walletAddress'])
            new_wallet.save()
            sada = WalletAddressSerializer(instance=new_wallet)
            return Response(sada.data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        
        # update_wallet = WalletAddress.objects.filter(id=self.get_serializer.instance.id)
        # update_wallet.update(enabled=False)
        obj_id = kwargs['pk']
        update_wallet = WalletAddress.objects.filter(id=obj_id,userData=User.objects.get(id=self.request.user.id),enabled=True)
        if not update_wallet.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        update_walletu = WalletAddress.objects.get(id=obj_id)
        update_walletu.enabled = False
        update_walletu.save()
        #必須採用單筆更新，deletetime才會發揮作用
        

        return Response(status=status.HTTP_204_NO_CONTENT)


class TransferLogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated ]

    serializer_class = TransferLogsSerializer
    queryset = TransferLogs.objects.all()

    def get_queryset(self):  
        wok = WalletAddress.objects.values_list('walletAddress',flat=True).filter(userData=self.request.user,enabled=True)
        return super().get_queryset().filter(Q(fromAddress__in=wok)|Q(toAddress__in=wok))

    def create(self, request, *args, **kwargs):
        pass

    def destroy(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request):
        pass

class TransferLogsUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated ]

    serializer_class = TransferLogsUserSerializer
    queryset = TransferLogsUser.objects.all()

    def get_queryset(self):  
        return super().get_queryset().filter(Q(fromUserData=self.request.user)|Q(toUserData=self.request.user))

    def create(self, request, *args, **kwargs):
        pass

    def destroy(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request):
        pass



class WalletViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = WalletSerializer



    def get_queryset(self):  # added string
        return Wallet.objects.get_queryset().filter(userData=User.objects.get(id=self.request.user.id))

    @action(detail=False, methods=['GET'])
    def weth(self, request):
        return Response(wfunction().getWallet(userId=request.user.id,token="weth"),status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def usdt(self, request):
        return Response(wfunction().getWallet(userId=request.user.id,token="usdt"),status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def usdc(self, request):
        return Response(wfunction().getWallet(userId=request.user.id,token="usdc"),status=status.HTTP_200_OK)