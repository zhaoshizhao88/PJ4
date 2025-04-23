# coding:utf-8
__author__ = "ila"

import logging, os, json, configparser
import time
import numbers
import requests
from werkzeug.utils import redirect

from flask import request, jsonify,session
from sqlalchemy.sql import func,and_,or_,case
from sqlalchemy import cast, Integer,Float
from api.models.brush_model import *
from . import main_bp
from utils.codes import *
from utils.jwt_auth import Auth
from configs import configs
from utils.helper import *
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from utils.baidubce_api import BaiDuBce
from api.models.config_model import config
from flask import current_app as app
from utils.spark_func import spark_read_mysql
from utils.hdfs_func import upload_to_hdfs
from utils.mapreduce1 import MRMySQLAvg
import pandas as pd
# 注册接口
@main_bp.route("/python75f6hd0t/hisyearscore/register", methods=['POST'])
def python75f6hd0t_hisyearscore_register():
    if request.method == 'POST':#post请求
        msg = {'code': normal_code, 'message': 'success', 'data': [{}]}
        req_dict = session.get("req_dict")


        #创建新用户数据
        error = hisyearscore.createbyreq(hisyearscore, hisyearscore, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = "注册用户已存在"
        else:
            msg['data'] = error
        #返回结果
        return jsonify(msg)

# 登录接口
@main_bp.route("/python75f6hd0t/hisyearscore/login", methods=['GET','POST'])
def python75f6hd0t_hisyearscore_login():
    if request.method == 'GET' or request.method == 'POST':#get、post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取用户名和密码参数
        req_dict = session.get("req_dict")
        req_model = session.get("req_dict")
        try:
            del req_model['role']
        except:
            pass
        #根据用户名获取用户数据
        datas = hisyearscore.getbyparams(hisyearscore, hisyearscore, req_model)
        if not datas:#如果为空则代表账号密码错误或用户不存在
            msg['code'] = password_error_code
            msg['msg']='密码错误或用户不存在'
            return jsonify(msg)


        req_dict['id'] = datas[0].get('id')
        try:
            del req_dict['mima']
        except:
            pass

        #新建用户缓存数据并返回结果
        return Auth.authenticate(Auth, hisyearscore, req_dict)


# 登出接口
@main_bp.route("/python75f6hd0t/hisyearscore/logout", methods=['POST'])
def python75f6hd0t_hisyearscore_logout():
    if request.method == 'POST':#post请求
        msg = {
            "msg": "退出成功",
            "code": 0
        }
        req_dict = session.get("req_dict")

        return jsonify(msg)

# 重置密码接口
@main_bp.route("/python75f6hd0t/hisyearscore/resetPass", methods=['POST'])
def python75f6hd0t_hisyearscore_resetpass():
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success"}
        #获取传递的参数
        req_dict = session.get("req_dict")

        if req_dict.get('mima') != None:
            req_dict['mima'] = '123456'
        #更新重置后的密码
        error = hisyearscore.updatebyparams(hisyearscore, hisyearscore, req_dict)

        if error != None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['msg'] = '密码已重置为：123456'
        return jsonify(msg)

# 获取会话信息接口
@main_bp.route("/python75f6hd0t/hisyearscore/session", methods=['GET'])
def python75f6hd0t_hisyearscore_session():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "data": {}}
        #获取token里的id，查找对应的用户数据返回
        req_dict={"id":session.get('params').get("id")}
        msg['data']  = hisyearscore.getbyparams(hisyearscore, hisyearscore, req_dict)[0]

        return jsonify(msg)

