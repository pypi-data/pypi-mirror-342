from db_objects import *
def getDbInstance(host='127.0.0.1',port=3306,user='root',password='password'):
    dbi=DbInstance({
        "host":host,
        "port":port,
        "user":user,
        "password":password
    })
    #
    schema=dbi.addSchema('hub')
    table=schema.addTable('users')
    table.addCol('uid','varchar(50)')
    table.addPkey(table.uid)
    table.addCol('name','varchar(50)')
    table.addIndex(table.name)
    table.addCol('ip','varchar(100)')
    table.addCol('expiry','datetime')
    #
    table=schema.addTable('user_perms')
    table.addCol('uid','varchar(50)')
    table.addIndex(table.uid)
    table.addCol('perm','varchar(50)')
    table.addIndex(table.perm)
    table.addPkey(table.uid,table.perm)
    #
    schema=dbi.addSchema('web_ms')
    table=schema.addTable('ms')
    table.addCol('url','varchar(100)')
    table.addPkey(table.url)
    table.addCol('filepath','varchar(200)')
    table.addCol('msGroup','varchar(100)')
    table.addCol('groupOrder','smallint')
    table.addCol('requiredPerm','varchar(50)')
    table.addCol('icon','mediumtext')
    #
    table=schema.addTable('routing')
    table.addFkeyCol(schema.ms.url)
    table.addCol('host','varchar(100)')
    table.addCol('port','int')
    table.addPkey(table.ms,table.host,table.port)
    table.addCol('pid','int')
    #
    # table=schema.addTable('routers')
    # table.addCol('port','int')
    # table.addPkey(table.port)
    # #
    # table=schema.addTable('user_router_binding')
    # table.addCol('ip','varchar(50)')
    # table.addPkey(table.ip)
    # table.addCol('port','int')
    # table.addCol('time','datetime(6)')
    #
    table=schema.addTable('user_routing')
    table.addCol('uid','varchar(50)')
    table.addFkeyCol(schema.ms.url)
    table.addPkey(table.uid,table.ms)
    table.addCol('host','varchar(100)')
    table.addCol('port','int')
    table.addCol('time','datetime')
    table.addIndex(table.time)
    #
    schema=dbi.addSchema('usage_log')
    table=schema.addTable('t')
    table.addCol('uid','varchar(50)')
    table.addIndex(table.uid)
    table.addCol('url','varchar(100)')
    table.addCol('fullUrl','varchar(768)')
    table.addIndex(table.fullUrl)
    table.addCol('time','datetime(6)')
    table.addIndex(table.time)
    table.addPkey(table.uid,table.url,table.time)
    table.addCol('host','varchar(20)')
    table.addCol('port','int')
    table.addCol('responseSize','bigint')
    table.addCol('responseTime','int')
    table.addCol('error','varchar(1000)')
    table.addCol('body','longtext')
    table.addYmPartitions(datetime.now(),datetime.now()+timedelta(days=10))
    #
    schema=dbi.addSchema('network_traffic')
    table=schema.addTable('t')
    table.addCol('hostname','varchar(100)')
    table.addCol('host','varchar(100)')
    table.addCol('port','int')
    table.addCol('time','datetime(6)')
    table.addPkey(table.host,table.port,table.time)
    table.addCol('pid','int')
    table.addCol('upload','bigint')
    table.addCol('download','bigint')
    table.addYmPartitions(datetime.now(),datetime.now()+timedelta(days=10))
    return dbi
if __name__=='__main__':
    from read_creds import read
    creds=read()
    print(creds)
    dbi=getDbInstance(user=creds['localhost']['user'],
                      password=creds['localhost']['password'])
    dbi.deploy()
    # print(id(dbi.web_ms.routing),dbi.web_ms.routing._a_['multiJoinLinks'])
    # print(id(dbi.web_ms.ms),dbi.web_ms.ms._a_['multiJoinLinks'])
    # print(id(dbi.web_ms.usage_log),dbi.web_ms.usage_log._a_['multiJoinLinks'])
    print(MultiColumn(dbi.web_ms.ms.url,dbi.web_ms.user_routing.uid).str())
    from mysql_query_builder import *
    now=datetime.now()
    ym=(now.year,now.month)
    # sq=Select(dbi.web_ms.routing.host,dbi.usage_log.t.time)\
    #     .where(dbi.usage_log.t.uid.eq('asdf')).str(ym)
    # print(sq)
    # sq=Select(dbi.usage_log.t.time,dbi.web_ms.routing.host)\
    #     .where(dbi.usage_log.t.uid.eq('asdf')).str(ym)
    # print(sq)
    sq=Update(dbi.usage_log.t.error).values(None)\
        .where(dbi.usage_log.t.uid.eq('asdf')).str(ym)
    print(sq)
    sq=Delete(dbi.usage_log.t)\
        .where(dbi.usage_log.t.uid.eq('asdf')).str(ym)
    print(sq)
