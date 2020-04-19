from db import *
import pandas as pd
from datetime import datetime, timedelta


# date = '2018-05'


def get_interval_stat(date_interval):
    
    res = interval_req(date_interval)
    l = len(res)
    clients_list=[]
    sum=0

    for x in range(l):
        if x < (l-1):
            if res[x][0] == res[x+1][0]:
                d1 = res[x][1]
                d2 = res[x+1][1]
                diff = d1 - d2
                delta = timedelta(minutes = 5)
                if diff <= delta:
                    sum=sum+1
                    clients_list.append(res[x][0])

    ls = clients_list
    df = pd.DataFrame(ls)
    df1 = df.sort_values(by=0,ignore_index=True)
    df2=pd.DataFrame()
    df2['client_id']=df1[0]
    df2['canceled']=1
    df3 = df2.groupby('client_id').count()
    df3 = df3.sort_values(by=['canceled'],ascending=False)

    msg = f'date interval: {date_interval}\n\n\t{df3}\n\noverall: {sum} canceled orders'

    return msg