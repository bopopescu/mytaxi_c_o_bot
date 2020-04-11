import mysql.connector 


conn = mysql.connector.connect(
    host="apitest.mytaxi.uz",
    user="jamshid_dc",
    passwd="ce90698e0e9ddd0d120edf72f43cb878",
    database="test"
)

mycur = conn.cursor()

sql = """SELECT client_id, date, from_adres
           FROM max_taxi_incoming_orders
          WHERE status = '8' 
            AND date BETWEEN '2017-05-02' AND '2018-05-02'
       ORDER BY date DESC
          LIMIT 20"""


mycur.execute(sql)
res = mycur.fetchall()


arr = []

arr.extend(res[0])

print(res)


print("test")


print(arr)
