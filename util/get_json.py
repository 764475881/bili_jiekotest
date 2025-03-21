import json
from datetime import datetime


def bilibili_popular_json(response):
    jsonlist = []
    if response.status_code == 200:
        data = response.json()
        # 处理原始数据并插入数据库的示例
        for item in data['data']['list']:
            video_data = {
                'aid': item['aid'],
                'bvid': item['bvid'],
                'title': item['title'],
                'desc': item['desc'] if item['desc'] != '-' else None,
                'duration': item['duration'],
                'tid': item['tid'],
                'tname': item['tname'],
                'tidv2': item.get('tidv2'),
                'tnamev2': item.get('tnamev2'),
                'pubdate': item['pubdate'],
                'ctime': item['ctime'],
                'owner_mid': item['owner']['mid'],
                'owner_name': item['owner']['name'],
                'owner_face': item['owner']['face'],
                'view_count': item['stat']['view'],
                'danmaku_count': item['stat']['danmaku'],
                'reply_count': item['stat']['reply'],
                'favorite_count': item['stat']['favorite'],
                'coin_count': item['stat']['coin'],
                'share_count': item['stat']['share'],
                'like_count': item['stat']['like'],
                'pic_url': item['pic'],
                'width': item['dimension']['width'],
                'height': item['dimension']['height'],
                'rotate': item['dimension']['rotate'],
                'recommend_reason': item['rcmd_reason']['content'],
                'recommend_mark': item['rcmd_reason']['corner_mark'],
                'copyright': item['copyright'],
                'state': item['state'],
                'pub_location': item.get('pub_location')
            }
            jsonlist.append(video_data)
    else:
        print("Failed to retrieve data")
    return jsonlist


def bilibili_replies_json(response):
    replies_list = []
    if response.status_code == 200:
        data = response.json()
        print(data)
        for reply in data['data']['replies'] + data['data'].get('top_replies', []):
            # 处理表情数据
            emote_dict = {}
            if 'emote' in reply['content']:
                for k, v in reply['content']['emote'].items():
                    emote_dict[k] = {
                        'id': v['id'],
                        'url': v['url'],
                        'text': v['text']
                    }

            reply_data = {
                'rpid': int(reply['rpid_str']),
                'oid': int(reply['oid_str']),
                'type': reply['type'],
                'mid': int(reply['mid_str']),
                'root': int(reply['root_str']),
                'parent': int(reply['parent_str']),
                'dialog': int(reply['dialog_str']),
                'count': reply['count'],
                'rcount': reply['rcount'],
                'state': reply['state'],
                'fansgrade': reply['fansgrade'],
                'attr': reply['attr'],
                'ctime': reply['ctime'],
                'like_count': reply['like'],
                'message': reply['content']['message'],
                'emote': json.dumps(emote_dict, ensure_ascii=False) if emote_dict else None,
                'uname': reply['member']['uname'],
                'sex': reply['member']['sex'],
                'avatar': reply['member']['avatar'],
                'level': reply['member']['level_info']['current_level'],
                'vip_type': reply['member']['vip']['vipType'],
                'vip_status': reply['member']['vip']['vipStatus'],
                'official_desc': reply['member']['official_verify'].get('desc'),
                'location': reply['reply_control']['location'].split('：')[-1] if 'location' in reply['reply_control'] else None
            }
            replies_list.append(reply_data)
    else:
        print(f"请求失败，状态码：{response.status_code}")
    return replies_list

def bilibili_replies_replies_json(response):
    jsonlist = []
    if response.status_code == 200:
        data = response.json()
        root_data = data.get('data', {}).get('root', {})

        if root_data:
            member_info = root_data.get('member', {})
            vip_info = member_info.get('vip', {})
            reply_control = root_data.get('reply_control', {})

            reply_data = {
                'rpid': root_data.get('rpid'),
                'rpid_str': root_data.get('rpid_str'),
                'oid': root_data.get('oid'),
                'type': root_data.get('type'),
                'mid': root_data.get('mid'),
                'root': root_data.get('root'),
                'parent': root_data.get('parent'),
                'dialog': root_data.get('dialog'),
                'count': root_data.get('count'),
                'rcount': root_data.get('rcount'),
                'state': root_data.get('state'),
                'fansgrade': root_data.get('fansgrade'),
                'attr': root_data.get('attr'),
                'ctime': root_data.get('ctime'),
                'like_count': root_data.get('like'),
                'action': root_data.get('action'),
                'message': root_data.get('content', {}).get('message'),
                'member_mid': member_info.get('mid'),
                'member_uname': member_info.get('uname'),
                'member_sex': member_info.get('sex'),
                'member_sign': member_info.get('sign'),
                'member_avatar': member_info.get('avatar'),
                'member_level': member_info.get('level_info', {}).get('current_level'),
                'vip_type': vip_info.get('vipType'),
                'vip_label': vip_info.get('label', {}).get('text'),
                'reply_time_desc': reply_control.get('time_desc'),
                'reply_location': reply_control.get('location'),
                'up_like': root_data.get('up_action', {}).get('like'),
                'up_reply': root_data.get('up_action', {}).get('reply'),
            }
            jsonlist.append(reply_data)
    else:
        print(f"请求失败，状态码：{response.status_code}")
    return jsonlist