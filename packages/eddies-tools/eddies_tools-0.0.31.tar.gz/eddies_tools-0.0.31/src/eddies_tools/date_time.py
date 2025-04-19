from datetime import datetime,timedelta
def checkDate(dt):
    if type(dt)==str:
        dt=dt.split('-')
        dt=(int(a) for a in dt)
        dt=datetime(*dt)
        return dt
    return dt
def ymTuples(start,end):
    start=checkDate(start)
    end=checkDate(end)
    current=start
    yms=[]
    while current<=end:
        ym=(current.year,current.month)
        yms.append(ym)
        current+=timedelta(days=32)
        current=datetime(current.year,current.month,1)
    return yms
def ymdTuples(start,end):
    start=checkDate(start)
    end=checkDate(end)
    current=start
    ymds=[]
    while current<=end:
        ymd=(current.year,current.month,current.day)
        ymds.append(ymd)
        current+=timedelta(days=1)
    return ymds
if __name__=='__main__':
    print(ymTuples('2020-01-01','2021-01-01'))