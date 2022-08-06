from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from datetime import timedelta
from datetime import timezone

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
big_mother_day = os.environ['BIG_MOTHER_DAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id1 = os.environ["USER_ID1"]
user_id2 = os.environ["USER_ID2"]

template_id = os.environ["TEMPLATE_ID"]

tain_xing_api_key = os.environ["TX_API_KEY"]



def get_tody():
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )

    # 协调世界时
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)

    # 北京时间
    beijing_now = utc_now.astimezone(SHA_TZ)
    return datetime.strptime(str(beijing_now).split(" ")[0], "%Y-%m-%d")

def get_weekday():
    num = datetime.now().weekday()
    weekdayDict = {"0": "星期一", "1": "星期二", "2": "星期三", "3": "星期四", "4": "星期五", "5": "星期六", "6": "星期日"}
    return weekdayDict.get(str(num))


def get_cai_hong_pi():
    url = "http://api.tianapi.com/caihongpi/index?key=" + tain_xing_api_key
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['newslist'][0]['content']
    else:
        return "今天彩虹屁放不出来"


def get_tai_ci():
    url = "http://api.tianapi.com/dialogue/index?key=" + tain_xing_api_key
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = response.json()['newslist'][0]
        return data_dict['dialogue'], data_dict['english']
    else:
        return "今天台词说不出来"


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_jin_shan(date):
    url = "https://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title=" + date
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = response.json()
        return data_dict['content'], data_dict['note']
    else:
        return "今天金句还没出炉"


def get_love_days(today_date):
    delta = today_date - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday(today_date):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today_date).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def get_next_mother_day(today_date):
    return 30 - (today_date - datetime.strptime(big_mother_day, "%Y-%m-%d")).days

def run(user_id):
    today_date = get_tody()
    weekday = get_weekday()
    love_days = get_love_days(today_date)
    weather, temperature, min_temperature, max_temperature = get_weather()
    next_big_mother_day = get_next_mother_day(today_date)
    cai_hong_pi = get_cai_hong_pi()
    jin_shan_en, jin_shan_zh = get_jin_shan(str(today_date).split(" ")[0])

    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    data = {
        "today": {"value": today_date, "color": "#f4cccc"},
        "weekday": {"value": weekday, "color": "#76a5af"},
        "love_days": {"value": love_days, "color": "#ea9999"},
        "weather": {"value": weather, "color": "#ffff00"},
        "temperature": {"value": temperature, "color": "#674ea7"},
        "min_temperature": {"value": min_temperature, "color": "#3d85c6"},
        "max_temperature": {"value": max_temperature, "color": "#a64d79"},
        "big_mother_day": {"value": big_mother_day, "color": "#a61c00"},
        "next_big_mother_day": {"value": next_big_mother_day, "color": "#6aa84f"},
        "cai_hong_pi": {"value": cai_hong_pi, "color": "#c9daf8"},
        "jin_shan_en": {"value": jin_shan_en, "color": "#a4c2f4"},
        "jin_shan_zh": {"value": jin_shan_zh, "color": "#6fa8dc"}
    }
    print(user_id, template_id, data)
    res = wm.send_template(user_id, template_id, data)
    print(res)

run(user_id1)
run(user_id2)
