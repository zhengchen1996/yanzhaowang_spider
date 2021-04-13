from scrapy import Request
from scrapy.spiders import Spider
from yanzhaowang.items import YanzhaowangItem   #数据结构

class XiongmaoSpider(Spider):
    name = "date"

    def __init__(self):
        self.currentPage = 0

    def start_requests(self):#初始请求
        url = "https://yz.chsi.com.cn/sch/"
        yield Request(url)

    def parse(self, response):#解析函数
        list_selector = response.xpath("//tbody/tr")
        maxPage = \
            response.xpath("//div[@class='pager-box clearfix']/form/ul/li[last()-2]/a/text()").extract()[0]

        for one_selector in list_selector:
            try:
                schoolName = one_selector.xpath("td[1]/a/text()").extract()[0]
                location = one_selector.xpath("td[2]/text()").extract()[0]
                belong = one_selector.xpath("td[3]/text()").extract()[0]
                graduateSchool = one_selector.xpath("td[4]").extract()
                if "i class" in str(graduateSchool):
                    graduateSchool = "是"
                else:
                    graduateSchool = "否"
                optional = one_selector.xpath("td[5]").extract()
                if "i class" in str(optional):
                    optional = "是"
                else:
                    optional = "否"
                url = "https://yz.chsi.com.cn" +\
                      one_selector.xpath("td[1]/a/@href").extract()[0]

                item = YanzhaowangItem()
                item["schoolName"] = schoolName  # 学校名
                item["location"] = location  # 所在地
                item["belong"] = belong  # 隶属
                item["graduateSchool"] = graduateSchool# 研究生院
                item["optional"] = optional  # 自划线
                item["url"] = url  # url

                #生成中间页请求，meta为字典，nextPage为中间页解析函数
                yield Request(url,
                              meta={"item": item},
                              callback=self.nextPage)

            except:
                pass

            #获取下一页
            self.currentPage += 20
            if self.currentPage < int(maxPage)*20:
            # if self.currentPage < 3:
                nextUrl = "https://yz.chsi.com.cn/sch/?start=%d" % self.currentPage
                yield Request(nextUrl)

    def nextPage (self, response):#中间页解析函数
        tempUrl = "https://yz.chsi.com.cn" +\
                  response.xpath("//div[@class='yxk-index-con']/div[2]/ul/li[last()-2]/a/@href").extract()[0]
        item = response.meta["item"]
        url = tempUrl
        yield Request(url,
                      meta={"item": item},
                      callback=self.typePase)

    def typePase(self, response):#详细页解析函数
        item = response.meta["item"]
        list_selector = \
            response.xpath("//div[@class='main-wrapper']/div[3]/div[2]//div[@class='tab-item js-tab']")
        num = 1
        for j in range(len(list_selector)):
            classListSelector = \
                response.xpath("//div[@class='main-wrapper']/div[3]/div[2]/div[2]/div[" +
                               str(num) + "]/ul")
            for classSelector in classListSelector:
                for i in range(len(classSelector.xpath("li"))):
                    item["type"] = \
                        response.xpath("//div[@class='main-wrapper']/div[3]/div[2]/div[1]/div[" +
                                       str(num) + "]/a/text()").extract()[0]  # 专业分类
                    item["subject"] = classSelector.xpath("li["+str(i+1)+"]/text()").extract()[0]

                    yield item

            num += 1


