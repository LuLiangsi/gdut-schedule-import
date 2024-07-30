# gdut-schedule-import

## 项目简介
`gdut-schedule-import` 是一个用于将广东工业大学的学生课程表导入到日历应用中的工具。

本项目仅作学习使用。

## 功能
- 自动挡：自动抓取课表并转换为日历文件（需提供账号密码）
- 手动挡：将教务系统导出的CSV转换为日历文件

## 安装
0. 本项目需要python版本3.9以上，由于使用了`selenium`进行登陆模拟，需要chrome内核
1. 克隆本仓库到本地：
```bash
git clone https://github.com/LuLiangsi/gdut-schedule-import.git
```
2. 进入项目目录：
```bash
cd gdut-schedule-import
```
3. 安装依赖：

- Mac & Linux
```bash
pip3 install -r requirements.txt
```
- Windows
```bash
pip install -r requirements.txt
```

## 使用方法
### 自动挡
1. 运行`main.py`：

- Mac & Linux
```bash
python3 main.py
```

- Windows（由于涉及写入文件，请以管理员身份打开，防止因权限问题无法写入日历文件）
```bash
python main.py
```
2. 根据提示完成操作（需要输入教务系统账号密码，仅做登陆使用，不会记录）

### 手动挡
1. 将你从教务系统导出的课程表CSV文件放置在项目目录中。
2. 运行`main.py`：

- Mac & Linux
```bash
python3 main.py
```

- Windows（由于涉及写入文件，请以管理员身份打开，防止因权限问题无法写入日历文件）
```bash
python main.py
```

## NOTE
生成的ICS日历文件需要用日历软件打开，ios如何将ICS格式文件用日历软件打开请自行搜索

