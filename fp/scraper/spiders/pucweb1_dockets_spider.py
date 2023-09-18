from scrapy.http import Response
from scrapy import Request, Spider


class PucWeb1DocketsSpider(Spider):
    """scrapes data from (https://pucweb1.state.nv.us)
    
    Args:
        Spider (_type_): Base class for scrapy spiders. All spiders 
        must inherit from this class.
    """
    name = "pucweb1_dockets"

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
            item = dict()
            item["docket_no"] = dockets[col]
            item["date_filled"] = dockets[col+1]
            item["description"] = dockets[col+2]

            yield item