# 分类接口（后端）
@main_bp.route("/python75f6hd0t/hisyearscore/page", methods=['GET'])
def python75f6hd0t_hisyearscore_page():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        userinfo = session.get("params")
        try:#判断是否有消息
            __hasMessage__=hisyearscore.__hasMessage__
        except:
            __hasMessage__=None
        if __hasMessage__ and __hasMessage__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None and hisyearscore!='chat':
                req_dict["userid"]=session.get("params").get("id")

        tablename=session.get("tablename")
        #非管理员账号则需要判断用户的相应权限
        if tablename!="users" :
            mapping_str_to_object = {}
            for model in Base_model._decl_class_registry.values():
                if hasattr(model, '__tablename__'):
                    mapping_str_to_object[model.__tablename__] = model

            try:#是否有管理员权限
                __isAdmin__=mapping_str_to_object[tablename].__isAdmin__
            except:
                __isAdmin__=None
            try:#是否有用户权限
                __authSeparate__ =mapping_str_to_object[tablename].__authSeparate__
            except:
                __authSeparate__ = None

            if __isAdmin__!="是" and __authSeparate__ == "是" and session.get("params")!=None:
                req_dict["userid"]=session.get("params").get("id")
            else:
                try:
                    del req_dict["userid"]
                except:
                    pass

            # 当前表也是有管理员权限的表
            if  __isAdmin__ == "是" and 'hisyearscore' != 'forum':
                if req_dict.get("userid") and 'hisyearscore' != 'chat':
                    del req_dict["userid"]
            else:
                #非管理员权限的表,判断当前表字段名是否有userid
                if tablename!="users" and 'hisyearscore'[:7]!='discuss'and "userid" in hisyearscore.getallcolumn(hisyearscore,hisyearscore):
                    req_dict["userid"] = session.get("params").get("id")

        clause_args = []
        or_clauses = or_(*clause_args)
        #查询列表数据
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = hisyearscore.page(hisyearscore, hisyearscore, req_dict, or_clauses)
        return jsonify(msg)

# 排序接口
@main_bp.route("/python75f6hd0t/hisyearscore/autoSort", methods=['GET'])
def python75f6hd0t_hisyearscore_autosort():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        req_dict['sort']='clicktime'
        req_dict['order']='desc'

        try:#获取需要排序的内容
            __browseClick__= hisyearscore.__browseClick__
        except:
            __browseClick__=None
        #根据排序字段进行排序
        if __browseClick__ =='是':
            req_dict['sort']='clicknum'
        elif __browseClick__ =='时长':
            req_dict['sort']='browseduration'
        else:
            req_dict['sort']='clicktime'
        #获取排序内容
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = hisyearscore.page(hisyearscore, hisyearscore, req_dict)

        return jsonify(msg)

#查询单条数据
@main_bp.route("/python75f6hd0t/hisyearscore/query", methods=['GET'])
def python75f6hd0t_hisyearscore_query():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{}}
        #获取传递的参数，根据参数获取单条结果
        req_dict = session.get("req_dict")
        query = db.session.query(hisyearscore)
        for key, value in req_dict.items():
            query = query.filter(getattr(hisyearscore, key) == value)
        query_result = query.first()
        query_result.__dict__.pop('_sa_instance_state', None)
        msg['data'] = query_result.__dict__
        return jsonify(msg)

# 分页接口（前端）
@main_bp.route("/python75f6hd0t/hisyearscore/list", methods=['GET'])
def python75f6hd0t_hisyearscore_list():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":10,"list":[]}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        if req_dict.__contains__('vipread'):
            del req_dict['vipread']
            
        userinfo = session.get("params")

        try:#判断是否有列表权限
            __foreEndListAuth__=hisyearscore.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限判断就去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users" and session.get("params")!=None:
                req_dict['userid']=session.get("params").get("id")

        tablename=session.get("tablename")

        if 'luntan' in 'hisyearscore':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]

        if 'discuss' in 'hisyearscore':
            if 'userid' in req_dict.keys():
                del req_dict["userid"]
        #根据封装的req_dict字典去筛选获取列表数据
        msg['data']['list'], msg['data']['currPage'], msg['data']['totalPage'], msg['data']['total'], \
        msg['data']['pageSize']  = hisyearscore.page(hisyearscore, hisyearscore, req_dict)
        return jsonify(msg)

