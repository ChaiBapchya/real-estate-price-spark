# -*- coding: utf-8 -*-
import scrapy

class PropertyItem(scrapy.Item):
    platform = scrapy.Field()
    city = scrapy.Field()
    property_type = scrapy.Field()
    
    txn_type = scrapy.Field()
    locality = scrapy.Field()
    configtype = scrapy.Field()
    Building_Name = scrapy.Field()
    Selling_Price = scrapy.Field()   
    listing_date = scrapy.Field()
    sqft = scrapy.Field()
    listing_id=scrapy.Field()
    name_lister=scrapy.Field()
    contactno=scrapy.Field()
    Monthly_Rent=scrapy.Field()
    
   