import datetime
from mydatabase.models import WalletAddress, TransferLogs
from django.contrib.auth.models import User
from mywallet.serializers import WalletAddressSerializer, TransferLogsSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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
        update_wallet.update(enabled=False)
        

        return Response(status=status.HTTP_204_NO_CONTENT)


class TransferLogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    serializer_class = TransferLogsSerializer
    queryset = TransferLogs.objects.all()

    def get_queryset(self):  # added string
        return super().get_queryset().filter(userData=User.objects.get(id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        transferLogsdata = request.data

        try:
            new_transferLogs = TransferLogs.objects.create(userData=User.objects.get(id=self.request.user.id),
                                                           fromAddress=transferLogsdata['fromAddress'],
                                                           toAddress=transferLogsdata['toAddress'],
                                                           amount=transferLogsdata['amount'],
                                                           token=transferLogsdata['token'],
                                                           time=transferLogsdata['time'],
                                                           transferCheck=transferLogsdata['transferCheck'])
            new_transferLogs.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
