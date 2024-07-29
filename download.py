import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import uuid
import getpass

def chooseSemester():
    year = input('请输入导出课表的年份：\n')
    if year<'2010' or year>'2029':
        while year<'2010' or year>'2029':
            year = input('根据教务系统，仅支持导出2010年至2019年的课表，请检查你的输入\n请输入导出课表的学年：\n')
    
    season = input('请输入导出课表的学期：\n1.春季\n2.秋季\n')
    if season != '1' and season != '2':
        while season != '1' and season != '2':
            season = input('输入有误，请检查你的输入\n请输入导出课表的学期：\n1.春季\n2.秋季\n')
    
    semester_code = ''

    if season == '1':
        semester_code = str(int(year)-1) + '02'
    else:
        semester_code = year + '01'

    return semester_code, year, season

def pd2ics(semester, schedual):

    ics = f"""BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0

"""

    turn = {'0102':['083000','100500'],
            '0304':['102500','120000'],
            '05':['135000','143500'],
            '0607':['144000','161500'],
            '0809':['163000','180500'],
            '1011':['183000','200500'],
            '101112':['183000','205500'],
            '0102030405060708':['083000','171500']
            }

    table_size, table_type = schedual.shape

    for i in range(table_size):
        class_name = schedual['kcmc'][i]
        class_site = schedual['jxcdmc'][i]
        class_teacher = schedual['teaxms'][i]
        class_date = schedual['pkrq'][i].replace('-','')
        class_begin = class_date + 'T' + turn[schedual['jcdm'][i]][0]
        class_end = class_date + 'T' + turn[schedual['jcdm'][i]][1]
        ics += f"""BEGIN:VEVENT
UID:{uuid.uuid4()}
DTSTART;TZID=Asia/Shanghai:{class_begin}
DTEND;TZID=Asia/Shanghai:{class_end}
SUMMARY:{class_name} {class_site} {class_teacher}
END:VEVENT

"""

    ics += 'END:VCALENDAR'

    with open(f'{semester}.ics', 'w') as file:
        file.write(ics)


def download():
    print('正在加载中，请稍等...')

    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    # 禁用webdriver特征
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
    })


    

    Quit_while = False
    first_time = True

    while not Quit_while:
        driver.get("https://authserver.gdut.edu.cn/authserver/login?service=https%3A%2F%2Fjxfw.gdut.edu.cn%2Fnew%2FssoLogin")
        if first_time:
            print('加载完成，请登录教务系统')
            first_time = False
        username = input('请输入学号：\n')
        username_input = driver.find_element(By.XPATH, "//input[@name='username']")
        username_input.send_keys(username)

        password = getpass.getpass('(密码不会被记录，仅用于本次登录教务系统)\n(密码已设置为不可见，输入完成后回车即可)\n请输入密码：\n')
        password_input = driver.find_element(By.XPATH, "//input[@name='passwordText']")
        password_input.send_keys(password)
        print('正在登录中，请稍等...')

        time.sleep(random.uniform(2, 5))
        login_button = driver.find_element(By.ID, "login_submit")
        login_button.click()

        if 'welcome' in driver.current_url:
            print('登录成功')
            Quit_while = True
        else:
            print('登录失败，请检查学号密码是否正确\n')

    driver.implicitly_wait(10)
    cookies = driver.get_cookies()

    for_sure = '2'

    while for_sure == '2':

        semester, year, season = chooseSemester()

        cookies_dict = {}
        for i in range(len(cookies)):
            cookies_dict[cookies[i]['name']] = cookies[i]['value']

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            'Referer': f'https://jxfw.gdut.edu.cn/xsgrkbcx!xskbList2.action?xnxqdm={semester}&zc='
        }

        payload = {
            'MIME Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'zc':'',
            'xnxqdm': semester,
            'page': '1',
            'sort': 'kxh',
            'order': 'asc',
            'rows': '1000'

        }
        url = 'https://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
        res = requests.post(url, cookies=cookies_dict, headers=headers, data=payload)
        if res.json()['total'] == 0:
            print(f'未找到该学期({semester})课表，请检查学年学期是否正确')
            continue
        data = pd.DataFrame(res.json()['rows'], dtype=str)
        for_sure = input(year+f"年度{'春季' if season=='1' else '秋季'}的课程主要有：{set(data['kcmc'])}\n是否确认导出该课表？\n1.确认\n2.取消，选择其他学期\n")
        
    print('正在导出中，请稍等...')

    pd2ics(semester, data)

    print(f'导出成功, 生成文件为{year+"春季" if season=="1" else "秋季"}课表.ics，请用日历软件打开以导入')

if __name__ == '__main__':
    download()