import logging
def logout(message):
    try:
        logfile=open("D:/pythonTtest/TDXPystock/每日输出.txt",'a+',encoding='utf-8')
    except FileNotFoundError as fnot:
        logfile = open("D:/pythonTtest/TDXPystock/每日输出.txt", 'w+',encoding='utf-8')

    print(message)   #输出到屏幕
    print(message, file=logfile) #输出到文件
    logfile.close()

    # logger = logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)
    # handler = logging.FileHandler("D:/pythonTtest/TDXPystock/每日输出.txt")
    # handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    #
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    #
    # logger.addHandler(handler)
    # logger.addHandler(console)
