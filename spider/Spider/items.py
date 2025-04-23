# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class HisyearscoreItem(scrapy.Item):
    # 院校名称
    schoolname = scrapy.Field()
    # 年份
    nianfen = scrapy.Field()
    # 学位类别
    degreetype = scrapy.Field()
    # 专业名称
    specname = scrapy.Field()
    # 专业代码
    speccode = scrapy.Field()
    # 招生院系
    departname = scrapy.Field()
    # 总分
    totalscore = scrapy.Field()
    # 政治
    politics = scrapy.Field()
    # 外语
    english = scrapy.Field()
    # 专业课一
    specialone = scrapy.Field()
    # 专业课二
    specialtwo = scrapy.Field()
    # 研究方向
    specremark = scrapy.Field()

