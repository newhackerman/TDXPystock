# -- coding:UTF-8 --
# 导入所需模块
from flask import Flask, render_template, request, jsonify
import uuid
import redis
from flask_cors import CORS
from dboprater import DB as db
from 爱问财条件取数通用版 import *

# 初始化Flask应用
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) #垮域访问

# 连接MySQL数据库
conn = db.dbconnect()

htmlfile = 'selectstocks.html'

redis_client = redis.Redis(host='124.71.9.141', port=6379,password='TEST@redis1',encoding='utf-8',decode_responses=True,socket_connect_timeout=2)

# 定义首页路由
@app.route('/')
def index():
    return render_template(htmlfile, conditionList=conditions, resultList=stockresult)


conditions = []  # 记录用户传入的条件
stockresult = pd.DataFrame()  # 记录选股结果


# 定义添加条件路由（使用Ajax异步通信）
@app.route('/add_condition', methods=['POST'])
def add_condition():
    return jsonify('')


# 定义选股路由
@app.route('/select_stocks', methods=['post'])
def select_stocks():
    # 获取前端传入的条件
    conditions=[]
    condition = request.get_data(cache=False).decode('utf8')
    condition = parse.unquote(condition)
    # print('前端传入的条件为：', condition)
    if condition:
        tmplist = str(condition).split('&')[::]
        for data in tmplist:
            data = str(data).split('=')[1]
            conditions.append(data)

    print('前端传入的条件为：', conditions)
    # return jsonify({'dddddd':''})
    # TODO: 实现具体的选股逻辑
    task_id = str(uuid.uuid4())

    result = pd.DataFrame()
    if len(conditions) > 0:
        result = select_stocks_async(task_id, conditions)  #
        # 返回选股结果
        if result.empty:
            return jsonify('无结果')
        else:
            if '股票市场类型' in result.columns:
                result=result.drop('股票市场类型', axis=1)
            if 'market_code' in result.columns:
                result=result.drop('market_code', axis=1)
        result=result.to_html()
        # print(result)
        return result
        # return render_template(htmlfile, conditionList=conditions, stockresults=result)
    else:
        return jsonify('')

@app.route('/view_results', methods=['POST'])
def view_results():
    if isinstance(stockresult,'DataFrame'):
        pass
    else:
        result=pd.DataFrame(stockresult)
    if stockresult.empty:
        return None
    return stockresult.to_html

# 调问财选股
def runselect(conditions):
    if len(conditions) == 0 or conditions is None:
        return
    for keywork in conditions:
        try:
            df = pd.DataFrame(get_aiwencai_data(keywork, iwencai_pages, iwencai_querytype['股票']))
            time.sleep(2)
            print('条件为：', keywork)
            print('取数个股为：', len(df))
            # df = df[stockresult['code'].isin(stocklist)]
            if df.empty:
                print('综合条件已经没有符合要求的个股了，如有需要请修改条件')
                break
        except BaseException as b:
            print(b)
    if df.empty:
        print(conditions)
        print('选股无结果')
    else:
        df.reset_index(drop=True, inplace=True)
        print(df)
    return df


# 在异步任务中执行选股逻辑，并将结果存储在Redis中
def select_stocks_async(task_id, conditions):
    # 执行选股逻辑
    print('任务id:',task_id)
    stockresult = runselect(conditions)
    # 存储选股结果
    if stockresult.empty:
        return pd.DataFrame()
    else:
        redis_client.set(f'task:{task_id}', ','.join(stockresult))
    return stockresult


@app.route('/check-task-status', methods=['POST'])
def check_task_status():
    task_id = request.form.get('task_id')

    # 查询任务状态
    task_status = redis_client.exists(f'task:{task_id}')
    if task_status:
        # 如果任务已经完成，返回任务结果
        stocks = redis_client.get(f'task:{task_id}').decode().split(',')
        result = {'status': 'completed', 'stocks': stocks}
    else:
        # 如果任务还未完成，返回状态码
        result = {'status': 'processing'}

    return jsonify(result)


# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
