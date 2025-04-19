from date_time import ymTuples,ymdTuples
from datetime import date,datetime
from copy import deepcopy
from datetime import datetime,date,timedelta
import pymysql
import pymysql.cursors
import json
def addOther(ls,other,partition):
    otherType=type(other)
    if otherType==str:
        ls.append("'")
        ls.append(other)
        ls.append("'")
    elif otherType==int:
        ls.append(str(other))
    elif otherType==float:
        ls.append(str(other))
    elif otherType==tuple:
        ls.append(str(other))
    elif otherType==list:
        ls.append(str(tuple(other)))
    elif otherType==dict:
        ls.append("'")
        ls.append(json.dumps(other))
        ls.append("'")
    elif otherType==datetime:
        ls.append("'")
        ls.append(str(other))
        ls.append("'")
    elif otherType==date:
        ls.append("'")
        ls.append(str(other))
        ls.append("'")
    elif other is None:
        ls.append('NULL')
    elif otherType==SqlFunc:
        ls.append(other.str(partition))
    else:
        ls.append(other.str(partition))
class Object():
    def __init__(self,*names):
        self._a_={}
        self._a_['names']=names
        self._a_['actions']=[]
        self._a_['partitions']={}
        self._a_['children']=[]
        self._a_['cols']=[]
        self._a_['ymPartitions']=False
        self._a_['ymdPartitions']=False
    def copy(self):
        new=Object(*self._a_['names'])
        new._a_['actions']=deepcopy(self._a_['actions'])
        new._a_['partitions']=deepcopy(self._a_['partitions'])
        new._a_['children']=deepcopy(self._a_['children'])
        new._a_['cols']=deepcopy(self._a_['cols'])
        new._a_['parent']=self._a_.get('parent')
        new._a_['colType']=self._a_.get('colType')
        return new
    def extract_cols(self,other):
        tp=type(other)
        if tp==Column:
            self._a_['cols'].append(other)
        elif tp==tuple or tp==list:
            for obj in other:
                extract_cols(obj)
        elif tp==SqlFunc:
            self._a_['cols'].extend(other._a_['cols'])
    def As(self,alias):
        new=self.copy()
        new._a_['alias']=alias
        return new
    def eq(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('=',other))
        return new
    def ne(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('!=',other))
        return new
    def gt(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('>',other))
        return new
    def ge(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('>=',other))
        return new
    def lt(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('<',other))
        return new
    def le(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('<=',other))
        return new
    def Is(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('is',other))
        return new
    def IsNot(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('is not',other))
        return new
    def IsNull(self):
        new=self.copy()
        new._a_['actions'].append(('is',None))
        return new
    def IsNotNull(self):
        new=self.copy()
        new._a_['actions'].append(('is not',None))
        return new
    def And(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('and',other))
        return new
    def Or(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('or',other))
        return new
    def In(self,other):
        new=self.copy()
        self.extract_cols(other)
        new._a_['actions'].append(('in',other))
        return new
    def addYmPartitions(self,start,end):
        self._a_['ymPartitions']=True
        self._a_['start']=start
        yms=ymTuples(start,end)
        for ym in yms:
            if type(self).__name__=='Schema':
                raise Exception('you want to add partitions to the table itself')
            self._a_['partitions'][ym]=f'_{ym[0]}{str(ym[1]).zfill(2)}'
    def addYmdPartitions(self,start,end):
        self._a_['ymdPartitions']=True
        self._a_['start']=start
        ymds=ymdTuples(start,end)
        for ymd in ymds:
            self._a_['partitions'][ym]=f'_{ym[0]}{str(ym[1]).zfill(2)}'
            for child in self._a_['children']:
                child._a_['partitions'][ymd]=f'_{str(ymd[2]).zfill(2)}'
    def str(self,partition=None):
        pre=[]
        post=[]
        if partition:
            suffix=self._a_['partitions'].get(partition) or ''
        else:
            suffix=''
        if len(self._a_['names'])>1:
            post.append('(')
            for col in self._a_['names']:
                post.append(col.str(partition))
                post.append(', ')
            post.pop()
            post.append(')')
        else:
            if self._a_.get('colType'):
                post.append(self._a_['parent'].str(partition))
                post.append('.')
                post.append(self._a_['names'][0]+suffix)
            else:
                post.append(self._a_['names'][0]+suffix)
        for action in self._a_['actions']:
            pre.append('(')
            post.append(' ')
            post.append(action[0])
            post.append(' ')
            other=action[1]
            addOther(post,other,partition)
            post.append(')')
        if self._a_.get('alias'):
            post.append(' as ')
            post.append(self._a_['alias'])
        pre=list(reversed(pre))
        pre.extend(post)
        return ''.join(pre)
