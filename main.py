from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
from datetime import timedelta
from datetime import timezone


start_date = os.environ['START_DATE']
city = os.environ['CITY']

her_birthday = os.environ['HER_BIRTHDAY']
my_birthday = os.environ['MY_BIRTHDAY']

big_mother_day = os.environ['BIG_MOTHER_DAY']
big_mother_day_leave = os.environ['BIG_MOTHER_DAY_LEAVE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id1 = os.environ["USER_ID1"]
user_id2 = os.environ["USER_ID2"]

weather_template_id = os.environ["WEATHER_TEMPLATE_ID"]
date_template_id = os.environ["DATE_TEMPLATE_ID"]
funny_template_id = os.environ["FUNNY_TEMPLATE_ID"]
wwzc_template_id = os.environ["WWZC_TEMPLATE_ID"]

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
    print(beijing_now)
    return datetime.strptime(str(beijing_now).split(" ")[0], "%Y-%m-%d")


def get_weekday(today_date):
    num = today_date.weekday()
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
        return "今天是哑剧，没台词", ""


def get_tian_gou():
    url = "http://api.tianapi.com/tiangou/index?key=" + tain_xing_api_key
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['newslist'][0]['content']
    else:
        return "今天不当添购了哼哼！"


def get_cai_zi_mi():
    url = "http://api.tianapi.com/zimi/index?key=" + tain_xing_api_key
    response = requests.get(url)
    if response.status_code == 200:
        data_dict = response.json()['newslist'][0]
        return data_dict['content'], data_dict['answer'], data_dict['reason']
    else:
        return "今天字谜路了", "", ""


def get_wyy_comment():
    url = "http://api.tianapi.com/hotreview/index?key=" + tain_xing_api_key
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['newslist'][0]['content']
    else:
        return "今天网易云emo了..."


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], weather['wind'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high']), weather['airQuality'], weather['humidity']


def get_weather_notice(weather):
    if weather == "晴":
        return "小刘~ 今天有太阳，注意防晒哦！"
    elif weather == "阴":
        return "小刘~ 阴天！在不开灯的房间..."
    elif weather == "多云":
        return "小刘~ 今天是阴晴不定的一天哦"
    elif weather == "雨":
        return "小刘~ 今天有雨，出门记得带伞！"
    else:
        return "小刘~ 俺今天就不叨叨了！"


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


def get_birthday(today_date,  birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < today_date:
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


"""
根据上一次来的和走的时间，与现在时间对比，如果正在大姨妈，环境里的配置是big_mother_day=True，big_mother_day_leave=False
如果非姨妈期间，big_mother_day和big_mother_day_leave是具体时间
"""
def get_big_mother_value(big_mother_day, big_mother_day_leave, today_date):
    if big_mother_day == "True":
        return "正在经期中...", special_text(), special_text(), "正在经期中...", special_text()
    else:
        next_mother_day = get_next_mother_day(today_date)
        if next_mother_day < 0:
            return big_mother_day, special_text("-", "#000000"), big_mother_day_leave, "延迟 {days} ".format(days=str(abs(next_mother_day))), special_text("天", "#000000")
        else:
            return big_mother_day, special_text("-", "#000000"), big_mother_day_leave, str(next_mother_day), special_text("天后", "#000000")


"""
用于特殊情况处理 ： 还有{{10}} {{天}}
"""
def special_text(text="", color="#000000"):
    if text == "":
        return {"value": text}
    else:
        return {"value": text, "color": color}

"""
next_mother_day是获取环境里的上一次经期时间，用当前日期减去上一次的日期得出的天数
"""
def get_mother_day_notice(big_mother_day, today_date):
    if big_mother_day == "True":
        return "姨妈ing，别想冷饮了，吨吨吨热水吧！"
    else:
        next_mother_day = get_next_mother_day(today_date)
        if 1 <= next_mother_day <= 7:
            return "大姨妈快来啦，不能再吨吨吨地喝冷饮咯！"
        elif 7 < next_mother_day < 12:
            return "大姨妈刚走哦，别一下子吨吨吨喝太多冷饮哦！"
        elif next_mother_day <= 0:
            return "姨妈延期了{days}天诶，别担心，保持愉悦心情和正常作息即可！".format(days=abs(next_mother_day))
        else:
            return "大姨妈旅游去了，该吃吃该喝喝！"


def weather_sender(wm, user_id, template_id):
    # 获取时间
    today_date = get_tody()
    today_str = str(today_date).split(" ")[0]
    weekday = get_weekday(today_date)

    # 获取天气相关
    weather, wind, temperature, min_temperature, max_temperature, air_quality, humidity = get_weather()

    # 获取天气提醒
    weather_notice = get_weather_notice(weather)

    data = {
        "today": {"value": today_str, "color": "#f4cccc"},
        "weekday": {"value": weekday, "color": "#76a5af"},
        "city": {"value": city, "color": "#436EEE"},
        "weather": {"value": weather, "color": "#e69138"},
        "temperature": {"value": temperature, "color": "#674ea7"},
        "min_temperature": {"value": min_temperature, "color": "#3d85c6"},
        "wind": {"value": wind, "color": "#3CB371"},
        "max_temperature": {"value": max_temperature, "color": "#a64d79"},
        "air_quality": {"value": air_quality, "color": "#CD6839"},
        "humidity": {"value": humidity, "color": "#6495ED"},
        "weather_notice": {"value": weather_notice, "color": "#75A3AE"},
    }
    print(data)
    res = wm.send_template(user_id, template_id, data)
    print(res)


def date_menage_sender(wm, user_id, template_id):
    today_date = get_tody()

    love_days = get_love_days(today_date)
    until_her_birthday = get_birthday(today_date, her_birthday)
    until_my_birthday = get_birthday(today_date, my_birthday)

    # TODO:next_big_mother_day 根据天数变换颜色
    b_m_d, text1, b_m_d_l, next_big_mother_day, text2 = get_big_mother_value(big_mother_day, big_mother_day_leave, today_date)

    mother_day_notice = get_mother_day_notice(big_mother_day, today_date)

    data = {
        "love_days": {"value": love_days, "color": "#ea9999"},
        "until_her_birthday": {"value": until_her_birthday, "color": "#E9967A"},
        "until_my_birthday": {"value": until_my_birthday, "color": "#166985"},
        "big_mother_day": {"value": b_m_d, "color": "#A52A2A"},
        "text1": text1,
        "big_mother_day_leave": {"value": b_m_d_l, "color": "#E69E9E"},
        "next_big_mother_day": {"value": next_big_mother_day, "color": "#6aa84f"},
        "text2": text2,
        "mother_day_notice": {"value": mother_day_notice, "color": "#75A3AE"},
    }
    print(data)
    res = wm.send_template(user_id, template_id, data)
    print(res)

def funny_sender(wm, user_id, template_id):
    cai_hong_pi = get_cai_hong_pi()
    tian_gou = get_tian_gou()
    zi_mi, answer, reason = get_cai_zi_mi()

    data = {
        "cai_hong_pi": {"value": cai_hong_pi, "color": "#FF6666"},
        "tian_gou": {"value": tian_gou, "color": "#A64DFF"},
        "zi_mi": {"value": zi_mi, "color": "#990000"},
        "answer": {"value": answer, "color": "#FFFFFF"},
        "reason": {"value": reason, "color": "#FFFFFF"},
    }
    print(data)
    res = wm.send_template(user_id, template_id, data)
    print(res)


def wwzc_sender(wm, user_id, template_id):
    # 获取时间
    today_date = get_tody()
    today_str = str(today_date).split(" ")[0]

    # lines_zh, lines_en = get_tai_ci()
    lines = "今天是哑剧，没台词"
    times = 0
    while(True):
        if times >= 5:
            break
        lines_zh, lines_en = get_tai_ci()
        if len(lines_en) <= 90 and len(lines_zh) <= 50:
            if lines_en.strip() != "" and lines_zh.strip() != "":
                lines = lines_en + "\n" + lines_zh
                break
            elif lines_en.strip() != "" or lines_zh.strip() != "":
                lines = lines_en + lines_zh
                break
        times += 1
        
    jin_shan_en, jin_shan_zh = get_jin_shan(today_str)
    wyy_comment = get_wyy_comment()

    data = {
        "lines": {"value": lines, "color": "#004D99"},
        "jin_shan_en": {"value": jin_shan_en, "color": "#6fa8dc"},
        "jin_shan_zh": {"value": jin_shan_zh, "color": "#c9daf8"},
        "wyy_comment": {"value": wyy_comment, "color": "#D8648B"}
    }
    print(data)
    res = wm.send_template(user_id, template_id, data)
    print(res)

def run(user_id):
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    weather_sender(wm, user_id, weather_template_id)
    date_menage_sender(wm, user_id, date_template_id)
    funny_sender(wm, user_id, funny_template_id)
    wwzc_sender(wm, user_id, wwzc_template_id)

run(user_id1)
run(user_id2)
