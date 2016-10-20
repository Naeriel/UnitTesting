""""
Provides tests for the main module.

@author: schlauch
"""


import subprocess
import sys

from html_parser import main


def test_parse_localfile_success(tmpdir, capfd):
    # Create file
    html_document = tmpdir.join("test.html")
    html_document.write("<html><body><a href='new_unknown_link.html'>Test</a></body></html>")

    # Run the command
    _run_main_script([str(html_document)])
    
    # Check result
    assert capfd.readouterr()[0].startswith("new_unknown_link.html")

    
def test_parse_remotfile_success(capfd):
    _run_main_script(["https://www.google.de"])
    assert capfd.readouterr()[0].startswith("https://www.google.de")


def _run_main_script(parameters):
    """ Helper to run the main routine of the HTML parser. """
    
    command = [sys.executable, main.__file__] + parameters # python main.py <parameters>
    subprocess.call(command)
