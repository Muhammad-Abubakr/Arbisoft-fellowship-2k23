from datetime import datetime
from scrapy.http import Response
from scrapy import FormRequest, Request, Spider

class PucWeb1Spider(Spider):
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
                self.log(
                    "start_date and end_date must be provide alongside each\
                     other")


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
                callback=self.parse_docket)
            
    def parse_docket(self, response: Response):
        """parses the response received against the request made by 
        start_requests

        Args:
            response (Response): An object that represents an HTTP 
            response, which is usually downloaded (by the Downloader)
            and fed to the Spiders for processing.
        """
        dockets: list[str] = response.xpath(
            "//table[@id='GridView1']/tr/td/font/text()").getall()
        event_arguments: list[str] = response.xpath(
            "//a[contains(@href, 'javascript:__doPostBack')]/@href").getall()
        

        for col in range(0, len(dockets), 3):
            docket_date = datetime.strptime(dockets[col+1], '%m/%d/%Y')

            if hasattr(self, "docket_id"):
                if dockets[col] != self.docket_id:
                    continue
            elif hasattr(self, "start_date"):
                if docket_date < self.start_date:
                    continue
                if docket_date > self.end_date:
                    break

            data = {
                "docket_number": dockets[col],
                "date_filed": dockets[col+1],
                "description": dockets[col+2],
                "documents": list(),
            }
            event_argument = (event_arguments[(col//3)+16]
                              .removeprefix("javascript:__doPostBack(")
                              .removesuffix(")")
                              .split(',')[1]
                              .strip("'"))
            form_data = {
                "__EVENTTARGET": "GridView1",
                "__EVENTARGUMENT": event_argument,
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

            if hasattr(self, "docket_id"):
                break

    def parse(self, response: Response):
        """receives the Response object against the FormRequest 
        submitted by parse_docket

        Args:
            response (Response): Response against FormRequest

        Yields:
            _type_: dict[str, any]
        """
        self.log("I am here")
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