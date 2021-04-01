import requests
from bs4 import BeautifulSoup as bs
import telebot
import json
import datetime
import vk
import os

userid = "9884968540"
group_id = "43081042"

facebook_url = "https://www.facebook.com/ProgresstechUA/"
instagram_url = "https://instagramdimashirokovv1.p.rapidapi.com/followers/" + userid + "/optional"

#TOKEN = os.getenv("TOKEN")
#vk_token = os.getenv("VK_TOKEN")

TOKEN = '1474183111:AAHg3vQ7nXUcopS7nJ_1FIMzAOcs8P-Z1H8'
vk_token = '153f8e9d153f8e9d153f8e9da5154a28c71153f153f8e9d4ada7a970cf22b69880027e4'

def update_stat():
    curdate = datetime.datetime.now()
    write_date = str(curdate.day) + "." + str(curdate.month) + "." + str(curdate.year)

    with open('statistic.txt', 'w') as f:
        f.write(write_date + "\n")
        f.write("facebook " + str(parse_facebook()) + "\n")
        f.write("vk " + str(parse_vk()) + "\n")
        f.write("instagram " + str(parse_instagram()))

    return {
        "facebook": parse_facebook(),
        "vk": parse_vk(),
        "instagram": parse_instagram()
    }


def get_statistic():
    curdate = datetime.datetime.now()
    display_date = str(curdate.day) + "." + str(curdate.month) + "." + str(curdate.year) + "\n"

    with open('statistic.txt', 'r') as f:
        date = f.readline()
        facebook_stat = f.readline()
        vk_stat = f.readline()
        instagram_stat = f.readline()

    if date == display_date:
        return {
            "facebook": facebook_stat.split(" ")[1],
            "vk": vk_stat.split(" ")[1],
            "instagram": instagram_stat.split(" ")[1]
        }
    else:
        return update_stat()


def parse_facebook():
    try:
        facebook_res = bs(requests.get(facebook_url).content, "html.parser").select("div._4bl9 div")[5].text
        facebook_subs = ""
        for i in facebook_res:
            if i.isdigit():
                facebook_subs += i
        return facebook_subs
    except:
        pass


def parse_vk():
    try:
        session = vk.Session(access_token=vk_token)
        vk_api = vk.API(session)
        return vk_api.groups.getMembers(group_id=group_id, v=5.126)["count"]
    except:
        pass


def parse_instagram():
    try:
        querystring = {"userid": userid, "cursor": "optional"}
        headers = {
            'userid': userid,
            'cursor': "optional",
            'x-rapidapi-key': "42cffa6510msha80dfb921f197a4p148137jsn9f7dbdff74d9",
            'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com"
            }
        response = requests.request("GET", instagram_url, headers=headers, params=querystring)
        return json.loads(response.text)["count"]
    except:
        pass


bot = telebot.TeleBot(TOKEN)

answer = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
answer.row('Текущая статистика')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Доброго времени суток, "
                                      "если вы желаете посмотреть статистику подписчиков, "
                                      "нажмите кнопку \"Текущая статистика\" на клавиатуре!", reply_markup=answer)


@bot.message_handler(content_types=['text'])
def statistic(message):
    if message.text.lower() == "текущая статистика":
        stat = get_statistic()
        bot.send_message(message.chat.id, "Статистика подписчиков:" +
                                          "\nFacebook: " + str(stat["facebook"]) +
                                          "\nВконтакте: " + str(stat["vk"]) +
                                          "\nInstagram: " + str(stat["instagram"]))


bot.polling()
