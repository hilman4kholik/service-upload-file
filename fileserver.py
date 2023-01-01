#!/usr/bin/env python3
 
"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

see: https://gist.github.com/UniIsland/3346170
"""
 
 
__version__ = "1.0"
__all__ = ["FileServer"]
__author__ = "HilmanKholik"
__home_page__ = "hilman"
 
import os, sys
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import shutil
import mimetypes
import html
import re
from io import BytesIO
import configparser
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from threading import Thread
from urllib import request, error
from datetime import datetime

class Capture(Thread):
    def __init__(self, gate_name, url):
        Thread.__init__(self)
        self.file_name = f"{gate_name}{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        self.url = url

    def run(self):
        try:
            request.urlretrieve(self.url, self.file_name)
            print('capturing success!')
        except error.URLError as e: ResponseData = print(e)
        except NameError:
            print('Gagal mengambil gambar!')

class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
 
    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """
    server_version = "HTTPServer/" + __version__
 
    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
 
    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()
 
    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()

        f = BytesIO()
        f.write(bytes(info, "utf-8"))

        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def deal_post_data(self):
        key = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
        
        """for authorization"""
        # if self.headers.get('Authorizetion') != key:
        #     return (False, "{\"response_status\": \"401\",\"response_message\": \"Unauthorized\", \"data\": {\"msg\": \"Access denied!\"}}")

        if "capture" in self.path:
            """
                #For payload


                {
                    "gate":"M01",
                    "url":"http://192.168.1.88/tmpfs/snap.jpg?usr=admin&pwd=admin"
                }
            """

            length = int(self.headers['content-length'])
            payload = json.loads(self.rfile.read(length))
            getCapture = Capture(payload["gate"], payload["url"])
            getCapture.start()
            # getCapture.join()
            return (False, "{\"response_status\": \"200\",\"response_message\": \"Oke\", \"data\": {\"msg\": \"\"}}")

        content_type = self.headers['content-type']
        if not content_type:
            return (False, "{\"response_status\": \"403\",\"response_message\": \"Error\", \"data\": {\"msg\": \"Content-Type header doesn't contain boundary\"}}")
        
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "{\"response_status\": \"403\",\"response_message\": \"Error\", \"data\": {\"msg\": \"Content NOT begin with boundary\"}}")

        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "{\"response_status\": \"403\",\"response_message\": \"Error\", \"data\": {\"msg\": \"Can't find out file name...\"}}")

        path = self.translate_path(self.path)
        fName = fn[0]
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "{\"response_status\": \"403\",\"response_message\": \"Error\", \"data\": {\"msg\": \"Can't create file to write\"}}")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "{\"response_status\": \"00\",\"response_message\": \"Success\", \"data\": {\"msg\": \"%s\"}}" % fName)
            else:
                out.write(preline)
                preline = line
        return (False, "{\"response_status\": \"403\",\"response_message\": \"Error\", \"data\": {\"msg\": \"Unexpect Ends of data\"}}")
        
 
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = html.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(linkname), html.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
 
    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)
 
    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
 
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
 
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

def startWebServer(HandlerClass = SimpleHTTPRequestHandler):
    curDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    iniFile = configparser.ConfigParser()
    iniFile.read(curDir+"/FileServer.ini")
    imgRootDir = iniFile.get("Server", "ImageRootDir")
    print("FileServer serving on: {}/{}".format(curDir, imgRootDir))
    try:
        os.chdir("{}/{}".format(curDir, imgRootDir))
    except:
        os.mkdir("{}/{}".format(curDir, imgRootDir))
        try:
            os.chdir("{}/{}".format(curDir, imgRootDir))
        except:
            print('Tidak bisa membuat Folder {}'.format(imgRootDir))
    ThreadingServer(('', 8188), HandlerClass).serve_forever()

if __name__ == '__main__':
    
    try:
        startWebServer()
        while True:
            pass
    except KeyboardInterrupt:
        print("Program dipaksa berhenti")
        sys.exit()