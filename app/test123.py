import pandas as pd
from datetime import datetime, timedelta

date = '2018-05'
res = month_stat(date)
l = len(res)
clients_list=[]
sum=0

for x in range(l):
    if x < (l-1):
        if res[x][0] == res[x+1][0]:
#             print(f'{res[x][0]} and {res[x+1][0]}')
#             print(f'day {res[x][1].day}')
            d1 = res[x][1]
            d2 = res[x+1][1]
            diff = d1 - d2
            delta = timedelta(minutes = 5)
            if diff <= delta:
                sum=sum+1
                clients_list.append(res[x][0])
#                 print(f'day {res[x][1].day}\t\t\tn{x}:{sum}')

ls = clients_list
df = pd.DataFrame(ls)
df1 = df.sort_values(by=0,ignore_index=True)
df2=pd.DataFrame()
df2['client_id']=df1[0]
df2['canceled']=1
df3 = df2.groupby('client_id').count()


msg = f'date: {date}\n\n'
msg += f'{df3}\n\noverall: {sum}'

print(msg)