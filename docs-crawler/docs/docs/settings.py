import os
# -*- coding: utf-8 -*-

# Scrapy settings for docs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'docs'

SPIDER_MODULES = ['docs.spiders']
NEWSPIDER_MODULE = 'docs.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
FEED_URI = f'file://{os.getcwd()}/output/%(name)s/%(version)s.json'
FEED_FORMAT = 'json'
FEED_EXPORTERS = {'json': 'scrapy.exporters.JsonItemExporter'}
