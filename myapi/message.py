#  All Error Message

class Msg:
    class Err:
        class Account:  # User data CRUD error message
            create = "創建用戶錯誤"
            search = "查詢用戶錯誤"

        class FundingProject:  # Funding CRUD error message
            create = "創建集資錯誤"
            search = "查詢集資錯誤"

        class OpenSea:
            address = "請輸入地址"
            search = "查詢NFT錯誤"

        class Shares:
            # create_money_not_enough = {'error': 'money is not enough'}
            # delete_share_not_enough = {'error': 'day is higher than 2 days'}
            # not_found_shares = {'error': 'not found shares'}
            create = "創建份額錯誤"
            create_money_not_enough = "餘額不足"
            delete_share_not_enough = "發起超過2天"
            search = "查詢份額錯誤"
            create_share_not_filter = "不符合集資條件"
            shares_not_enabled = "已經集資過了"

    class NotFound:
        # user
        user ="查無此用戶"

        # nft
        nft = "查無此NFT"
        funding_nft = "此NFT無集資項目"

        # funding
        project = "查無集資項目"
        personal_project = "用戶無集資項目"

        # share
        shares = "查無份額"

        not_found_shares = "查無份額"

    class Success:
        # delete_success = {'msg': 'delete success'}
        delete_success = "刪除成功"
