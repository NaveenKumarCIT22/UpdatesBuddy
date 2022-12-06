from telebot import TeleBot
from telebot.types import InlineQueryResultArticle, InputMedia, InputTextMessageContent, PollAnswer, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from Resourses.ttdb import createTB, getData, insertData
from Resourses.PyCrypt import decrypt, encrypt
from Resourses.MorseTrans import mtot, ttom
from datetime import datetime, date
from discord_webhook import DiscordWebhook
from json import dumps
import time

TOKEN = ""
bot = TeleBot(TOKEN)
STAT = ""
DBN = "TimeTableDB"


def disc_appreq(cont):
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/...', content=cont)
    webhook.execute()


def disc_fdbk(cont):
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/...', content=cont)
    webhook.execute()



@bot.message_handler(func=lambda message: "hi" in message.text or "hello" in message.text)
@bot.message_handler(commands=["greet","start"])
def greet(message):
    msg = " Hello, how are you? \nThis is UpdatesBuddy! Get in touch with the happenings of ur day (actually not fully, lol).\nPlease use the commands to get help from me."
    bot.reply_to(message, msg)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,"Hi there is nothing to help with this bot cause this bot does nothing but run test scripts lol!")


@bot.message_handler(commands=["encrypt"])
def encpt(message):
    global STAT
    STAT = "encrypt"
    bot.reply_to(message,"Please send your text to be encrypted")


@bot.inline_handler(func= lambda msg: "/encrypt" in msg.query)
def inencpt(message):
    txt = message.query.lstrip("/encrypt").strip()
    if "<k>" not in txt:
        txt = "text<k>key"
    txt, key = txt.split("<k>")
    msg = encrypt(txt, key)
    reply1 = InlineQueryResultArticle(id=1, title="EncOnly",input_message_content=InputTextMessageContent(msg),description=msg)
    reply2 = InlineQueryResultArticle(id=2, title="EncAlso",input_message_content=InputTextMessageContent(txt+"\n"+msg),description=txt+"\n"+msg)
    bot.answer_inline_query(message.id,[reply1,reply2])


@bot.message_handler(commands=["decrypt"])
def decpt(message):
    global STAT
    STAT = "decrypt"
    bot.reply_to(message,"Please send your text to be decrypted")


@bot.inline_handler(func= lambda msg: "/decrypt" in msg.query)
def indecpt(message):
    txt = message.query.lstrip("/decrypt").strip()
    if "<k>" not in txt:
        txt = "text<k>key"
    txt, key = txt.split("<k>")
    msg = decrypt(txt, key)
    reply1 = InlineQueryResultArticle(id=1, title="DecOnly",input_message_content=InputTextMessageContent(msg),description=msg)
    reply2 = InlineQueryResultArticle(id=2, title="DecAlso",input_message_content=InputTextMessageContent(txt+"\n"+msg),description=txt+"\n"+msg)
    bot.answer_inline_query(message.id,[reply1,reply2])


@bot.message_handler(commands=["tomorse"])
def tomorse(message):
    global STAT
    bot.send_message(message.chat.id,"Now send your text to be converted to morse code")
    STAT = "tomorse"


@bot.message_handler(commands=["frmmorse"])
def frmmorse(message):
    global STAT
    bot.send_message(message.chat.id,"Now send your morse code to be converted to text")
    STAT = "frmmorse"


@bot.inline_handler(func= lambda msg: "/tomorse" in msg.query)
def intomorse(message):
    text = message.query.lstrip("/tomorse").strip()
    if text == "":
        text = "no message"
    mtext = ttom(text)
    reply1 = InlineQueryResultArticle(id=1, title="MorseOnly",input_message_content=InputTextMessageContent(mtext),description=mtext)
    reply2 = InlineQueryResultArticle(id=2, title="MorseAlso",input_message_content=InputTextMessageContent(text+"\n"+mtext),description=text+"\n"+mtext)
    bot.answer_inline_query(message.id,[reply1,reply2])
    

@bot.inline_handler(func= lambda msg: "/frmmorse" in msg.query)
def infrmmorse(message):
    mtxt = message.query.lstrip("/frmmorse").strip()
    if mtxt != "":
        txt = mtot(mtxt)
        rply1 = InlineQueryResultArticle(id=1, title="TextOnly",input_message_content=InputTextMessageContent(txt),description=txt)
        rply2 = InlineQueryResultArticle(id=2, title="TextAlso",input_message_content=InputTextMessageContent(mtxt+"\n"+txt),description=mtxt+"\n"+txt)
        bot.answer_inline_query(message.id,[rply1,rply2])


