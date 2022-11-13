from mydatabase.models import Wallet
from django.contrib.auth.models import User
from mywallet.serializers import WalletSerializer

class wfunction():
    def __init__(self):
        pass

    def addWallet(self,userId,token):
        Wallet.objects.create(userData=User.objects.get(id=userId),amount=0.0,token=token)


    def getWallet(self,userId,token):
        if not Wallet.objects.filter(userData=User.objects.get(id=userId),token=token).exists():
            self.addWallet(userId,token)
        wallets = WalletSerializer(Wallet.objects.get(userData=User.objects.get(id=userId),token=token))
        return wallets.data
        



    def walletChange(self,userId,token,amount):
        if not Wallet.objects.filter(userData=User.objects.get(id=userId),token=token).exists():
            self.addWallet(userId,token)