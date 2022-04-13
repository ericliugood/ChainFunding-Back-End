#  All Error Message

class Msg:
    class Err:
        class Account:  # User data CRUD error message
            create = "創建用戶錯誤"
            search = "查詢用戶錯誤"

        class FundingProject:  # Funding CRUD error message
            create = "創建集資錯誤"
            search = "查詢集資錯誤"

    class NotFound:
        # user
        user = "查無此用戶"

        # nft
        nft = "查無此NFT"
        funding_nft = "此NFT無集資項目"

        #
        project = "查無此集資項目"
        personal_project = "用戶無集資項目"
