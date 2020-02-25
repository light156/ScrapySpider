import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

<<<<<<< HEAD
#execute(["scrapy", "crawl", "Claim"])
#execute(["scrapy", "crawl", "Legacy"])
execute(["scrapy", "crawl", "Firm"])
=======
execute(["scrapy", "crawl", "Claim"])
#execute(["scrapy", "crawl", "Legacy"])
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
