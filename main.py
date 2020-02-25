import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

<<<<<<< HEAD
#execute(["scrapy", "crawl", "Claim"])
#execute(["scrapy", "crawl", "Legacy"])
execute(["scrapy", "crawl", "Firm"])
=======
<<<<<<< HEAD
#execute(["scrapy", "crawl", "Claim"])
#execute(["scrapy", "crawl", "Legacy"])
execute(["scrapy", "crawl", "Firm"])
=======
execute(["scrapy", "crawl", "Claim"])
#execute(["scrapy", "crawl", "Legacy"])
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
>>>>>>> 2b4d1433e506a14c377ce697c0cfa9c2ae9c9c2a
