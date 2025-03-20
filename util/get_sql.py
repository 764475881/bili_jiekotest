
from datetime import datetime
def getsql(table,values):

    now = datetime.now()
    # 连接数据库


    sql = ""
    valus = []
    # 执行SQL查询
    for i in values:
        l_item = []
        l_value = []
        for k,v in i.items():
            l_item.append("`"+k+"`")
            l_value.append(v)
        l_item.append("`get_time`")
        l_value.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        wenhao = ",".join(["%s"] * len(l_item))  # 生成与字段数量相同的占位符
        if sql == "":
            sql = "INSERT IGNORE INTO "+table +"("+ ",".join(l_item) +") VALUES (" + wenhao + ")"
        valus.append(tuple(l_value))
    return sql,valus
