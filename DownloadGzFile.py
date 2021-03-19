# -*- coding: utf-8 -*-
import os
import time
from ftplib import FTP

# 加载初始化


def init():
    with open("IGSStationName.txt", "r", encoding="utf-8") as file:
        # 逐行读取站名
        global allStationName
        allStationName = file.readlines()
    # 建立异常记录文件
    global exceptionFile
    exceptionFile = open("异常记录.txt", "a", encoding="utf-8")
    # 记录异常开始时间
    recordStart = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.localtime(time.time()))
    exceptionFile.write("执行时间：" + recordStart + "\n")
    # 获取年和天数
    global year
    year = eval(input("输入年份："))
    global startDay
    startDay = eval(input("输入开始天数："))
    global endDay
    endDay = eval(input("输入结束天数："))


def ftpConnect():
    # 'igs.bkg.bund.de'/'cddis.nasa.gov'
    ftp_server = 'igs.ign.fr'
    username = ''
    password = ''
    # 调用构造函数，生成对象ftp
    ftp = FTP()
    # ftp.set_debuglevel(2)#打开调试级别2，显示详细信息
    print("正在连接服务器...")
    # 连接服务器
    ftp.connect(ftp_server, 21)
    print("正在登入服务器...")
    ftp.getwelcome()
    # 登录，空串代替匿名登入
    ftp.login(username, password)
    return ftp


def downloadFile():
    ftp = ftpConnect()
    # print("文件开始下载")
    # "/IGS/obs"/"/gnss/data/daily"
    datapath1 = "pub/igs/data/campaign/mgex/daily/rinex3/"
    constant1 = "_R_"
    constant2 = "0000_01D_30S_MO.crx.gz"
    constant3 = "0000_01D_CN.rnx.gz"
    for i in range(len(allStationName)):
        for Day in range(startDay, endDay+1):
            try:
                stationName = allStationName[i][0:]
                # 生成文件名称
                observationFile = stationName + constant1 + str(year) + \
                    date2Str(Day) + constant2
                navigationFile = stationName + constant1 + str(year) + \
                    date2Str(Day) + constant3
                if os.path.exists(observationFile):
                    print(observationFile + "已经存在！")
                else:
                    print(observationFile + "文件开始下载...")
                    serverPath = datapath1 + str(year) + \
                        "/" + date2Str(Day) + "/" + observationFile
                    if os.path.exists("./resources"):
                        fp = open("./resources/" + observationFile, 'wb')
                    else:
                        os.mkdir("resources")
                        fp = open("./resources/" + observationFile, 'wb')
                    # 接收服务器上文件并写入本地文件
                    ftp.retrbinary("RETR " + serverPath, fp.write)
                    # 文件关闭，释放使用权
                    fp.close()
                    print(observationFile + "文件下载完成！")
                    fileSize = ftp.size(serverPath)
                    print(
                        "文件大小：" +
                        str(fileSize(fileSize)[0]) +
                        fileSize(fileSize)[1])
                    print()

                if os.path.exists(navigationFile):
                    print(navigationFile + "已经存在！")
                else:
                    print(navigationFile + "文件开始下载...")
                    serverPath = datapath1 + str(year) + \
                        "/" + date2Str(Day) + "/" + navigationFile
                    if os.path.exists("./resources"):
                        fp = open("./resources/" + navigationFile, 'wb')
                    else:
                        os.mkdir("resources")
                        fp = open("./resources/" + navigationFile, 'wb')
                    # 接收服务器上文件并写入本地文件
                    ftp.retrbinary("RETR " + serverPath, fp.write)
                    # 文件关闭，释放使用权
                    fp.close()
                    print(navigationFile + "文件下载完成！")
                    fileSize = ftp.size(serverPath)
                    print(
                        "文件大小：" +
                        str(fileSize(fileSize)[0]) +
                        fileSize(fileSize)[1])
                    print()
            except Exception as ex_results:
                if str(ex_results) == "550 Failed to open file.":
                    exceptionFile.write(observationFile + "文件不存在！" + "\n")
                    print(observationFile + "文件不存在！")
                    fp.close()
                    # 删除空文件
                    os.remove(observationFile)
                else:
                    exceptionFile.write("抓到一个未处理异常：" + str(ex_results) + "\n")
                    print("抓到一个未处理异常：", ex_results)
    # 退出ftp服务器
    ftp.quit()


def date2Str(day):
    if 0 <= day <= 9:
        return "00" + str(day)
    elif 10 <= day <= 99:
        return "0"+str(day)
    else:
        return str(day)


def fileSize(fileSize):
    if 0 < fileSize <= 1024:
        return (fileSize, "B")
    else:
        fileSize = int(round(fileSize/1024))
        if 0 < fileSize <= 1024:
            return (fileSize, "KB")
        else:
            fileSize = int(round(fileSize/1024))
            if 0 < fileSize <= 1024:
                return (fileSize, "MB")
            else:
                fileSize = int(round(fileSize/1024))
                return (fileSize, "GB")


if __name__ == "__main__":
    init()
    downloadFile()
    print("所有文件下载完成!")
    # endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    exceptionFile.write(
        "结束时间：" +
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) +
        "\n")
    exceptionFile.close()
