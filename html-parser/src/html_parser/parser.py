"""
Provides functionality to parse HML docuements.

@author: schlauch
"""


import bs4

from html_parser.fetcher import FetcherError


class HtmlParser:
    """ 
    Parses a HTML document and makes the result accesible to other client modules.
    Currently, only the extraction of URLs is supported.
    """
    
    def __init__(self, fetcher):
        """
        :param fetcher: Helps to retrieve the content that needs to be parsed.
        :type fetcher: `Fetcher<hml_parser.fetcher.Fetcher>`
        """

        self._fetcher = fetcher
        
    def extract_links(self):
        """ Extracts links from the HTMl document retrieved via the fetcher.
        
        :note: Here is the actual content retrieved as well. Thus, it might need some time.
        
        :return: A list of parsed links.
        """
        
        # Retrieve the content
        try:
            html_document = self._fetcher.retrieve()
        except FetcherError as error:
            raise HtmlParserError("Cannot retrieve content.") from error
        else:
            # Parses the content and handles decoding of bytes automatically
            parser = bs4.BeautifulSoup(html_document, "html.parser")
            
            # Determine all links
            retrieved_links = list()
            links = parser.find_all("a")
            for tag in links:
                link = tag.get("href", None)
                if not link is None:
                    retrieved_links.append(link)
            return retrieved_links


class HtmlParserError(Exception):
    pass
