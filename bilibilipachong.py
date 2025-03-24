import requests
import getconn
from util import get_json
from util.comt_sql import commit_sql
from util.get_sql import getsql
from datetime import datetime

def start_indb(table,url,headers):
    #获取api相应
    global jsonlist
    response = requests.get(url, headers=headers)
    # print(response.text)
    #获取json数据
    if table == 'bilibili_popular':
        try:
            jsonlist = get_json.bilibili_popular_json(response)
        except:
            print(response.json())
    elif table == 'bilibili_replies':
        jsonlist = get_json.bilibili_replies_json(response)
    elif table == 'bilibili_replies_replies':
        if response.json().get('code') == 12022:
            print("数据已被删除")
            return
        elif response.json().get('code') == 12061:
            print("评论区已关闭")
            return
        try:
            jsonlist = get_json.bilibili_replies_replies_json(response)
        except:
            print(response.json())
    #获取数据库连接
    conn = db_pool.get_connection()
    #转化json为sql和值
    sql,vle =  getsql(table,jsonlist)
    #开始入库
    commit_sql(conn,sql,vle)


def popular():
    popular_url = "https://api.bilibili.com/x/web-interface/popular"
    # popular_url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    popular_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    start_indb("bilibili_popular",popular_url,popular_headers)


def replies():
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT aid FROM bilibili_popular WHERE LEFT(CAST(get_time AS CHAR), 10) = %s",  # 修改点1：FROM 的正确拼写
        (datetime.now().strftime("%Y-%m-%d"),)           # 修改点2：参数使用元组格式
    )
    aids = cursor.fetchall()
    for aid in aids:
        print(aid)
        replys_url = "https://api.bilibili.com/x/v2/reply?oid="+str(dict(aid).get('aid')) +"&type=1&pn=1&ps=20"
        replys_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Cookie':'''buvid3=31AE4E3C-CE50-C3FB-2B9F-A2C589FCDD5421257infoc; b_nut=1727085821; _uuid=29538B93-43C6-DF9E-13A8-8172FB36183420043infoc; buvid4=CD49980F-7214-F4F3-3269-2A67FF7912EE23579-024092310-NTjbVv2UilJbCNvFKMeiKw%3D%3D; bsource=search_google; enable_web_push=DISABLE; rpdid=|(kRR~YuuJl0J'u~k~Y||YRl; header_theme_version=CLOSE; fingerprint=e8d3b28aaa09e77b1a4ce7a9c16424e2; buvid_fp_plain=undefined; enable_feed_channel=ENABLE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI1NDgzMjksImlhdCI6MTc0MjI4OTA2OSwicGx0IjotMX0.fxTqbhYnbYftNI2VnbmDt5OOmHmuvgj-_dfyp-4uHIA; bili_ticket_expires=1742548269; b_lsid=44FEE922_195B65C5E31; buvid_fp=e8d3b28aaa09e77b1a4ce7a9c16424e2; SESSDATA=c5d4ca3c%2C1758073368%2C63e12%2A31CjCfOPu7jVoMBC3aQKRhoOAIONbahy7rVITp16x7SYXWyobVRvHYnbC7eDvcZ6h9nNASVjFrTTA3bWxRWHc3OGZHclpMcTFLQUNwOFNpdTlSeVlncXRPM3RPWGo2NnFHYXdhV2V6TGVfQ1BxTU5rdVA1NVgtU3YzdFdSVDB2Y0QwSWlOcVN4Qkt3IIEC; bili_jct=df74eaebaa3e8e928937f638d9b81d88; DedeUserID=28472252; DedeUserID__ckMd5=6b637572c90dd417; sid=4yff6d4i; CURRENT_FNVAL=2000; home_feed_column=4; browser_resolution=1108-1177; bp_t_offset_28472252=1046610747519401984'''
        }
        start_indb("bilibili_replies_replies",replys_url,replys_headers)
        # time.sleep(3)

def replies_replies():
    conn = db_pool.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT oid,rpid FROM bilibili_replies WHERE oid in (SELECT aid FROM bilibili_popular WHERE get_time <= %s)",  # 修改点1：FROM 的正确拼写
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)           # 修改点2：参数使用元组格式
    )
    oids = cursor.fetchall()

    for oid in oids:
        replys_url = "https://api.bilibili.com/x/v2/reply/reply?oid="+str(dict(oid).get('oid')) +"&root="+str(dict(oid).get('rpid'))+"&pn=1&ps=2&type=1"
        # print(replys_url)
        replys_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Cookie':''''''
        }
        start_indb("bilibili_replies_replies",replys_url,replys_headers)


if __name__ == "__main__":
    db_pool = getconn.DBConnectionPool()
    # popular()
    # replies()
    replies_replies()
    ##test
