# coding:utf-8
import random
from datetime import datetime
from sqlalchemy import text,TIMESTAMP

from api.models.models import Base_model
from api.exts import db
from sqlalchemy.dialects.mysql import DOUBLE,LONGTEXT
# 个人信息
class hisyearscore(Base_model):
    __doc__ = u'''hisyearscore'''
    __tablename__ = 'hisyearscore'



    __authTables__={}
    __authPeople__='否'
    __authSeparate__='否'
    __thumbsUp__='是'
    __intelRecom__='用协'
    __browseClick__='是'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    specname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='专业名称' )
    speccode=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='专业代码' )
    schoolname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='院校名称' )
    nianfen=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='年份' )
    departname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='招生院系' )
    specremark=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='研究方向' )
    totalscore=db.Column( db.Integer, default=0 ,  nullable=True, unique=False,comment='总分' )
    politics=db.Column( db.Integer, default=0 ,  nullable=True, unique=False,comment='政治' )
    english=db.Column( db.Integer, default=0 ,  nullable=True, unique=False,comment='外语' )
    specialone=db.Column( db.Integer, default=0 ,  nullable=True, unique=False,comment='专业课一' )
    specialtwo=db.Column( db.Integer, default=0 ,  nullable=True, unique=False,comment='专业课二' )
    degreetype=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='学位类别' )
    thumbsupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='赞' )
    crazilynum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='踩' )
    clicktime=db.Column( db.DateTime,  nullable=True, unique=False,comment='最近点击时间' )
    clicknum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='点击次数' )
    discussnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='评论数' )
    storeupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='收藏数' )

class yonghu(Base_model):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='zhanghao'


    __authTables__={}
    __authPeople__='是'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    zhanghao=db.Column( db.VARCHAR(255), nullable=False,unique=True,comment='账号' )
    mima=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='密码' )
    xingming=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='姓名' )
    xingbie=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='性别' )
    shouji=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='手机' )
    touxiang=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )

class kaoyanyixiang(Base_model):
    __doc__ = u'''kaoyanyixiang'''
    __tablename__ = 'kaoyanyixiang'



    __authTables__={'zhanghao':'yonghu',}
    __authPeople__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    zhanghao=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='账号' )
    xingming=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='姓名' )
    xingbie=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='性别' )
    touxiang=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    xueli=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='学历' )
    zhuanye=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='专业' )
    yixiangcengci=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='意向层次' )
    chengjifenshu=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='成绩分数' )
    suozaidi=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='所在地' )
    kexuandi=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='可选地' )
    dengjishijian=db.Column( db.DateTime,  nullable=True, unique=False,comment='登记时间' )
    yixiangpianhao=db.Column( db.Text,  nullable=True, unique=False,comment='意向偏好' )
    yixiangxiangqing=db.Column( db.Text,  nullable=True, unique=False,comment='意向详情' )

class tuijianyuanxiao(Base_model):
    __doc__ = u'''tuijianyuanxiao'''
    __tablename__ = 'tuijianyuanxiao'



    __authTables__={'zhanghao':'yonghu',}
    __authPeople__='否'
    __authSeparate__='否'
    __thumbsUp__='否'
    __intelRecom__='否'
    __browseClick__='否'
    __foreEndListAuth__='否'
    __foreEndList__='是'
    __isAdmin__='否'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    tuijianbiaoti=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='推荐标题' )
    tuijiantupian=db.Column( db.Text,  nullable=True, unique=False,comment='推荐图片' )
    schoolname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='院校名称' )
    specname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='专业名称' )
    speccode=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='专业代码' )
    diqu=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='地区' )
    yuanxiaocengci=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='院校层次' )
    luqufenshuxian=db.Column( db.Float, default=0 ,  nullable=True, unique=False,comment='录取分数线' )
    luqubili=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='录取比例' )
    tuijianshijian=db.Column( db.DateTime,  nullable=True, unique=False,comment='推荐时间' )
    tuijianxiangqing=db.Column( db.Text,  nullable=True, unique=False,comment='推荐详情' )
    zhanghao=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='账号' )
    xingming=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='姓名' )

class syslog(Base_model):
    __doc__ = u'''syslog'''
    __tablename__ = 'syslog'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    username=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='用户名' )
    operation=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='用户操作' )
    method=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='请求方法' )
    params=db.Column( db.Text,  nullable=True, unique=False,comment='请求参数' )
    time=db.Column( db.BigInteger, default=0 ,  nullable=True, unique=False,comment='请求时长(毫秒)' )
    ip=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='IP地址' )

class newstype(Base_model):
    __doc__ = u'''newstype'''
    __tablename__ = 'newstype'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    typename=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='分类名称' )

class news(Base_model):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    __thumbsUp__='是'
    __intelRecom__='是'
    __browseClick__='是'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    title=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='标题' )
    introduction=db.Column( db.Text,  nullable=True, unique=False,comment='简介' )
    typename=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='分类名称' )
    name=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='发布人' )
    headportrait=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    clicknum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='点击次数' )
    clicktime=db.Column( db.DateTime,  nullable=True, unique=False,comment='最近点击时间' )
    thumbsupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='赞' )
    crazilynum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='踩' )
    storeupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='收藏数' )
    picture=db.Column( db.Text, nullable=False, unique=False,comment='图片' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='内容' )

class storeup(Base_model):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    userid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='用户id' )
    refid=db.Column( db.BigInteger, default=0 ,  nullable=True, unique=False,comment='商品id' )
    tablename=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='表名' )
    name=db.Column( db.VARCHAR(255), nullable=False, unique=False,comment='名称' )
    picture=db.Column( db.Text,  nullable=True, unique=False,comment='图片' )
    type=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='类型' )
    inteltype=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='推荐类型' )
    remark=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='备注' )

class messages(Base_model):
    __doc__ = u'''messages'''
    __tablename__ = 'messages'



    __authTables__={}
    __hasMessage__='是'
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    userid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='留言人id' )
    username=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='用户名' )
    avatarurl=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='留言内容' )
    cpicture=db.Column( db.Text,  nullable=True, unique=False,comment='留言图片' )
    reply=db.Column( db.Text,  nullable=True, unique=False,comment='回复内容' )
    rpicture=db.Column( db.Text,  nullable=True, unique=False,comment='回复图片' )

class discusshisyearscore(Base_model):
    __doc__ = u'''discusshisyearscore'''
    __tablename__ = 'discusshisyearscore'



    __authTables__={}
    id = db.Column(db.BigInteger, primary_key=True,autoincrement=False,comment='主键')
    addtime = db.Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    refid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='关联表id' )
    userid=db.Column( db.BigInteger, default=0 , nullable=False, unique=False,comment='用户id' )
    avatarurl=db.Column( db.Text,  nullable=True, unique=False,comment='头像' )
    nickname=db.Column( db.VARCHAR(255),  nullable=True, unique=False,comment='用户名' )
    content=db.Column( db.Text, nullable=False, unique=False,comment='评论内容' )
    reply=db.Column( db.Text,  nullable=True, unique=False,comment='回复内容' )
    thumbsupnum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='赞' )
    crazilynum=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='踩' )
    istop=db.Column( db.Integer,default=0 ,  nullable=True, unique=False,comment='置顶(1:置顶,0:非置顶)' )
    tuserids=db.Column( db.Text,  nullable=True, unique=False,comment='赞用户ids' )
    cuserids=db.Column( db.Text,  nullable=True, unique=False,comment='踩用户ids' )

