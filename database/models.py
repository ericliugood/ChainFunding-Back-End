from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)


class UserDatas(AbstractBaseUser):
    usernameAccount = models.CharField(
        max_length=128,
        unique=True
    )
    emailAccount = models.EmailField(
        max_length=128,
        unique=True
    )
    emailAuth = models.BooleanField(default=False)
    evaluation = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'user_datas'

class WalletAddress(models.Model):
    userData = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    walletType = models.CharField(max_length=18)
    walletAddress = models.CharField(max_length=36)

    class Meta:
        db_table = 'wallet_address'


class TransferLogs(models.Model):
    userData = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    fromAddress = models.CharField(max_length=36)
    toAddress = models.CharField(max_length=36)
    amount = models.DecimalField(max_digits=18, decimal_places=18)
    token = models.CharField(max_length=18)
    time = models.DateTimeField()
    transferCheck = models.BooleanField(default=False)

    class Meta:
        db_table = 'transfer_logs'


class FundingProjects(models.Model):
    nftId = models.PositiveIntegerField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    token = models.CharField(max_length=18)
    buyPrice = models.DecimalField(max_digits=18, decimal_places=18)
    sellPrice = models.DecimalField(max_digits=18, decimal_places=18)
    gasPrice = models.DecimalField(max_digits=18, decimal_places=18)
    fundraiser = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    userLikeList = models.ManyToManyField(UserDatas, through='LikeLists', related_name='userLike')
    userFundingShare = models.ManyToManyField(UserDatas, through='FundingShares', related_name='userFunding')

    class Meta:
        db_table = 'funding_projects'


class LikeLists(models.Model):
    userData = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)

    class Meta:
        db_table = 'like_lists'


class FundingShares(models.Model):
    userData = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=18, decimal_places=18)

    class Meta:
        db_table = 'funding_shares'
