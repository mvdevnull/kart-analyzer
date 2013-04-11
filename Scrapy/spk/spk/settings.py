# Scrapy settings for spk project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'spk'

SPIDER_MODULES = ['spk.spiders']
NEWSPIDER_MODULE = 'spk.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spk (+http://www.yourdomain.com)'
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 543,
#    'spk.middlewares.ProxyMiddleware': 100
#}