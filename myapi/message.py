#  All Error Message

class Msg:
    class Err:
        class Account:  # User data CRUD error message
            create = {'error': "創建用戶錯誤"}
            search = {'error': "查詢用戶錯誤"}

        class FundingProject:  # Funding CRUD error message
            create = {'error': "創建集資錯誤"}
            search = {'error': "查詢集資錯誤"}

        class OpenSea:
            address = {'error': "請輸入地址"}
            search = {'error': "查詢NFT錯誤"}

        class Shares:
            create_money_not_enough = {'error': 'money is not enough'}
            shares_not_enabled = {'error': 'shares not enabled'}
            create_share_not_filter = {'error': '集資項目不符合條件或集資低於下限（最後一人要買剩下的）'}
            delete_share_not_enough = {'error': 'day is higher than 2 days'}
            not_found_shares = {'error': 'not found shares'}
            search = {'error': "查詢份額錯誤"}

    class NotFound:
        # user
        user ={'error':  "查無此用戶"}

        # nft
        nft = {'error': "查無此NFT"}
        funding_nft = {'error': "此NFT無集資項目"}

        # funding
        project = {'error': "查無集資項目"}
        personal_project = {'error': "用戶無集資項目"}

        # share
        shares = {'error': "查無份額"}

    class Sucess:
        delete_sucess = {'msg': 'delete sucess'}
