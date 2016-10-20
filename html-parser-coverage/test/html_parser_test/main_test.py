""""
Provides tests for the main module.

@author: schlauch
"""


from http import server
import os
import socketserver
import subprocess
import sys
import threading

import pytest

from html_parser import main


def test_parse_localfile_success(tmpdir, capfd):
    # Create file
    html_document = tmpdir.join("test.html")
    html_document.write("<html><body><a href='new_link.html'>Test</a></body></html>")

    # Run the command
    _run_main_script([str(html_document)])
    
    # Check result
    assert capfd.readouterr()[0].startswith("new_link.html")


def test_parse_remotefile_success(httpserver, tmpdir, capfd):
    # Retrieve HTTP server details
    root_url, server_base_dir = httpserver # We use a fake object instead
    
    # Create valid HTML document
    html_document = server_base_dir.join("test.html")
    content = "<html><body><a href='new_link.html'>Test</a></body></html>"
    html_document.write(content.encode("utf-8"), mode="wb")
    
    # Run the command
    _run_main_script([root_url + "test.html"])

    # Make sure it is successfully run
    assert capfd.readouterr()[0].startswith("new_link.html")


def _run_main_script(parameters):
    """ Helper to run the main routine of the HTML parser. """
    
    command = [sys.executable, main.__file__] + parameters # python main.py <parameters>
    subprocess.call(command)


@pytest.fixture(scope="module")
def httpserver(request, tmpdir_factory):
    """
    Provides a `SimpleHTTPRequestHandler` instance which serves its files
    in `server_base_dir`. The server can handle multiple requests during the test
    function lifetime. As soon as the test functions exits, the server is
    shut down.
    
    :return: Tuple of the root URL to access the server and tmpdir object to
             manipulate files which the server allows access to.
    :rtype: Tuple of str, py.path.local 
    """

    # Set up HTTP server => next free port is selected automatically
    httpserver = socketserver.TCPServer(("", 0), server.SimpleHTTPRequestHandler)
    root_url = "http://localhost:{0}/".format(httpserver.server_address[1])
    server_base_dir = tmpdir_factory.mktemp("server_base")
    
    # Start HTTP server
    current_work_dir = os.curdir
    os.chdir(str(server_base_dir))
    try:
        thread = threading.Thread(target=httpserver.serve_forever)
        thread.start()
    finally: # Make sure we reset the current working to not confuse other processes
        os.chdir(current_work_dir)

    # Automatically disposes HTTP server after tests are finished
    def _finalize_server():
        httpserver.shutdown()
        thread.join()
    request.addfinalizer(_finalize_server)
    
    return root_url, server_base_dir
