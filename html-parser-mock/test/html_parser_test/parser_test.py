"""
Provides some basic tests of the HTML parser.

@author: schlauch
"""


from unittest import mock

import pytest 

from html_parser.fetcher import Fetcher, FetcherError
from html_parser.parser import HtmlParser, HtmlParserError


class TestHtmlParser():
    
    def setup_method(self, _):
        self._fetcher_mock = mock.Mock(spec=Fetcher)
        self._parser = HtmlParser(self._fetcher_mock)

    def test_extract_links_success(self):
        # Configure the mock
        self._fetcher_mock.retrieve.return_value = "<a href='/index.html'>index.html</a>"

        # Call the method to test
        extracted_links = self._parser.extract_links()
        
        # Check the assertions
        assert len(extracted_links) == 1
        assert extracted_links[0] == "/index.html"
    
    def test_invalid_document(self):
        # Configure the mock
        self._fetcher_mock.retrieve.return_value = ""

        # Call the method to test
        extracted_links = self._parser.extract_links()
        
        # Check the assertions
        assert len(extracted_links) == 0     
    
    def test_no_link(self):
        # Configure the mock
        self._fetcher_mock.retrieve.return_value = "<a>index.html</a>"

        # Call the method to test
        extracted_links = self._parser.extract_links()
        
        # Check the assertions
        assert len(extracted_links) == 0
        
    def test_errors(self):
        # Configure the mock
        self._fetcher_mock.retrieve.side_effect = FetcherError

        # Call the method to test
        with pytest.raises(HtmlParserError):
            self._parser.extract_links()