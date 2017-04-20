from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from OLX.items import PropertyItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from datetime import datetime,time,timedelta,date

class MySpider(CrawlSpider):
    name = "OlxSpider"
    allowed_domains = ['www.olx.in']
    start_urls = ["https://www.olx.in/mumbai/houses/?search%5Bphotos%5D=false",
    "https://www.olx.in/mumbai/apartments/?search%5Bphotos%5D=false",
    "https://www.olx.in/mumbai/commercial-space/?search%5Bphotos%5D=false",
    "https://www.olx.in/mumbai/land-plots/?search%5Bphotos%5D=false",
    "https://www.olx.in/mumbai/guest-houses/",

   ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('www.olx.in'), restrict_xpaths=('//*[@id="offers_table"]/tbody/tr/td/table/tbody/tr[1]/td[1]/div/span/a[@href]',)), callback="parsef", follow= True),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//section[@id="body-container"]/div[1]/div/div[@class="pager rel clr"]/span[@class="fbold next abs large"]/a[@href]',)), follow= True),
    )
 
    def parsef(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//span[@class="rel inlblk"]')
        loc = hxs.xpath('//strong[@class="c2b small"]')
        dates = hxs.xpath('//span[@class="pdingleft10 brlefte5"]')
        price= hxs.xpath('//strong[@class="xxxx-large margintop7 inlblk not-arranged"]')
        postedby= hxs.xpath('//span[@class="block color-5 brkword xx-large"]')
        contact= hxs.xpath('//strong[@class="large lheight20 fnormal  "]')
        tran= hxs.xpath('//td[@class="middle"]')
        ptitle= hxs.xpath('//h1[@class="brkword lheight28"]')
        detail= hxs.xpath('//table[@class="details fixed marginbott20 margintop5"]')
        
        items = []
        for titles in titles:
            item = PropertyItem()
            item["listing_id"] = map(unicode.strip, titles.xpath("text()").extract())
            item['platform']="OLX"  
            item['city']="Mumbai"     
        for loc in loc:
            item["locality"] = map(unicode.strip, loc.xpath("text()").extract())            
        for dates in dates:
            ldate = str(map(unicode.strip, dates.xpath("text()").extract()))
            print ldate
            if "at" in ldate:
                item['listing_date']=date.today()
            elif "terday" in ldate:
                item['listing_date']=date.today() - timedelta(days=1)
            elif "on" in ldate:
                a=ldate.find('on')
                ldate=ldate[a+3:a+10]
                ldate=ldate.replace("'","")
                item['listing_date']=ldate
        
        for postedby in postedby:
            item["name_lister"] = map(unicode.strip, postedby.xpath("text()").extract())
        for contact in contact:
            item["contactno"] = map(unicode.strip, contact.xpath("text()").extract())
        for tran in tran: 
            if "mmercial" in str(map(unicode.strip, tran.xpath("//ul/li[3]/a/span[1]/text()").extract())) :
                item["property_type"] = "Commercial"
            elif "Plots" in str(map(unicode.strip, tran.xpath("//ul/li[3]/a/span[1]/text()").extract())):
                item["property_type"] = "Plots/Land"
            else:
                item["property_type"] = "Residential"
            fl=0
            
            if "ale" in str(map(unicode.strip, tran.xpath("//ul/li[4]/a/span[1]/text()").extract())) :
                item["txn_type"] = "Sale"
                fl=1
            elif "uest" in str(map(unicode.strip, tran.xpath("//ul/li[4]/a/span[1]/text()").extract())):
                item["txn_type"] = "Vacation/Guest"
            else:
                item["txn_type"] = "Rent"
        for price in price:
            if fl==1:
                item["Selling_Price"] = map(unicode.strip, price.xpath("text()").extract())
            elif fl==0:
                item["Monthly_Rent"] = map(unicode.strip, price.xpath("text()").extract())
                  
        for ptitle in ptitle:
            myString= str(map(unicode.strip, ptitle.xpath("text()").extract()))
            myString = myString.upper()
            no= myString.find('BHK')
            x=0
            if no==-1:
                no1=myString.find('RK ')
                s1=no1-2
                no1=no1+2
                hk1=myString[s1:no1]
                item['configtype']= hk1
                x=1
            if no!=-1:     
                s=no-2
                no=no+3
                hk=myString[s:no]
                item['configtype']= hk 
        for detail in detail:
            if "quare" in str(map(unicode.strip, detail.xpath("tr[1]/td[1]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[1]/div[1]/strong/text()").extract()))
            elif "quare" in str(map(unicode.strip, detail.xpath("tr[1]/td[2]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[2]/div[1]/strong/text()").extract()))
            elif "quare" in str(map(unicode.strip, detail.xpath("tr[1]/td[3]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[3]/div[1]/strong/text()").extract()))
            elif "quare" in str(map(unicode.strip, detail.xpath("tr[3]/td[1]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[1]/div[1]/strong/text()").extract()))
            elif "quare" in str(map(unicode.strip, detail.xpath("tr[3]/td[2]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[2]/div[1]/strong/text()").extract()))
            elif "quare" in str(map(unicode.strip, detail.xpath("tr[3]/td[3]/div[1]/text()").extract())):
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[3]/div[1]/strong/text()").extract()))
            num=st.find("ft")         
            st=st[1:num]
            st=st.replace("u","")
            st=st.replace("'","")
            item['sqft']=st
            f=0
            
            if "oom" in str(map(unicode.strip, detail.xpath("tr[1]/td[1]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[1]/div[1]/strong/text()").extract()))
                f=1
            elif "oom" in str(map(unicode.strip, detail.xpath("tr[1]/td[2]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[2]/div[1]/strong/a/text()").extract()))
                f=1
            elif "oom" in str(map(unicode.strip, detail.xpath("tr[1]/td[3]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[1]/td[3]/div[1]/strong/a/text()").extract()))
                f=1
            elif "oom" in str(map(unicode.strip, detail.xpath("tr[3]/td[1]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[1]/div[1]/strong/a/text()").extract()))
                f=1
            elif "oom" in str(map(unicode.strip, detail.xpath("tr[3]/td[2]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[2]/div[1]/strong/a/text()").extract()))
                f=1
            elif "oom" in str(map(unicode.strip, detail.xpath("tr[3]/td[3]/div[1]/text()").extract())) and no==-1:
                st=str(map(unicode.strip, detail.xpath("tr[3]/td[3]/div[1]/strong/a/text()").extract()))
                f=1
            if f==1 and "1" in st:
                item['configtype']="1BHK"
            elif f==1 and "2" in st:
                item['configtype']="2BHK"
            elif f==1 and "3" in st:
                item['configtype']="3BHK"
            
        items.append(item)
        return(items)