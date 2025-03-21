import requests
import getconn
from util import get_json
from util.comt_sql import commit_sql
from util.get_sql import getsql


def start_indb(table,url,headers):
    #获取api相应
    global jsonlist
    response = requests.get(url, headers=headers)
    #获取json数据
    if table == 'bilibili_popular':
        jsonlist = get_json.bilibili_popular_json(response)
    elif table == 'bilibili_replies':
        jsonlist = get_json.bilibili_replies_json(response)
    #获取数据库连接
    conn = getconn.Getconn().getconn()
    #转化json为sql和值
    sql,vle =  getsql(table,jsonlist)
    #开始入库
    commit_sql(conn,sql,vle)

if __name__ == "__main__":
    popular_url = "https://api.bilibili.com/x/web-interface/popular"
    popular_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # start_indb("bilibili_popular",popular_url,popular_headers)

    replys_url = "https://api.bilibili.com/x/v2/reply?oid=114160012630590&type=1&pn=1&ps=20"
    replys_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie':'''x x x'''
    }
    start_indb("bilibili_replies",replys_url,replys_headers)
