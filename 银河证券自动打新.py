import easytrader
from easytrader.utils.stock import get_today_ipo_data

# user = easytrader.use('htzq_client')
# user = easytrader.use('ht_client')
# user = easytrader.use('gj_client')
# user = easytrader.use('ths')
# user = easytrader.use('xq')
user = easytrader.use('yh_client',debug=False)
print(user)
usrlogin=user.prepare(config_file='D:/config.txt')  #登录
print(usrlogin)
atuoipo=user.auto_ipo()  #一键打新
userbalance= user.balance()   #获取资金
print(userbalance)
# user.position()  #获取持仓
# buy=user.buy('162411', price=0.55, amount=100)   #买入
# sell=user.sell('162411', price=0.55, amount=100)  #卖出
# user.cancel_entrust('buy/sell 获取的 entrust_no')   #撤单
# user.today_trades  #查看当日成交
# user.today_entrusts #查看当日委托
# user.refresh()  #刷新数据
# user.exit()    #退出
# ipo_data = get_today_ipo_data()  #查看当日可以打新的新股
# print(ipo_data)

