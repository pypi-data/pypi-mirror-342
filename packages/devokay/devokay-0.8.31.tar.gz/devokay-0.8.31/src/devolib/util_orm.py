import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)
from sqlalchemy.ext.declarative import declarative_base

# 基础类
Base = declarative_base()

'''
@brief 操作封装
'''

class UtilOrm:
    _engine = None
    _session = None

    def __init__(self) -> None:
        # 创建引擎
        _engine = create_engine(
            "mysql+pymysql://tom:123@192.168.0.120:3306/db1?charset=utf8mb4",
            # "mysql+pymysql://tom@127.0.0.1:3306/db1?charset=utf8mb4", # 无密码时
            # 超过链接池大小外最多创建的链接
            max_overflow=0,
            # 链接池大小
            pool_size=5,
            # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
            pool_timeout=10,
            # 多久之后对链接池中的链接进行一次回收
            pool_recycle=1,
            # 查看原生语句（未格式化）
            echo=True
        )

        # 绑定引擎
        Session = sessionmaker(bind=_engine)

        # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
        # 内部会采用threading.local进行隔离
        _session = scoped_session(Session)

    # 创建表
    def start(self):
        # 如果没有scheme就创建

        # 如果没有表，就创建    
        Base.metadata.create_all(self._engine)

    # 停止，关闭资源
    def stop(self):
        self._session.close()

    # 删除表
    def drop_all(self):
        
        Base.metadata.drop_all(self._engine)

    # 添加一个
    def add_one(self, model):
        self._session.add(model)
        self._session.commit()

    # 添加一组
    def add_many(self, models):
        self._session.add_all(
            (
                user_instance1,
                user_instance2
            )
        )
        self._session.commit()

    # 删除记录
    def delete_one(self):
        pass
    def delete_many(self):
        pass

    # 更新
    def save_one(self):
        pass


'''
@brief 配置表
'''

class DevoConf(Base):
    """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "userInfo"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(32), index=True, nullable=False, comment="姓名")
    age = Column(Integer, nullable=False, comment="年龄")
    phone = Column(DECIMAL(6), nullable=False, unique=True, comment="手机号")
    address = Column(String(64), nullable=False, comment="地址")
    # 对于非必须插入的字段，不用采取nullable=False进行约束
    gender = Column(Enum("male", "female"), default="male", comment="性别")
    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")
    last_update_time = Column(
        DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")
    delete_status = Column(Boolean(), default=False,
                           comment="是否删除")

    __table__args__ = (
        UniqueConstraint("name", "age", "phone"),  # 联合唯一约束
        Index("name", "addr", unique=True),       # 联合唯一索引
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.name}>"
    
# user_instance = models.UserInfo(
#     name="Jack",
#     age=18,
#     phone=330621,
#     address="Beijing",
#     gender="male"
# )