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

    print(f"课表中的主要课程有：{set(schedual['课程名称'])}")

    # try:
    #     print('课表中的主要课程有：'+set(schedual['课程名称']))
    # except:
    #     print('该课表的格式无法识别，请检查后重试')
    #     return

    ics = f"""BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0

"""

    begin = {
        '01': '083000',
        '02': '092000',
        '03': '102500',
        '04': '111500',
        '05': '135000',
        '06': '144000',
        '07': '153000',
        '08': '163000',
        '09': '172000',
        '10': '183000',
        '11': '192000',
        '12': '201000'
    }

    end = {
        '01': '091500',
        '02': '100500',
        '03': '111000',
        '04': '120000',
        '05': '143500',
        '06': '152500',
        '07': '161500',
        '08': '171500',
        '09': '180500',
        '10': '191500',
        '11': '200500',
        '12': '205500'
    }

    table_size, table_type = schedual.shape

    for i in range(table_size):
        class_name = schedual['课程名称'][i]
        class_site = schedual['上课地点'][i]
        class_teacher = schedual['教师'][i]
        class_date = schedual['排课日期'][i].replace('-','')
        class_begin = class_date + 'T' + begin[schedual['节次'][i][:2]]
        class_end = class_date + 'T' + end[schedual['节次'][i][-2:]]
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

    print(f'导出成功, 在项目目录生成文件为 课表导出.ics，请用日历软件打开以导入')

if __name__ == '__main__':
    csv2ics()