class Column(Object):
    def __init__(self,name,colType):
        super().__init__(name)
        self._a_['colType']=colType
        self._a_['otherParents']=[]
        self._a_['linkedCols']={}
    def str(self,partition=None):
        ls=[self._a_['parent'].str(partition),'.',
            self._a_['names'][0]]
        return ''.join(ls)
class MultiColumn(Object):
    def __init__(self,*names):
        super().__init__(*names)
class Table(Object):
    def __init__(self,name):
        super().__init__(name)
        self._a_['indexes']=[]
        self._a_['fkeys']=[]
        self._a_['fkeyCols']=[]
        self._a_['linkedCols']=[]
        self._a_['multiJoinLinks']={}
    def addCol(self,name,colType):
        col=Column(name,colType)
        col._a_['parent']=self
        self._a_['children'].append(col)
        self.__setattr__(name,col)
        return col
    def addPkey(self,*cols):
        self._a_['pkey']=cols
    def addIndex(self,*cols):
        self._a_['indexes'].append(cols)
    def addFkeyCol(self,col):
        self._a_['fkeys'].append(len(self._a_['children']))
        newCol=Column(col._a_['parent']._a_['names'][0],col._a_['colType'])
        newCol._a_['origParent']=col._a_['parent']
        newCol._a_['parent']=self
        newCol._a_['origCol']=col
        self._a_['children'].append(newCol)
        self._a_['fkeyCols'].append(newCol)
        otherTable=col._a_['parent']
        otherTable._a_['linkedCols'].append(col)
        col._a_['otherParents'].append(self)
        col._a_['linkedCols'][id(self)]=newCol
        newCol._a_['linkedCols'][id(otherTable)]=col
        self.__setattr__(otherTable._a_['names'][0],newCol)
        self._a_['multiJoinLinks'][id(otherTable)]=[(col,self,otherTable)]
        otherTable._a_['multiJoinLinks'][(id(self))]=[(newCol,otherTable,self)]
        recurseMultiJoin(self,otherTable,[(col,self,otherTable)])
        schema=self._a_['parent']
        for table in schema._a_['children']:
            if table==self: continue
            recurseMultiJoin(table,self,[(newCol,otherTable,self)])
        return col
def recurseMultiJoin(table1,table2,linkingCols):
    for col in table2._a_['fkeyCols']:
        table3=col._a_['origParent']
        if table3==table1: continue
        linkingCols2=[*linkingCols,(col._a_['origCol'],table2,table3)]
        ix=id(table3)
        if ix not in table1._a_['multiJoinLinks'] or \
        len(linkingCols2)<len(table1._a_['multiJoinLinks'][ix]):
            table1._a_['multiJoinLinks'][ix]=linkingCols2
            table3._a_['multiJoinLinks'][id(table1)]=list(reversed(linkingCols2))
            recurseMultiJoin(table1,table3,linkingCols2)
    for col in table2._a_['linkedCols']:
        for table3 in col._a_['otherParents']:
            if table3==table1: continue
            linkingCols2=[*linkingCols,(col._a_['linkedCols'][id(table3)],table2,table3)]
            ix=id(table3)
            if ix not in table1._a_['multiJoinLinks'] or \
            len(linkingCols2)<len(table1._a_['multiJoinLinks'][ix]):
                table1._a_['multiJoinLinks'][ix]=linkingCols2
                table3._a_['multiJoinLinks'][id(table1)]=list(reversed(linkingCols2))
                recurseMultiJoin(table1,table3,linkingCols2)
class Schema(Object):
    def __init__(self,name):
        super().__init__(name)
    def addTable(self,name):
        table=Table(name)
        table._a_['parent']=self
        self.__setattr__(name,table)
        self._a_['children'].append(table)
        return table
