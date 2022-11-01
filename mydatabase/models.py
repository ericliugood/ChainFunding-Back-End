from django.db import models
from django.contrib.auth.models import User
from pytz import timezone

class WalletAddress(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    walletType = models.CharField(max_length=18)
    walletAddress = models.CharField(max_length=36)

    class Meta:
        db_table = 'wallet_address'


class TransferLogs(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fromAddress = models.CharField(max_length=36)
    toAddress = models.CharField(max_length=36)
    amount = models.DecimalField(max_digits=128, decimal_places=18)
    token = models.CharField(max_length=18)
    time = models.DateTimeField()
    transferCheck = models.BooleanField(default=False)

    class Meta:
        db_table = 'transfer_logs'


class FundingProjects(models.Model):
    nftId = models.PositiveIntegerField()
    nftContractAddress = models.CharField(max_length=255)
    nftName = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    token = models.CharField(max_length=18)
    buyPrice = models.DecimalField(max_digits=128, decimal_places=18)
    sellPrice = models.DecimalField(max_digits=128, decimal_places=18)
    gasPrice = models.DecimalField(max_digits=128, decimal_places=18)
    evaluation = models.PositiveIntegerField(null=True)
    fundraiser = models.ForeignKey(User, on_delete=models.PROTECT)
    userLikeList = models.ManyToManyField(User, through='LikeLists', related_name='userLike')
    userFundingShare = models.ManyToManyField(User, through='FundingShares', related_name='userFunding')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'funding_projects'


class LikeLists(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)

    class Meta:
        db_table = 'like_lists'


class FundingShares(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=36, decimal_places=18)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'funding_shares'

class SoldPrices(models.Model):
    fundingShares = models.ForeignKey(FundingShares, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=128, decimal_places=18)
    sold = models.BooleanField(default=True)

    class Meta:
        db_table = 'sold_prices'



class Notice(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    notice = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notice'