# 保存接口（后端）
@main_bp.route("/python75f6hd0t/hisyearscore/save", methods=['POST'])
def python75f6hd0t_hisyearscore_save():
    request.operation = "新增历年考研分数"#封装日志内容
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        for key in req_dict:#将空值转为None
            if req_dict[key] == '':
                req_dict[key] = None

        #保存数据
        error= hisyearscore.createbyreq(hisyearscore, hisyearscore, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
        else:
            msg['data'] = error
        return jsonify(msg)

# 添加接口（前端）
@main_bp.route("/python75f6hd0t/hisyearscore/add", methods=['POST'])
def python75f6hd0t_hisyearscore_add():
    request.operation = "新增历年考研分数"#封装日志内容
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取参数
        req_dict = session.get("req_dict")
        #判断用户权限
        try:
            __foreEndListAuth__=hisyearscore.__foreEndListAuth__
        except:
            __foreEndListAuth__=None
        #不需要权限则去掉userid
        if __foreEndListAuth__ and __foreEndListAuth__!="否":
            tablename=session.get("tablename")
            if tablename!="users":
                req_dict['userid']=session.get("params").get("id")

        #保存数据
        error= hisyearscore.createbyreq(hisyearscore, hisyearscore, req_dict)
        if error!=None and error is Exception:
            msg['code'] = crud_error_code
            msg['msg'] = error
            return jsonify(msg)
        else:
            msg['data'] = error
        return jsonify(msg)

# 踩、赞接口
@main_bp.route("/python75f6hd0t/hisyearscore/thumbsup/<id_>", methods=['GET'])
def python75f6hd0t_hisyearscore_thumbsup(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        id_=int(id_)
        type_=int(req_dict.get("type",0))
        #获取要踩赞的记录
        rets=hisyearscore.getbyid(hisyearscore, hisyearscore,id_)
        update_dict={
            "id":id_,
        }
        #加减数据
        if type_==1:#赞
            update_dict["thumbsupnum"]=int(rets[0].get('thumbsupnum'))+1
        elif type_==2:#踩
            update_dict["crazilynum"]=int(rets[0].get('crazilynum'))+1
        #更新记录
        error = hisyearscore.updatebyparams(hisyearscore, hisyearscore, update_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 获取详情信息（后端）
@main_bp.route("/python75f6hd0t/hisyearscore/info/<id_>", methods=['GET'])
def python75f6hd0t_hisyearscore_info(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = hisyearscore.getbyid(hisyearscore, hisyearscore, int(id_))
        if len(data)>0:
            msg['data']=data[0]
        #浏览点击次数
        try:
            __browseClick__= hisyearscore.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__  and  "clicknum"  in hisyearscore.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=hisyearscore.updatebyparams(hisyearscore,hisyearscore,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 获取详情信息（前端）
@main_bp.route("/python75f6hd0t/hisyearscore/detail/<id_>", methods=['GET'])
def python75f6hd0t_hisyearscore_detail(id_):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #根据id获取对应记录
        data = hisyearscore.getbyid(hisyearscore, hisyearscore, int(id_))
        if len(data)>0:
            msg['data']=data[0]

        #浏览点击次数
        try:
            __browseClick__= hisyearscore.__browseClick__
        except:
            __browseClick__=None

        if __browseClick__ and "clicknum" in hisyearscore.__table__.columns:
            click_dict={"id":int(id_),"clicknum":str(int(data[0].get("clicknum") or 0)+1)}#增加点击次数
            ret=hisyearscore.updatebyparams(hisyearscore,hisyearscore,click_dict)#更新记录
            if ret!=None:
                msg['code'] = crud_error_code
                msg['msg'] = ret
        return jsonify(msg)

# 更新接口
@main_bp.route("/python75f6hd0t/hisyearscore/update", methods=['POST'])
def python75f6hd0t_hisyearscore_update():
    request.operation = "更新历年考研分数"#填充日志内容
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #如果存在密码或点击次数则不更新
        if req_dict.get("mima") and "mima" not in hisyearscore.__table__.columns :
            del req_dict["mima"]
        if req_dict.get("password") and "password" not in hisyearscore.__table__.columns :
            del req_dict["password"]
        try:
            del req_dict["clicknum"]
        except:
            pass

        #更新记录
        error = hisyearscore.updatebyparams(hisyearscore, hisyearscore, req_dict)
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error

        return jsonify(msg)

# 删除接口
@main_bp.route("/python75f6hd0t/hisyearscore/delete", methods=['POST'])
def python75f6hd0t_hisyearscore_delete():
    request.operation = "删除历年考研分数"#更新日志记录
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #删除记录
        error=hisyearscore.delete(
            hisyearscore,
            req_dict
        )
        if error!=None:
            msg['code'] = crud_error_code
            msg['msg'] = error
        return jsonify(msg)

# 投票接口
@main_bp.route("/python75f6hd0t/hisyearscore/vote/<int:id_>", methods=['POST'])
def python75f6hd0t_hisyearscore_vote(id_):
    if request.method == 'POST':#post请求
        msg = {"code": normal_code, "msg": "success"}
        #根据id获取记录
        data= hisyearscore.getbyid(hisyearscore, hisyearscore, int(id_))
        for i in data:
            #增加投票数并更新记录
            votenum=i.get('votenum')
            if votenum!=None:
                params={"id":int(id_),"votenum":votenum+1}
                error=hisyearscore.updatebyparams(hisyearscore,hisyearscore,params)
                if error!=None:
                    msg['code'] = crud_error_code
                    msg['msg'] = error
        return jsonify(msg)

#分组统计接口
@main_bp.route("/python75f6hd0t/hisyearscore/group/<columnName>", methods=['GET'])
def python75f6hd0t_hisyearscore_group(columnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取传递的参数
        req_dict = session.get("req_dict")
        limit = 0
        order = ""
        if "limit" in req_dict:
            limit = req_dict["limit"]
            del req_dict["limit"]
        if "order" in req_dict:
            order = req_dict["order"]
            del req_dict["order"]
        userinfo = session.get("params")
        #获取hadoop分析后的数据文件
        json_filename = f'hisyearscore_group{columnName}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            #查询记录
            msg['data'] = hisyearscore.groupbycolumnname(hisyearscore,hisyearscore,columnName,req_dict)
            msg['data'] = msg['data'][:10]
            msg['data'] = [ {**i,columnName:str(i[columnName])} if columnName in i else i for i in msg['data']]
        #对结果进行升序可降序排序
        if order == "desc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
        elif order == "asc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])
        #截取列表个数
        if 0 < int(limit) < len(msg['data']):
            msg['data'] = msg['data'][:int(limit)]
        return jsonify(msg)#返回封装的json结果

# 按值统计接口
@main_bp.route("/python75f6hd0t/hisyearscore/value/<xColumnName>/<yColumnName>", methods=['GET'])
def python75f6hd0t_hisyearscore_value(xColumnName, yColumnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        #获取参数
        req_dict = session.get("req_dict")
        limit = 0
        order = ""
        if "limit" in req_dict:
            limit = req_dict["limit"]
            del req_dict["limit"]
        if "order" in req_dict:
            order = req_dict["order"]
            del req_dict["order"]
        userinfo = session.get("params")
        #获取hadoop分析后的数据文件
        json_filename = f'hisyearscore_value{xColumnName}{yColumnName}.json'
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            #查询记录
            msg['data'] = hisyearscore.getvaluebyxycolumnname(hisyearscore,hisyearscore,xColumnName,yColumnName,req_dict)
            msg['data'] = msg['data'][:10]
        #对结果进行升序可降序排序
        if order == "desc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
        elif order == "asc":
            msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])
        #截取列表个数
        if 0 < int(limit) < len(msg['data']):
            msg['data'] = msg['data'][:int(limit)]
        return jsonify(msg)#返回封装的json结果

# 按日期统计接口
@main_bp.route("/python75f6hd0t/hisyearscore/value/<xColumnName>/<yColumnName>/<timeStatType>", methods=['GET'])
def python75f6hd0t_hisyearscore_value_riqi(xColumnName, yColumnName, timeStatType):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": {}}
        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"
        json_filename = f'hisyearscore_value{xColumnName}{yColumnName}{date_type}.json'

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            #定义查询统计语句
            for key, value in req_dict.items():
                if key!="limit" and key!="order":
                    where = where + " and {0} ='{1}' ".format(key,value)
            sql = ''
            if timeStatType == '日':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, yColumnName, where, '%Y-%m-%d')

            if timeStatType == '月':
                sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, yColumnName, where, '%Y-%m')

            if timeStatType == '季':
                sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) AS {0}, SUM({1}) AS total FROM orders {2} GROUP BY YEAR({0}), QUARTER({0})".format(xColumnName, yColumnName, where)

            if timeStatType == '年':
                sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, yColumnName, where, '%Y')
            #执行查询
            data = db.session.execute(sql)
            data = data.fetchall()
            #封装结果
            results = []
            for i in range(len(data)):
                result = {
                    xColumnName: decimalEncoder(data[i][0]),
                    'total': decimalEncoder(data[i][1])
                }
                results.append(result)

            msg['data'] = results
            json_filename='hisyearscore'+f'_value_{xColumnName}_{yColumnName}.json'
            with open(json_filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(results, indent=4, ensure_ascii=False))
            app.executor.submit(upload_to_hdfs, json_filename)
            app.executor.submit(MRMySQLAvg.run)
        req_dict = session.get("req_dict")
        #对结果进行排序
        if "order" in req_dict:
            order = req_dict["order"]
            if order == "desc":
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'],reverse=True)
            else:
                msg['data'] = sorted((x for x in msg['data'] if x['total'] is not None),key=lambda x: x['total'])
        #截取列表个数
        if "limit" in req_dict and int(req_dict["limit"]) < len(msg['data']):
            msg['data'] = msg['data'][:int(req_dict["limit"])]
        return jsonify(msg)#返回封装的json结果

# 按值统计（多）
@main_bp.route("/python75f6hd0t/hisyearscore/valueMul/<xColumnName>", methods=['GET'])
def python75f6hd0t_hisyearscore_valueMul(xColumnName):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        json_filename = f'''hisyearscore_value{xColumnName}{req_dict['yColumnNameMul'].replace(",","")}.json'''
        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            for item in req_dict['yColumnNameMul'].split(','):
                #定义查询语句
                sql = "SELECT {0}, sum({1}) AS total FROM hisyearscore {2} GROUP BY {0} LIMIT 10".format(xColumnName, item, where)
                L = []
                #执行查询
                data = db.session.execute(sql)
                data = data.fetchall()
                for i in range(len(data)):
                    result = {
                        xColumnName: decimalEncoder(data[i][0]),
                        'total': decimalEncoder(data[i][1])
                    }
                    L.append(result)
                msg['data'].append(L)
        return jsonify(msg)

# 按值统计（多）
@main_bp.route("/python75f6hd0t/hisyearscore/valueMul/<xColumnName>/<timeStatType>", methods=['GET'])
def python75f6hd0t_hisyearscore_valueMul_time(xColumnName,timeStatType):
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}

        req_dict = session.get("req_dict")
        #获取hadoop分析后的数据文件
        date_type = ""
        if timeStatType == '日':
            date_type = "date"
        if timeStatType == '月':
            date_type = "month"
        if timeStatType == '季':
            date_type = "quarter"
        if timeStatType == '年':
            date_type = "year"

        json_filename = f'''hisyearscore_value{xColumnName}{req_dict['yColumnNameMul'].replace(",","")}{date_type}.json'''

        if os.path.exists(json_filename) == True:
            with open(json_filename, encoding='utf-8') as f:
                msg['data'] = json.load(f)
        else:
            userinfo = session.get("params")
            where = ' where 1 = 1 '
            for item in req_dict['yColumnNameMul'].split(','):
                #定义查询语句
                sql = ''
                if timeStatType == '日':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d') LIMIT 10".format(xColumnName, item, where, '%Y-%m-%d')

                if timeStatType == '月':
                    sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y-%m') LIMIT 10".format(xColumnName, item, where, '%Y-%m')

                if timeStatType == '季':
                    sql = "SELECT CONCAT(YEAR(MIN({0})), '-Q', QUARTER(MIN({0}))) {0}, sum({1}) total FROM hisyearscore {2} GROUP BY YEAR({0}), QUARTER({0}) LIMIT 10".format(xColumnName, item, where)

                if timeStatType == '年':
                    sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM hisyearscore {2} GROUP BY DATE_FORMAT({0}, '%Y') LIMIT 10".format(xColumnName, item, where, '%Y')
                L = []
                #执行查询
                data = db.session.execute(sql)
                data = data.fetchall()
                for i in range(len(data)):
                    result = {
                        xColumnName: decimalEncoder(data[i][0]),
                        'total': decimalEncoder(data[i][1])
                    }
                    L.append(result)
                msg['data'].append(L)
        return jsonify(msg)

