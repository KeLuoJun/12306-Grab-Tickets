# settings.py

# 车站cookie值
STARTS = "%u5317%u4EAC%2CBJP"  # 起点：北京
ENDS = "%u4E0A%u6D77%2CSHH"    # 终点：上海

# 购票日期
DTIME = "2025-02-23"

# 抢票时间
TIME = "2025-02-21 12:51:00"

# 车次配置
ORDER = 3               # 车次
USERS = ["name",]       # 乘车人
XB = "二等座"            # 席别
PZ = "成人票"            # 票种

# 是否学生票
STUDENT = False

# chromedriver路径
EXECUTABLE_PATH = './asset/chromedriver.exe'

EMAIL_SENDER="...@qq.com"  # 发件人邮箱
EMAIL_PASSWORD=""    # 发件人邮箱登录授权码
EMAIL_RECEIVER="...@qq.com"       # 收件人邮箱（可以是自己的邮箱）
