import struct as st
import os
#########解码
def STOCKuncode(date,codeamo):     #可以解出日期了,竞价数据要用f解
    text1=st.unpack("I",date)[0]
    text2 = st.unpack("f", codeamo)[0]
    return text1,text2
    # with open('C:\\Users\\test\\Desktop\\0_300563.dat','rb') as fr:
    #     seek=4
    #     str=fr.read()
    #    # aa=st.pack('f', 0)
    #     for a in range(0,len(str),seek*2):
    #        text1=st.unpack("I",str[a:a+seek])[0]
    #        text2=st.unpack("f",str[a+seek:a+seek+seek])[0]
    #        text3=st.pack('I',text1)  #整型编码
    #        text4=st.pack('f',text2)   #float 编码
    #        print(text1,text2)
#STOCKuncode()
#########编码
def stockcode(date,codeamo):
    seek =4
    text1=st.pack('I', int(date))
    #print(text1)
    text2=st.pack('f', float(codeamo))
    #print(text2)
    return text1+text2

# 将通达信的日线文件转换成CSV格式
def stockdaydata2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    try:
        source_file = open(source_dir + os.sep + file_name, 'rb')
        buf = source_file.read()
        source_file.close()

        # 打开目标文件，后缀名为CSV
        target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        #print(rec_count)
        begin = 0
        end = 32
        # 4字节 如20091229
        # 开盘价*100
        # 最高价*100
        # 最低价*100
        # 收盘价*100
        # 成交额
        # 成交量
        # 保留值

        header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
            + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('保留') + '\n'
        target_file.write(header)
        for i in range(rec_count):
            # 将字节流转换成Python数据格式
            # I: unsigned int
            # f: float
            a= st.unpack('IIIIIfII', buf[begin:end])
            #print(a)
            line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
                + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
                + str(a[6]) + ', ' + str(a[7]) + '\n'
            #print(line)
            target_file.write(line)
            begin += 32
            end += 32
        target_file.close()
    except FileNotFoundError as fnot:
        print('file is not found')
    except TypeError as tper:
        print(tper)
    except BaseException as ber:
        print(ber)