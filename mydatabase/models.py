from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser
)
from myaccount.views import CustomUserManager


class UserDatas(AbstractBaseUser):
    usernameAccount = models.CharField(
        max_length=128,
        unique=True
    )
    emailAccount = models.EmailField(
        max_length=128,
        unique=True
    )

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = 'usernameAccount'
    EMAIL_FIELD = 'emailAccount'
    REQUIRED_FIELD = []

    objects = CustomUserManager()

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
    amount = models.DecimalField(max_digits=128, decimal_places=18)
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
    buyPrice = models.DecimalField(max_digits=128, decimal_places=18)
    sellPrice = models.DecimalField(max_digits=128, decimal_places=18)
    gasPrice = models.DecimalField(max_digits=128, decimal_places=18)
    evaluation = models.PositiveIntegerField(null=True)
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
    share = models.DecimalField(max_digits=36, decimal_places=18)

    class Meta:
        db_table = 'funding_shares'


class Notice(models.Model):
    userData = models.ForeignKey(UserDatas, on_delete=models.PROTECT)
    notice = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notice'