import math
#计算相似度
def cosine_similarity(a, b):
    numerator = sum([a[key] * b[key] for key in a if key in b])
    denominator = math.sqrt(sum([a[key]**2 for key in a])) * math.sqrt(sum([b[key]**2 for key in b]))
    return numerator / denominator

#收藏协同算法
@main_bp.route("/python75f6hd0t/hisyearscore/autoSort2", methods=['GET'])
def python75f6hd0t_hisyearscore_autoSort2():
    if request.method == 'GET':#get请求
        user_ratings = {}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")
        #查询收藏了的记录
        sql = "select * from storeup where type = 1 and tablename = 'hisyearscore' order by addtime desc"
        #执行查询
        data = db.session.execute(sql)
        data_dict = [dict(zip(result.keys(), result)) for result in data.fetchall()]

        for item in data_dict:
            #封装userid、refid的矩阵
            if user_ratings.__contains__(item["userid"]):
                ratings_dict = user_ratings[item["userid"]]
                if ratings_dict.__contains__(item["refid"]):
                    ratings_dict[str(item["refid"])]+=1
                else:
                    ratings_dict[str(item["refid"])] =1
            else:
                user_ratings[item["userid"]] = {
                    str(item["refid"]):1
                }
        sorted_recommended_goods=[]
        try:
            # 计算目标用户与其他用户的相似度
            similarities = {other_user: cosine_similarity(user_ratings[userinfo.get("id")], user_ratings[other_user])
                            for other_user in user_ratings if other_user != userinfo.get("id")}
            # 找到与目标用户最相似的用户
            most_similar_user = sorted(similarities, key=similarities.get, reverse=True)[0]
            # 找到最相似但目标用户未购买过的商品
            recommended_goods = {goods: rating for goods, rating in user_ratings[most_similar_user].items() if
                                 goods not in user_ratings[userinfo.get("id")]}
            # 按评分降序排列推荐
            sorted_recommended_goods = sorted(recommended_goods, key=recommended_goods.get, reverse=True)
        except:
            pass

        L = []
        #按评分顺序查询要推荐列表(当前用户收藏关注过的同类型优先)
        where = " AND ".join([f"{key} = '{value}'" for key, value in req_dict.items() if key!="page" and key!="limit" and key!="order"and key!="sort"])
        if where:
            sql = f'''SELECT * FROM (SELECT * FROM hisyearscore WHERE {where}) AS table1 WHERE id IN ('{"','".join(sorted_recommended_goods)}') union all SELECT * FROM (SELECT * FROM hisyearscore WHERE {where}) AS table1 WHERE id NOT IN ('{"','".join(sorted_recommended_goods)}')'''
        else:
            sql ="select * from hisyearscore where id in ('%s"%("','").join(sorted_recommended_goods)+"') union all select * from hisyearscore where id not in('%s"%("','").join(sorted_recommended_goods)+"')"
        #执行查询
        data = db.session.execute(sql)
        #封装结果
        data_dict = [dict(zip(result.keys(), result)) for result in data.fetchall()]
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                elif 'datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)
        #返回封装的json结果
        return jsonify({"code": 0, "msg": '',  "data":{"currPage":1,"totalPage":1,"total":1,"pageSize":5,"list": L[0:int(req_dict['limit'])]}})


