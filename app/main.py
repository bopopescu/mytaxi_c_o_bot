import telebot 
from telebot import types 
import mysql.connector
import datetime


mydb = mysql.connector.connect(
  host="apitest.mytaxi.uz",
  user="jamshid_dc",
  passwd="ce90698e0e9ddd0d120edf72f43cb878",
  database="test"
)

mycursor = mydb.cursor()


def get_day_cancel(date):
    sql = f"""SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(from_adres, ',',1), ' ',1)) REGION,
                     DATE_FORMAT(date,'%W') DAY,
                     COUNT(*) ORDERS
              FROM max_taxi_incoming_orders
              WHERE status = '8'
              AND date BETWEEN DATE_SUB(DATE_FORMAT('{date}', '%Y-%m-%d'), INTERVAL 1 day) AND '{date}'
              GROUP BY 1,2
              ORDER BY 3 DESC, 1"""
    
    mycursor.execute(sql)
    result = mycursor.fetchall()


    if len(result) == 0:
        msg = 'Check the date again, the result is empty'
    else:
        mesg = ''
        for i in range(len(result)):
            raw = f'{result[i][1]} |  {result[i][2]}  | {result[i][0]}\n'
            mesg += raw
        
        msg = f'{date}\n   DAY   | CANCELED | REGION\n'
        msg += mesg
    mydb.close()
    return msg

# date = '2019-11-29'
# get_day_cancel(date)


def month_stat(date_m):
    date = f'{date_m}-01'
    sql = f"""SELECT T1.client_id,
                     T3.AVG_COST,
                     T1.S_ORDER_FREQ,
                     T2.C_ORDER_FREQ,
                     T3.AVG_DR_DIS,
                     T3.AVG_DR_TIME
                FROM (SELECT client_id,
                             (AMOUNT/COUNT(*)) S_ORDER_FREQ
                        FROM
                             (SELECT DATE_FORMAT(date, '%Y-%m-%d') DATE,
                                     DATE_FORMAT(date, '%W') WEEKDAY,
                                     COUNT(*) AMOUNT,
                                     client_id
                                FROM max_taxi_incoming_orders
                               WHERE status = 7
                                 AND date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                            GROUP BY 1,4) as tbl
            GROUP BY 1) AS T1
                JOIN (SELECT client_id,
                             (AMOUNT/COUNT(*)) C_ORDER_FREQ
                        FROM
                             (SELECT DATE_FORMAT(date, '%Y-%m-%d') DATE,
                                     DATE_FORMAT(date, '%W') WEEKDAY,
                                     COUNT(*) AMOUNT,
                                     client_id
                                FROM max_taxi_incoming_orders
                               WHERE status = 8
                                 AND date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                            GROUP BY 1,4) as tbl
                        GROUP BY 1) AS T2
                  ON T2.client_id = T1.client_id
                JOIN (SELECT o.client_id,
                             AVG(total_cost) AVG_COST,
                             AVG(driving_time) AVG_DR_TIME,
                             AVG(driving_distance) AVG_DR_DIS
                        FROM max_taxi_orders_details d
                        JOIN max_taxi_incoming_orders o
                          ON o.id = d.order_id
                         AND o.date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                    GROUP BY 1) AS T3
                  ON T3.client_id = T1.client_id
            ORDER BY 2 DESC;"""

    mycursor.execute(sql)
    result = mycursor.fetchall()


    if len(result) == 0:
        msg = 'Check the date again, the result is empty'
    else:
        mesg = ''
        for i in range(len(result)):
            raw = f'  {result[i][0]}  | {round(result[i][2],2)} | {round(result[i][3],2)} | {round(result[i][1],2)} | {round(result[i][4],2)} | {round(result[i][5],2)}\n'
            mesg += raw
        
        msg = f'{date}\nCLIENT_ID|S_O_F |C_O_F | AVG_COST |AVG_DR_DIS|AVG_DR_MIN\n'
        msg += mesg
    mydb.close()
    return msg

# date_m = '2019-01'
# month_stat(date_m)


TOKEN = '1018909192:AAFCCirDJ72yQyTijRNksDxZ0LzeWvSKdik'
bot = telebot.TeleBot(TOKEN)


date_regex = r"^(20|21)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
date_m_regex = r"^(20|21)[0-9]{2}-(0[1-9]|1[0-2])$"


@bot.message_handler(regexp=date_regex)
def task_1(message):
    chat_id = message.chat.id
    date = message.text
    msg = get_day_cancel(date)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(regexp=date_m_regex)
def task_2(message):
    chat_id = message.chat.id
    date_m = message.text
    msg = month_stat(date_m)
    bot.send_message(chat_id, msg)
    return




@bot.message_handler(content_types=['text'])
def recommendation(message):
    chat_id = message.chat.id
    msg = 'Error message!\nIt should be in forms given below:\nFOR TASK1: YYYY-MM-DD\nFOR TASK2: YYYY-MM'
    bot.send_message(chat_id, msg)
    return



if __name__ == "__main__":
    bot.polling(None)
