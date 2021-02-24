import akshare as ak #api 使用：https://akshare-4gize6tod19f2d2e-1252952517.tcloudbaseapp.com/index.html

class akShareUnit(ak):

    # 例获取基金排名top20
    def get_Topjijin(self):
        repsponse = ak.fund_em_open_fund_rank()
        print(repsponse.head(21))
        return repsponse.head(21)    #获取基金排名
        def get_Topjijin(self):
            repsponse=ak.fund_em_open_fund_rank()
            print(repsponse.head(21))
            return repsponse.head(21)