#查询记录总数量接口
@main_bp.route("/python75f6hd0t/hisyearscore/count", methods=['GET'])
def python75f6hd0t_hisyearscore_count():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success",  "data": 0}
        req_dict = session.get("req_dict")
        userinfo = session.get("params")

        #查询记录个数
        msg['data']  = hisyearscore.count(hisyearscore, hisyearscore, req_dict)
        #返回json结果
        return jsonify(msg)


#获取所有记录列表
@main_bp.route("/python75f6hd0t/hisyearscore/lists", methods=['GET'])
def python75f6hd0t_hisyearscore_lists():
    if request.method == 'GET':#get请求
        msg = {"code": normal_code, "msg": "success", "data": []}
        list,_,_,_,_ = hisyearscore.page(hisyearscore,hisyearscore,{})
        msg['data'] = list
        return jsonify(msg)

import math
#数据清洗接口
@main_bp.route("/python75f6hd0t/hisyearscore/cleanse", methods=['GET','POST'])
def python75f6hd0t_hisyearscore_cleanse():
    if request.method == 'GET' or request.method == 'POST':
        msg = {'code': normal_code, 'message': 'success', 'data': {}}
        try:
            #获取要清理的数据列表
            list, _,_,total,_ = hisyearscore.page(hisyearscore, hisyearscore,{})
            df = pd.DataFrame(list)
            #删除空行
            df['specname'].replace([None, ''], pd.NA,inplace = True)
            df.dropna(subset=['specname'],inplace = True)
            #删除空行
            df['speccode'].replace([None, ''], pd.NA,inplace = True)
            df.dropna(subset=['speccode'],inplace = True)
            #随机填充
            df['schoolname'].replace([None, ''], pd.NA,inplace = True)
            schoolname_non_na = df['schoolname'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'schoolname']):
                    df.loc[i, 'schoolname'] = schoolname_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['nianfen'].replace([None, ''], pd.NA,inplace = True)
            nianfen_non_na = df['nianfen'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'nianfen']):
                    df.loc[i, 'nianfen'] = nianfen_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['departname'].replace([None, ''], pd.NA,inplace = True)
            departname_non_na = df['departname'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'departname']):
                    df.loc[i, 'departname'] = departname_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['specremark'].replace([None, ''], pd.NA,inplace = True)
            specremark_non_na = df['specremark'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'specremark']):
                    df.loc[i, 'specremark'] = specremark_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['totalscore'].replace([None, ''], pd.NA,inplace = True)
            totalscore_non_na = df['totalscore'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'totalscore']):
                    df.loc[i, 'totalscore'] = totalscore_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['politics'].replace([None, ''], pd.NA,inplace = True)
            politics_non_na = df['politics'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'politics']):
                    df.loc[i, 'politics'] = politics_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['english'].replace([None, ''], pd.NA,inplace = True)
            english_non_na = df['english'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'english']):
                    df.loc[i, 'english'] = english_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['specialone'].replace([None, ''], pd.NA,inplace = True)
            specialone_non_na = df['specialone'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'specialone']):
                    df.loc[i, 'specialone'] = specialone_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['specialtwo'].replace([None, ''], pd.NA,inplace = True)
            specialtwo_non_na = df['specialtwo'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'specialtwo']):
                    df.loc[i, 'specialtwo'] = specialtwo_non_na.sample(n=1,replace=True).values[0]
            #随机填充
            df['degreetype'].replace([None, ''], pd.NA,inplace = True)
            degreetype_non_na = df['degreetype'].dropna()  # 获取非空值
            for i in df.index:
                if pd.isna(df.loc[i, 'degreetype']):
                    df.loc[i, 'degreetype'] = degreetype_non_na.sample(n=1,replace=True).values[0]
            #将DataFrame 转换为列表
            data_list = df.to_dict(orient='records')
            db.session.query(hisyearscore).delete()
            for dl in data_list:
                filtered_data = {k: v for k, v in dl.items() if v not in [None, '', float('nan')] and (not isinstance(v, float) or not math.isnan(v))}
                db.session.add(hisyearscore(**filtered_data))
            db.session.commit()
            return jsonify(msg)
        except Exception as e:
            msg["code"] = other_code
            msg["message"] = e.__str__()
            return jsonify(msg)
