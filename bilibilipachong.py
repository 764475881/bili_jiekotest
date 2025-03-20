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
        'Cookie':'''buvid3=31AE4E3C-CE50-C3FB-2B9F-A2C589FCDD5421257infoc; b_nut=1727085821; _uuid=29538B93-43C6-DF9E-13A8-8172FB36183420043infoc; buvid4=CD49980F-7214-F4F3-3269-2A67FF7912EE23579-024092310-NTjbVv2UilJbCNvFKMeiKw%3D%3D; bsource=search_google; enable_web_push=DISABLE; CURRENT_FNVAL=4048; rpdid=|(kRR~YuuJl0J'u~k~Y||YRl; SESSDATA=1dca17c6%2C1744015499%2Ce96fb%2Aa1CjADZWtzcAHtXcpPmNWtyFZ3ndEbFv3p5ojetKg8IwDydJPTuNrtIoeAyIR27YRHbVISVnBfS080eXp5dFdUUnJXaTlKZFBXNlFPVGtBakpuSGE1YTBUVUJyRUIwQkViWDNUQ3R2Wmp2alVfdmRHRFlUQ1BOZWpMcDFIcFF1M25rcURZZTQwRnVnIIEC; bili_jct=42a921de3429971ebc6eb162f73b6eed; DedeUserID=28472252; DedeUserID__ckMd5=6b637572c90dd417; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; header_theme_version=CLOSE; sid=77wq2xac; b_lsid=A659B2A5_195A862A4DC; fingerprint=e8d3b28aaa09e77b1a4ce7a9c16424e2; buvid_fp_plain=undefined; enable_feed_channel=ENABLE; buvid_fp=e8d3b28aaa09e77b1a4ce7a9c16424e2; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI1NDgzMjksImlhdCI6MTc0MjI4OTA2OSwicGx0IjotMX0.fxTqbhYnbYftNI2VnbmDt5OOmHmuvgj-_dfyp-4uHIA; bili_ticket_expires=1742548269; home_feed_column=4; browser_resolution=1288-1177'''
    }
    start_indb("bilibili_replies",replys_url,replys_headers)
