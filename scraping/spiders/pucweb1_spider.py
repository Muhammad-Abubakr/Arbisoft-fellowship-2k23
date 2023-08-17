from scrapy.http import Response
from scrapy import FormRequest, Request, Spider

class PucWeb1Spider(Spider):
    """scrapes data from (https://pucweb1.state.nv.us)
    
    Args:
        Spider (_type_): Base class for scrapy spiders. All spiders 
        must inherit from this class.
    """
    name = "pucweb1"
    
    def start_requests(self):
        """used by scrapy under the hood to schedule requests

        Yields:
            _type_: scrapy.Request
        """
        urls = [
            "https://pucweb1.state.nv.us/puc2/(X(1)S(c4icmmg52pdrbxtp2f31jubc))/Dktinfo.aspx?Util=All&AspxAutoDetectCookieSupport=1"
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse_docket)
            
    def parse_docket(self, response: Response):
        """parses the response received against the request made by 
        start_requests

        Args:
            response (Response): An object that represents an HTTP 
            response, which is usually downloaded (by the Downloader)
            and fed to the Spiders for processing.
        """
        dockets = response.xpath(
            "//table[@id='GridView1']/tr/td/font/text()").getall()
        
        for col in range(0, len(dockets), 3):
            data = {
                "docket_number": dockets[col],
                "date_filed": dockets[col+1],
                "description": dockets[col+2],
                "documents": list(),
            }
            form_data = {
                "__EVENTTARGET": "GridView1",
                "__EVENTARGUMENT": f"Select${col//3}",
            }
            yield FormRequest.from_response(
                response=response,
                method='POST',
                formid="form1",
                formdata=form_data,
                dont_filter=True,
                callback=self.parse,
                dont_click=True,
                meta={"docket": data},
            )

    def parse(self, response: Response):
        """receives the Response object against the FormRequest 
        submitted by parse_docket

        Args:
            response (Response): Response against FormRequest

        Yields:
            _type_: dict[str, any]
        """
        docket = response.meta.get("docket")
        dockets_details = response.xpath(
            "//table[@id='GridView2']/tr/td/font/text()").getall()
        
        for col in range(0, len(dockets_details),4):
            detail = {
                "date_filled": dockets_details[col].strip(),
                "doc_type": dockets_details[col+1].strip(),
                "notes": dockets_details[col+2].strip(),
                "docID": dockets_details[col+3].strip(),
            }
            docket.get("documents").append(detail)
        
        yield docket