@bot.message_handler(commands=["poll"])
def poll(message):
    quest = ["Is this working? lol","Well you like it?","Do you have any idea of what could accomplished with this?"]
    opts = [["Yah","Nope"],["Yah!","Not at all","Could be better!"],["Yah, I do","No idea","This is just waste of time!"]]
    for i in range(len(quest)):
        j = quest[i]
        v = opts[i]
        res = bot.send_poll(chat_id=message.chat.id,question=j,options=v,type="regular", is_anonymous=False)
        """ for i in range(2):
            print(">>",res.poll.options[i].text)
            print(">>",res.poll.options[i].voter_count) """


""" @bot.inline_handler(func= lambda msg: "/poll")
def inpoll(message):
    repls = []
    quest = ["Is this working? lol","Well you like it?","Do you have any idea of what could accomplished with this?"]
    opts = [["Yah","Nope"],["Yah!","Not at all","Could be better!"],["Yah, I do","No idea","This is just waste of time!"]]
    for n in range(len(quest)):

        repls.append(InlineQueryResultArticle(id=1, title="TextOnly",input_message_content=InputMedia(poll,)),description=quest[n]))
 """


@bot.message_handler(commands=['btnmsg'])
def btnmsg(message):
    kb = InlineKeyboardMarkup([
    [InlineKeyboardButton("Yes",callback_data="reply_yes"),
    InlineKeyboardButton("No", callback_data='reply_no')],
    [InlineKeyboardButton("Get Appointment", callback_data='reply_appointment')]
    ])
    bot.reply_to(message, "Did you like our service?", reply_markup=kb)


@bot.inline_handler(func= lambda msg: "/btnmsg" in msg.query)
def inbtnmsg(message):
    kb = InlineKeyboardMarkup([
    [InlineKeyboardButton("Yes",callback_data="reply_yes"),
    InlineKeyboardButton("No", callback_data='reply_no')],
    [InlineKeyboardButton("Get Appointment", callback_data='reply_appointment')]
    ])
    msg = "Did you like our service?"
    reply = InlineQueryResultArticle(id=1, title="ServiceFeedback",input_message_content=InputTextMessageContent(msg), reply_markup=kb)
    bot.answer_inline_query(message.id,[reply])


@bot.callback_query_handler(func=lambda msg: True)
def reply_btn(query):
    global STAT
    data = query.data
    querym = query.message
    try:
        if data == "reply_yes":
            bot.answer_callback_query(query.id)
            bot.send_message(querym.chat.id,"Thank you for your feedback!!!")
        elif data == "reply_no":
            bot.answer_callback_query(query.id)
            bot.send_message(querym.chat.id, "We are sorry about that, in a hoope to mould us perfect can you please share with us the reason of your disatisfaction.")
            STAT = "reply_no"
        elif data == "reply_appointment":
            bot.answer_callback_query(query.id)
            bot.send_message(querym.chat.id, "Sure, an appointment will be booked with the next 24 hours.")
            cont = f"An appointment request from {querym.chat.first_name} {querym.chat.last_name} ({querym.chat.username})"
            bot.send_message("968005905", cont)
            disc_appreq(cont)
    except:
        if data == "reply_yes":
            bot.answer_callback_query(query.id)
            bot.send_message(query.from_user.id,"Thank you for your feedback!!!")
        elif data == "reply_no":
            bot.answer_callback_query(query.id)
            bot.send_message(query.from_user.id, "We are sorry about that, in a hoope to mould us perfect can you please share with us the reason of your disatisfaction.")
            STAT = "reply_no"
        elif data == "reply_appointment":
            bot.answer_callback_query(query.id)
            bot.send_message(query.from_user.id, "Sure, an appointment will be booked with the next 24 hours.")
            cont = f"An appointment request from {query.from_user.first_name} {query.from_user.last_name} ({query.from_user.username})"
            bot.send_message("968005905", cont)
            disc_appreq(cont)



@bot.message_handler(commands=["pay"])
def pay(message):
    bot.reply_to(message)


def _Calc(expr):
    try:
        val = eval(expr)
    except:
        val = "Unexpected Input"
    return val


@bot.inline_handler(func=lambda msg: "/calc" in msg.query)
def incalc(message):
    ctxt = message.query.lstrip('/calc').strip()
    val = _Calc(ctxt)
    rply1 = InlineQueryResultArticle(id=1, title="Result",input_message_content=InputTextMessageContent(val),description=val)
    rply2 = InlineQueryResultArticle(id=2, title="Result with qn",input_message_content=InputTextMessageContent(f"{ctxt}\n{val}"),description=ctxt+"\n"+str(val))
    bot.answer_inline_query(message.id,[rply1,rply2])


