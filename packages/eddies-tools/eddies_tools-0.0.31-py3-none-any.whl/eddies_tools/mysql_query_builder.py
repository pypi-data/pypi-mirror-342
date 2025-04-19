import traceback

from date_time import ymTuples
from db_objects import *
class Select:
    def __init__(self,*cols):
        self.cols=cols
        self.distinct_=False
        self.includePartition_=False
        self.condition=None
        self.tables=[]
        for col in self.cols:
            tp=type(col)
            if tp==Column:
                table=col._a_['parent']
                if table not in self.tables:
                    self.tables.append(table)
            elif tp==MultiColumn:
                for col2 in col._a_['names']:
                    table=col2._a_['parent']
                    if table not in self.tables:
                        self.tables.append(table)
            elif tp==SqlFunc:
                for col2 in col._a_['cols']:
                    table=col2._a_['parent']
                    if table not in self.tables:
                        self.tables.append(table)
    def distinct(self):
        self.distinct_=True
        return self
    def includePartition(self):
        self.includePartition_=True
        return self
    def where(self,condition):
        self.condition=condition
        for col in self.condition._a_['cols']:
            table=col._a_['parent']
            if table not in self.tables:
                self.tables.append(table)
        return self
    def str(self,partition=None):
        stack=traceback.format_stack()[-2].replace('\n','')
        ls=['select ',
            f'/*{stack}*/ ',
            ]
        if self.distinct_:
            ls.append('distinct ')
        for col in self.cols:
            ls.append(col.str(partition))
            ls.append(',')
        ls.pop()
        ls.append(' from ')
        table0=self.tables[0]
        ls.append(table0._a_['parent'].str(partition))
        ls.append('.')
        ls.append(table0.str(partition))
        done=[table0]
        for table1 in self.tables[1:]:
            if table1 in done: continue
            joins=table0._a_['multiJoinLinks'].get(id(table1))
            if joins is None:
                raise Exception('could not join '
                                +table0._a_['parent'].str()
                                +'.'
                                +table0.str()
                                +' to '
                                +table1._a_['parent'].str()
                                +'.'
                                +table1.str())
            for col,t1,t2 in joins:
                col2=col._a_['linkedCols'][id(t1)]
                if t1 in done:
                    ls.append(' join ')
                    ls.append(t2._a_['parent'].str(partition))
                    ls.append('.')
                    ls.append(t2.str(partition))
                    ls.append(' on ')
                    ls.append(col.str(partition))
                    ls.append('=')
                    ls.append(col2.str(partition))
                    done.append(t2)
                else:
                    ls.append(' join ')
                    ls.append(t1._a_['parent'].str(partition))
                    ls.append('.')
                    ls.append(t1.str(partition))
                    ls.append(' on ')
                    ls.append(col.str(partition))
                    ls.append('=')
                    ls.append(col2.str(partition))
                    done.append(t1)
        if self.condition:
            ls.append(' where ')
            ls.append(self.condition.str(partition))
        return ''.join(ls)
class Update:
    def __init__(self,*cols):
        self.cols=cols
        self.table=cols[0]._a_['parent']
    def values(self,*vals):
        self.vals=vals
        return self
    def where(self,condition):
        self.condition=condition
        return self
    def str(self,partition=None):
        stack=traceback.format_stack()[-2].replace('\n','')
        ls=['update ',
            f'/*{stack}*/ ',
            self.table.str(partition),' set ']
        if len(self.cols)!=len(self.vals):
            raise Exception('column count does not match value count')
        for c,v in zip(self.cols,self.vals):
            ls.append(c.str(partition))
            ls.append('=')
            addOther(ls,v,partition)
        if not self.condition:
            raise Exception('blanket update not allowed')
        ls.append(' where ')
        ls.append(self.condition.str(partition))
        return ''.join(ls)
class Insert:
    def __init__(self,*cols):
        self.cols=cols
        self.table=cols[0]._a_['parent']
        self.duplicateUpdateCols=None
    def values(self,*vals):
        self.vals=vals
        return self
    def on_duplicate_update(self,*duplicateUpdateCols):
        self.duplicateUpdateCols=duplicateUpdateCols
        return self
    def str(self,partition=None):
        stack=traceback.format_stack()[-2].replace('\n','')
        ls=['insert ',
            f'/*{stack}*/ ',
            self.table._a_['parent'].str(partition),
            '.',
            self.table.str(partition),
            ' (']
        for val in self.vals:
            if len(self.cols)!=len(val):
                raise Exception('column count does not match value count')
        for col in self.cols:
            ls.append(col.str(partition))
            ls.append(',')
        ls.pop()
        ls.append(') values ')
        for val in self.vals:
            ls.append('(')
            for v in val:
                addOther(ls,v,partition)
                ls.append(',')
            ls.pop()
            ls.append(')')
            ls.append(',')
        ls.pop()
        ls.append(' as new ')
        if self.duplicateUpdateCols:
            ls.append(' on duplicate key update ')
            for col in self.duplicateUpdateCols:
                ls.append(col.str())
                ls.append('=new.')
                ls.append(col._a_['names'][0])
                ls.append(',')
            ls.pop()
        return ''.join(ls)
class Delete:
    def __init__(self,table):
        self.table=table
    def where(self, condition):
        self.condition=condition
        return self
    def str(self,partition=None):
        stack=traceback.format_stack()[-2].replace('\n','')
        ls=['delete ',
            f'/*{stack}*/ ',
            'from ',self.table.str(partition),' where ']
        if not self.condition:
            raise Exception('blanket delete not allowed')
        ls.append(' where ')
        ls.append(self.condition.str(partition))
        return ''.join(ls)
