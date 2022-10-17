import requests
from scrapy import Selector
import csv
import time
import fake_useragent


def Import_data(li_tag, num) :
    for item in li_tag :
        # 房名：
        name = "".join(item.xpath("./div[1]/p/a/text()").extract()).split()[0]
        # 面积：
        type = "".join(item.xpath("./div[1]/p[2]/text()").extract()).split()[-3]
        if "㎡" not in type :
            type = "".join(item.xpath("./div[1]/p[2]/text()").extract()).split()[-4]
        # 房型
        room = "".join(item.xpath("./div[1]/p[2]/text()").extract()).split()[-1]
        # 朝向
        toward = "".join(item.xpath("./div[1]/p[2]/text()").extract()).split()
        if toward[-3] in ["东", "南", "西", "北"] :
            toward = "".join("".join(item.xpath("./div[1]/p[2]/text()").extract()).split()[-3 :-1])
        else :
            toward = toward[-2]
        # 地址区
        nearby = "".join(item.xpath("./div[1]/p[2]/a[1]/text()").extract())
        # 具体地址
        nearby1 = "".join(item.xpath("./div[1]/p[2]/a[2]/text()").extract()).split()
        nearby2 = "".join(item.xpath("./div[1]/p[2]/a[3]/text()").extract()).split()
        nearb = "-".join(nearby1 + nearby2)
        # 照片地址
        pic_url = "".join(item.xpath(".//img/@data-src").extract())
        # 详细链接地址url
        url = "".join(item.xpath("./div[1]//a/@href").extract())
        url = "https://cs.lianjia.com" + url[0 :url.rfind('.html') + 5]
        # 租房的价格
        price = "".join(item.xpath("./div[1]/span/em/text()").extract()) + "".join(
            item.xpath("./div[1]/span/text()").extract())

        dit = {
            '房源名称' : name,
            '房型面积' : type,
            '户型' : room,
            '朝向' : toward,
            '地区' : nearby,
            "具体地址" : nearb,
            '照片地址' : pic_url,
            '链接地址' : url,
            "月租价格" : price,
        }
        time.sleep(2)
        f = open('租房数据.csv', mode='a', encoding='utf-8-sig', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=['房源名称', '房型面积', '户型', '朝向', '地区', "具体地址",
                                                   '照片地址', '链接地址', "月租价格"])
        if num == 1 :
            csv_writer.writeheader()
            num = 0
        csv_writer.writerow(dit)
    return num


if __name__ == '__main__' :
    # 随机User_Agent

    headers = fake_useragent.UserAgent()
    num = 1
    for i in range(1, 101) :
        url = "https://cs.lianjia.com/zufang/pg{}/#contentList".format(i)
        html = requests.get(url, headers.chrome,timeout=2).text
        sel = Selector(text=html)
        li_tag = sel.xpath("//div[@class='content__list--item']")
        print('在获取第{}页数据中......'.format(i))
        num = Import_data(li_tag, num)

    print('本次爬虫已结束！！！')
