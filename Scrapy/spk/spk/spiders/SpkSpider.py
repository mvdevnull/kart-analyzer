#!/usr/bin/python

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from spk.items import SpkDriver

from urlparse import urlparse, urljoin
import re

class SpkSpider(BaseSpider):
	name = "SpkSpider"
	domain_name = "http://www.clubspeedtiming.com"
	start_urls = ["http://www.clubspeedtiming.com/spwvirginia/RacerHistory.aspx?CustID=1000001"]

	def parse(self, response):

		# Determine the next url to scrape by adding 1 to the current CustID
		custid_curr_dirty = re.split('=', urlparse(response.url).query)
		custid_curr = int(custid_curr_dirty[1])
		custid_next = custid_curr + 1
		url_next = "http://www.clubspeedtiming.com/spwvirginia/RacerHistory.aspx?CustID=" + str(custid_next)

		# Scrape pertinent data
		hxs =  HtmlXPathSelector(response)
		driver = SpkDriver()
		driver['name']		= hxs.select('//span[@id="lblRacerName"]/text()').extract()
		driver['custid']	= custid_curr

		# Return driver data and spawn an additional thread with a new request
		return driver, Request(url_next)