class DbInstance():
    def __init__(self,kwargs,):
        self._a_={}
        self._a_['kwargs']=kwargs
        self._a_['children']=[]
        # self._a_['conn']=pymysql.Connection(**kwargs)
    def addSchema(self,name):
        schema=Schema(name)
        schema._a_['parent']=self
        self.__setattr__(name,schema)
        self._a_['children'].append(schema)
        return schema
    def query(self,sql,cursor=None):
        conn=self._a_['conn']=pymysql.Connection(**self._a_['kwargs'])
        if cursor=='dict':
            cursor=pymysql.cursors.DictCursor
        elif cursor is None:
            pass
        else:
            raise Exception('unknown cursor type',cursor)
        crs=self._a_['conn'].cursor(cursor)
        cnt=0
        while True:
            try:
                crs.execute(sql)
                conn.commit()
                break
            except Exception as e:
                print(e)
                if str(e).find('exist')>-1:
                    for schema in self._a_['children']:
                        for table in schema._a_['children']:
                            if table._a_['ymPartitions']:
                                table.addYmPartitions(table._a_['start'],
                                   datetime.now()+timedelta(days=10))
                    if cnt==0:
                        self.deploy()
                        cnt+=1
                    else:
                        raise e
                else:
                    raise e
        conn.close()
        return crs
    def deploy(self):
        self._a_['conn']=pymysql.Connection(**self._a_['kwargs'])
        crs=self._a_['conn'].cursor()
        def doTable(partition):
            sq=[f"create table {schema.str(partition)}.{table.str(partition)}("]
            for jx,col in enumerate(table._a_['children']):
                if jx in table._a_['fkeys']:
                    sq.append(col._a_['origParent'].str())
                else:
                    sq.append(col._a_['names'][0])
                sq.append(' ')
                sq.append(col._a_['colType'])
                sq.append(', ')
            sq.pop()
            sq.append(', primary key (')
            for col in table._a_['pkey']:
                if col in table._a_['fkeyCols']:
                    sq.append(col._a_['origParent'].str())
                else:
                    sq.append(col._a_['names'][0])
                sq.append(',')
            sq.pop()
            sq.append(')')
            sq.append(', ')
            for jx in table._a_['fkeys']:
                sq.append(' foreign key (')
                col=table._a_['children'][jx]
                # sq.append(col._a_['names'][0])
                sq.append(col._a_['origParent'].str())
                sq.append(') references ')
                sq.append(col._a_['origParent']._a_['parent'].str(partition))
                sq.append('.')
                sq.append(col._a_['origParent'].str(partition))
                sq.append('(')
                sq.append(col._a_['origCol']._a_['names'][0])
                sq.append(')')
                sq.append(', ')
            sq.pop()
            sq.append(')')
            sq=''.join(sq)
            print(sq)
            try:
                crs.execute(sq)
            except pymysql.err.OperationalError as e:
                if str(e).find('exists')>-1:
                    pass
                else:
                    raise e
            for index in table._a_['indexes']:
                sq=[f'create index ']
                for col in index:
                    sq.append(col._a_['names'][0])
                    sq.append('__')
                sq.pop()
                sq.append(f' on {schema.str(partition)}.{table.str(partition)} (')
                for col in index:
                    sq.append(col._a_['names'][0])
                    sq.append(',')
                sq.pop()
                sq.append(')')
                sq=''.join(sq)
                print(sq)
                try:
                    crs.execute(sq)
                except pymysql.err.OperationalError as e:
                    if str(e).find('Duplicate')>-1:
                        pass
                    else:
                        raise e
        for schema in self._a_['children']:
            if schema._a_['partitions']:
                for partition in schema._a_['partitions']:
                    sq=f'create schema {schema.str(partition)}'
                    print(sq)
                    try:
                        crs.execute(sq)
                    except pymysql.err.ProgrammingError as e:
                        if str(e).find('exists')>-1:
                            pass
                        else:
                            raise e
            else:
                sq=f'create schema {schema.str()}'
                print(sq)
                try:
                    crs.execute(sq)
                except pymysql.err.ProgrammingError as e:
                    if str(e).find('exists')>-1:
                        pass
            for table in schema._a_['children']:
                if table._a_['partitions']:
                    for partition in table._a_['partitions']:
                        doTable(partition)
                else:
                    doTable(None)
        self._a_['conn'].close()

class SqlFunc(Object):
    def __init__(self):
        super().__init__()
    def __getattr__(self, item):
        new=SqlFunc()
        new._a_['name']=item
        new._a_['args']=None
        new._a_['cols']=[]
        return new
    def __call__(self, *args):
        self._a_['args']=args
        for a in args:
            self.extract_cols(a)
        return self
    def str(self,partition=None):
        ls=[self._a_['name'],'(']
        if self._a_['args']:
            for a in self._a_['args']:
                ls.append(a.str(partition))
                ls.append(',')
            ls.pop()
        ls.append(')')
        return ''.join(ls)
SQL=SqlFunc()
class QuotedString(Object):
    def __init(self):
        super().__init__()
    def __call__(self, quotedString):
        new=QuotedString()
        new._a_['name']=quotedString
        return new
    def As(self,alias):
        self._a_['alias']=alias
        return self
    def str(self,partition=None):
        ls=["'",self._a_['name'],"'"]
        if self._a_.get('alias'):
            ls.append(' as ')
            ls.append(self._a_['alias'])
        return ''.join(ls)
QS=QuotedString()
if __name__=='__main__':
    print(SQL.unix_timestamp(SQL.now()).str())
    print(QS('asdf').As('s').str())