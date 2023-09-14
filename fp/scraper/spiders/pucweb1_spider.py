from datetime import datetime
from scrapy.http import Response
from scrapy import FormRequest, Request, Spider

from ..items import DocketItem, DocumentItem

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
        event_arguments: list[str] = response.xpath(
            "//a[contains(@href, 'javascript:__doPostBack')]/@href").getall()
        

        for col in range(0, len(dockets), 3):
            docket_date = datetime.strptime(dockets[col+1], '%m/%d/%Y')

            if hasattr(self, "docket_id"):
                if dockets[col] != self.docket_id:
                    continue
            elif hasattr(self, "start_date"):
                if docket_date > self.end_date:
                    continue
                elif docket_date < self.start_date:
                    break
            
            item = DocketItem()    
            item["docket_no"] = dockets[col]
            item["date_filled"] = dockets[col+1]
            item["description"] = dockets[col+2]

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
                meta={"docket": item},
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
        docket: DocketItem = response.meta.get("docket")
        dockets_details = response.xpath(
            "//table[@id='GridView2']/tr/td/font/text()").getall()
        documents: list[DocumentItem] = list()
        
        for col in range(0, len(dockets_details),4):
            item = DocumentItem()
            item["docket"] = docket.django_model.docket_no
            item["date_filed"] = dockets_details[col].strip()
            item["doc_type"] = dockets_details[col+1].strip()
            item["notes"] = dockets_details[col+2].strip()
            item["document_id"] = dockets_details[col+3].strip()

            documents.append(item)
        
        yield (docket, documents)