
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import sessionmaker
from ActivityUsingFlask import config, create_app, create_egn
from . import app1
import pymysql
pymysql.install_as_MySQLdb()


engine = create_egn()

Base = declarative_base()
Base.metadata.create_all(engine)

if __name__ == '__main__':
    app1.run(host='0.0.0.0', debug=app1.config.from_object(config['DEBUG']), threaded=True)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    userName = Column(String(32))
    userPwd = Column(String(64))

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    userName = Column(String(32))
    userPassword = Column(String(64))



@app1.route('/hello')
def hello():
    return 'Hello World'

@app1.route('/')
def hello_world():
    # self.createTable()
    # 父类Base调用所有继承他的子类来创建表结构
    createTableUsingOrm()

    # insert
    insertTableUsingOrm()

    #query
    queryTableUsingOrm()

    #update
    updateTableUsingOrm()

    return 'Hello World!'

def updateTableUsingOrm():
    Session_Class = sessionmaker(bind=engine)
    Session = Session_Class()
    result = Session.query(Admin).first()
    result.userName = "jj"
    Session.commit()
    print(result)

def queryTableUsingOrm():
    Session_Class = sessionmaker(bind=engine)
    Session = Session_Class()
    result = Session.query(Admin).all()
    print("all:")
    for r in result:
        print(r)
    print("first:")
    first = Session.query(Admin).first()
    print(first)
    print("filter:")
    result = Session.query(Admin).filter_by(userName="test1").first()
    print(result)

def insertTableUsingOrm():
    Session_Class = sessionmaker(bind=engine)
    Session = Session_Class()

    t1 = Admin(userName='test1', userPassword='123456')
    t2 = Admin(userName='test2', userPassword='abcdef')

    print(t1.userName, t1.userPassword)
    print(t2.userName, t2.userPassword)

    Session.add(t1)
    Session.add(t2)
    Session.commit()


def createTableUsingOrm():
    Base.metadata.create_all(engine)

def creaateTable():
    engine.execute('create table test1(id int,name varchar(48),salary int not null)')
    engine.execute("insert into test1(id,name,salary) values(1,'zs',88888)")
    result = engine.execute('select * from test1')
    print(result.fetchall())
