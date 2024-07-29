import download
import csv2ics
import time
import sys

def main():
    choose = input('请输入你要执行的操作：\n1.登陆教务系统以导出课表生成日历\n2.自行导出课表(.csv)放在 main.py 同根目录下以生成日历\n0.退出\n')
    if choose != '1' and choose != '2' and choose != '0':
        while choose != '1' and choose != '2' and choose != '0':
            choose = input('\n输入有误，请检查你的输入\n请输入你要执行的操作：\n1.登陆教务系统以导出课表生成日历\n2.自行导出课表放在 main.py 同根目录下以生成日历\n0.退出\n')
    if choose == '0':
        return
    elif choose == '1':
        download.download()
    elif choose == '2':
        csv2ics.csv2ics()
        
    print('即将在 5 秒后退出')
    time.sleep(5)
    return

if __name__ == '__main__':
    main()
