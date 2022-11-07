from django.db import models
from django.contrib.auth.models import User
from pytz import timezone

class WalletAddress(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    walletAddress = models.CharField(max_length=36)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)


    class Meta:
        db_table = 'wallet_address'


class TransferLogs(models.Model):
    fromAddress = models.CharField(max_length=36)
    toAddress = models.CharField(max_length=36)
    amount = models.DecimalField(max_digits=128, decimal_places=18)
    token = models.CharField(max_length=18)
    time = models.DateTimeField()
    transferCheck = models.PositiveIntegerField()
    remark = models.CharField(max_length=36)

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
    real_buyPrice = models.DecimalField(max_digits=128, decimal_places=18)
    sellPrice = models.DecimalField(max_digits=128, decimal_places=18)
    real_sellPrice = models.DecimalField(max_digits=128, decimal_places=18)
    gasPrice = models.DecimalField(max_digits=128, decimal_places=18)
    real_gasPrice = models.DecimalField(max_digits=128, decimal_places=18)
    evaluation = models.PositiveIntegerField(null=True)
    fundraiser = models.ForeignKey(User, on_delete=models.PROTECT)
    userLikeList = models.ManyToManyField(User, through='LikeLists', related_name='userLike')
    userFundingShare = models.ManyToManyField(User, through='FundingShares', related_name='userFunding',through_fields=('fundingProject','userData' ))
    userFundingShareSold = models.ManyToManyField(User, through='SharesSold', related_name='userSharesSold')
    userFundingShareBid = models.ManyToManyField(User, through='SharesBid', related_name='userSharesBid')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'funding_projects'


class LikeLists(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)

    class Meta:
        db_table = 'like_lists'


class FundingShares(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT, related_name='userData')
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=36, decimal_places=18)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    hands = models.PositiveIntegerField()
    userSold = models.ForeignKey(User, on_delete=models.PROTECT, related_name='userSold')

    class Meta:
        db_table = 'funding_shares'

class SharesSold(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=36, decimal_places=18)
    price = models.DecimalField(max_digits=128, decimal_places=18)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=18)
    userSharesSolded = models.ManyToManyField(User, through='SharesSolded', related_name='userSharesSolded')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shares_sold'

class SharesSolded(models.Model):
    sharesSold = models.ForeignKey(SharesSold, on_delete=models.PROTECT)
    userBuy = models.ForeignKey(User, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=36, decimal_places=18)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shares_solded'

class SharesBid(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    fundingProject = models.ForeignKey(FundingProjects, on_delete=models.PROTECT)
    share = models.DecimalField(max_digits=36, decimal_places=18)
    start_price = models.DecimalField(max_digits=128, decimal_places=18)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=18)
    userSharesBided = models.ManyToManyField(User, through='SharesBided', related_name='userSharesBided')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shares_bid'

class SharesBided(models.Model):
    sharesBid = models.ForeignKey(SharesBid, on_delete=models.PROTECT)
    userBid = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=128, decimal_places=18)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shares_bided'


class Notice(models.Model):
    userData = models.ForeignKey(User, on_delete=models.PROTECT)
    notice = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notice'

class TransferLogsUser(models.Model):
    fromUserData = models.ForeignKey(User, on_delete=models.PROTECT,related_name="fromUser")
    toUserData = models.ForeignKey(User, on_delete=models.PROTECT,related_name="toUser")
    amount = models.DecimalField(max_digits=128, decimal_places=18)
    token = models.CharField(max_length=18)
    time = models.DateTimeField(auto_now_add=True)
    transferCheck = models.PositiveIntegerField()
    remark = models.CharField(max_length=36)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transfer_logs_user'
