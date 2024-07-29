import pandas as pd
import uuid
import os

def csv2ics():

    files = os.listdir()

    file = ''

    for f in files:
        if 'csv' in f:
            file = f

    try:
        schedual = pd.read_csv(file,dtype=str)
    except:
        print('该课表的格式无法识别，请检查后重试')
        return


    required_columns = ['课程名称', '上课地点', '教师']
    missing_columns = [col for col in required_columns if col not in schedual.columns]

    if missing_columns:
        print(f"缺少必要的列: {', '.join(missing_columns)}，请检查CSV文件的格式。")
        return

    try:
        print('课表中的主要课程有：'+set(schedual['课程名称']))
    except:
        print('该课表的格式无法识别，请检查后重试')
        return

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
        class_name = schedual['课程名称'][i]
        class_site = schedual['上课地点'][i]
        class_teacher = schedual['教师'][i]
        class_date = schedual['排课日期'][i].replace('-','')
        class_begin = class_date + 'T' + turn[schedual['节次'][i]][0]
        class_end = class_date + 'T' + turn[schedual['节次'][i]][1]
        ics += f"""BEGIN:VEVENT
UID:{uuid.uuid4()}
DTSTART;TZID=Asia/Shanghai:{class_begin}
DTEND;TZID=Asia/Shanghai:{class_end}
SUMMARY:{class_name} {class_site} {class_teacher}
END:VEVENT

"""

    ics += 'END:VCALENDAR'

    with open('课表导出.ics', 'w') as file:
        file.write(ics)

    print(f'导出成功, 生成文件为 课表导出.ics，请用日历软件打开以导入')

if __name__ == '__main__':
    csv2ics()