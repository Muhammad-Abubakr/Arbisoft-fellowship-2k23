from datetime import datetime
from scrapy.http import Response
from scrapy import Request, Spider

from ..items import DocketItem

class PucWeb1DocketsSpider(Spider):
    """scrapes data from (https://pucweb1.state.nv.us)
    
    Args:
        Spider (_type_): Base class for scrapy spiders. All spiders 
        must inherit from this class.
    """
    name = "pucweb1"

    def __init__(
            self, docket_id:str=None, start_date:str=None, 
            end_date:str=None, *args, **kwargs):
        """init method for PucWeb1Spider

        using to get the command line arguments for the Spider

        Args:
            docket_id (str, optional): 
                Specific Docket Id that we want to scrape. Defaults to None.
            start_date (str, optional): 
                Start date for dockets to collect. Defaults to None.
            end_date (str, optional): 
                End date for dockets to collect. Defaults to None.
        """
        if docket_id and start_date:
            raise ValueError(
            "you can pick one of two options (but not both)\n" 
            "a). docket_id or b). start_date and end_date")
        elif docket_id:
            self.docket_id = docket_id
        elif start_date or end_date:
            try:
                self.start_date = datetime.strptime(start_date, '%m/%d/%Y')
                self.end_date = datetime.strptime(end_date, '%m/%d/%Y')
            except TypeError:
                raise ValueError(
                "start_date and end_date must be provided alongside each other")


    def start_requests(self):
        """used by scrapy under the hood to schedule requests

        Yields:
            _type_: scrapy.Request
        """
        urls = [
            "https://pucweb1.state.nv.us/puc2/(X(1)S(c4icmmg52pdrbxtp2f31jubc))/Dktinfo.aspx?Util=All&AspxAutoDetectCookieSupport=1"
        ]
        for url in urls:
            yield Request(
                url=url, 
                callback=self.parse)
            
    def parse(self, response: Response):
        """parses the response received against the request made by 
        start_requests

        Args:
            response (Response): An object that represents an HTTP 
            response, which is usually downloaded (by the Downloader)
            and fed to the Spiders for processing.
        """
        dockets: list[str] = response.xpath(
            "//table[@id='GridView1']/tr/td/font/text()").getall()

        for col in range(0, len(dockets), 3):
            item = DocketItem()
            item["docket_no"] = dockets[col]
            item["date_filled"] = dockets[col+1]
            item["description"] = dockets[col+2]

            yield item