@bot.message_handler(commands=["calc"])
def calc(message):
    global STAT
    STAT = "calc"
    bot.reply_to(message, "Please enter your math python expression")


@bot.message_handler(func=lambda msg: "thank you" in msg.text or "thanks" in msg.text or "tq" in msg.text)
def welc(message):
    bot.reply_to(message, "My pleasure !!!")


@bot.message_handler(commands=["changett"])
def changett(message):
    createTB(DBN,"tt"+str(message.chat.id),("day","p1","p2","p3","p4","p5"))
    bot.send_message(message.chat.id,"Send your data in this format..."+"\np1,p2,p3,p4,..."*6+"\n*Each line represents a day of week from monday to saturday*\n*Max 5 periods a day, 6 days(MON to SAT).*")
    ### have to think of something that allows me to get further messages ###
    global STAT
    STAT = "changett"
    

@bot.message_handler(commands=["weektt"])
def weektt(message):
    res = getData(DBN,"tt"+str(message.chat.id),"*")
    res = res[-6:]
    resf = ""
    for r in res:
        resf += f"{r[0]} --> {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]}\n"
    bot.reply_to(message,resf)


@bot.message_handler(commands=["todaytt"])
def todaytt(message):
    y = datetime.today().strftime("%Y")
    m = datetime.today().strftime("%m")
    d = datetime.today().strftime("%d")
    day = date(int(y),int(m),int(d)).strftime('%A')
    rest = getData(DBN,"tt"+str(message.chat.id),"*",f"day='{day}'")
    fin = ""
    for a,b,c,d,e,f in (rest[0],):
        fin += f"{a} --> {b}, {c}, {d}, {e}, {f}"
    bot.reply_to(message,fin)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global STAT
    text = ""
    day1=[]; day2=[]; day3=[]; day4=[]; day5=[]; day6=[]
    if STAT == "changett":
        try:
            text = message.text
            dayl = text.split("\n")
            day1 = dayl[0].split(",")
            day2 = dayl[1].split(",")
            day3 = dayl[2].split(",")
            day4 = dayl[3].split(",")
            day5 = dayl[4].split(",")
            day6 = dayl[5].split(",")
            msg = f"Updated Time Table !!!\nMonday:{day1}\nTuesday:{day2}\nWednesday:{day3}\nThursday:{day4}\nFriday:{day5}\nSaturday:{day6}"
            STAT = ""
        except:
            msg = "Unexpected input!!!"
        
        while len(day1)<5:
            day1.append("None")
        while len(day2)<5:
            day2.append("None")
        while len(day3)<5:
            day3.append("None")
        while len(day4)<5:
            day4.append("None")
        while len(day5)<5:
            day5.append("None")
        while len(day6)<5:
            day6.append("None")
        
        for a,b,c,d,e in (day1,):
            day1t = ("Monday",a,b,c,d,e)
        for a,b,c,d,e in (day2,):
            day2t = ("Tuesday",a,b,c,d,e)
        for a,b,c,d,e in (day3,):
            day3t = ("Wednesday",a,b,c,d,e)
        for a,b,c,d,e in (day4,):
            day4t = ("Thursday",a,b,c,d,e)
        for a,b,c,d,e in (day5,):
            day5t = ("Friday",a,b,c,d,e)
        for a,b,c,d,e in (day6,):
            day6t = ("Saturday",a,b,c,d,e)
        periods = (day1t,day2t,day3t,day4t,day5t,day6t)
        
        insertData(DBN,"tt"+str(message.chat.id),periods)
        
    elif STAT == "tomorse":
        msg = ttom(message.text)
    
    elif STAT == "frmmorse":
        msg = mtot(message.text)

    elif STAT == "calc":
        msg = _Calc(message.text.strip())
    
    elif STAT == "reply_no":
        cont = f"Feedback from {message.chat.username}\n{message.text}"
        bot.send_message("968005905", cont)
        msg = "Thank you for your feedback!"
        disc_fdbk(cont)

    elif STAT == "encrypt":
        try:
            txt, key = message.text.split("<k>")
        except:
            key = ""
        msg = encrypt(txt,key)

    elif STAT == "decrypt":
        try:
            txt, key = message.text.split("<k>")
        except:
            key=""
        msg = decrypt(txt,key)

    else:
        msg = f"{message.text}?\n sorry, Can't get you..."

    bot.reply_to(message, msg)


def main():
    bot.polling()



if __name__ == '__main__':
    main()