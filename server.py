import re
from http.server import BaseHTTPRequestHandler
import subprocess
import os
import json

import constant


class MyServer(BaseHTTPRequestHandler):
    webServer = None
    root = constant.WWW_DIR

    def do_GET(self):
        try:
            status = 200
            dataType = "text/html"
            print("Requested URL: " + self.path)
            self.Execute_htaccess_like()
            file = self.path
            params = self.get_all_params_from_url(self.path)
            if file.find("?") > -1:
                file = file.split('?')[0]
            if file == "/" or file == "":
                file = "/index.py"
                if not self.file_exists(file):
                    file = "/index.html"
                elif not self.file_exists(file):
                    file = "/index.htm"
            fileExtension = self.file_extension(file)
            if fileExtension == "py":
                passedData = {
                    "METHOD": "GET",
                    "DATA": params,
                    "PATH": self.path,
                    "HOST": self.headers.get('Host'),
                    "DIRECTORY": self.root
                }
                data = self.run_and_capture_output(self.root + file, passedData)
                # posSemiColon = data.find(';')
                # info = data[:posSemiColon]
                # data = data[posSemiColon:]
                # info = info.split(',')
                # status = info[0]
                # dataType = info[1]
                data = data.encode()
            else:
                if fileExtension == "html" or fileExtension == "htm":
                    dataType = "text/html"
                elif fileExtension == "css":
                    dataType = "text/css"
                elif fileExtension == "js":
                    dataType = "application/javascript"
                elif fileExtension == "json":
                    dataType = "application/json"
                elif fileExtension == "xml":
                    dataType = "application/xml"
                elif fileExtension == "gif":
                    dataType = "image/gif"
                elif fileExtension == "png":
                    dataType = "image/png"
                elif fileExtension == "svg":
                    dataType = "image/svg+xml"
                elif fileExtension == "jpg" or fileExtension == "jpeg":
                    dataType = "image/jpge"
                elif fileExtension == "svg":
                    dataType = "image/png"
                elif fileExtension == "mp3":
                    dataType = "audio/mp3"
                elif fileExtension == "wav":
                    dataType = "audio/wav"
                elif fileExtension == "mp4":
                    dataType = "video/mp4"
                elif fileExtension == "avi":
                    dataType = "video/x-msvideo"
                elif fileExtension == "pdf":
                    dataType = "application/pdf"
                elif fileExtension == "doc" or fileExtension == "docx":
                    dataType = "application/msword"
                elif fileExtension == "xls" or fileExtension == "xlsx":
                    dataType = "application/vnd.ms-excel"
                elif fileExtension == "ppt" or fileExtension == "pptx":
                    dataType = "application/vnd.ms-powerpoint"
                requestedFile = self.root + file
                with open(requestedFile, 'rb') as f:
                    data = f.read()

            self.send_response(int(status))
            self.send_header('Content-type', dataType)
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            page = self.loadCustomErrorFile(404)
            if not page:
                page = '<h1>Error 404: URL NOT FOUND</h1>'
            self.wfile.write(page.encode("utf-8"))
        except PermissionError:
            self.send_response(403)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            page = self.loadCustomErrorFile(403)
            if not page:
                page = '<h1>Error 403: URL NOT PERMITTED</h1>'
            self.wfile.write(page.encode("utf-8"))
        except Exception as e:
            print(e)
            self.send_response(500)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            page = self.loadCustomErrorFile(500)
            if not page:
                page = '<h1>Error 500: INTERNAL SERVER ERROR</h1>'
            self.wfile.write(page.encode("utf-8"))

    def do_POST(self):

        status = 200
        dataType = "text/html"
        print("Requested URL: " + self.path)
        self.Execute_htaccess_like()
        url = self.root + self.path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        passedData = {
            "PATH": self.path,
            "HOST": self.headers.get('Host'),
            "METHOD": "POST",
            "DATA": data,
            "DIRECTORY": self.root
        }
        data = self.run_and_capture_output(url, passedData)
        posSemiColon = data.find(';')
        if posSemiColon > -1:
            info = data[:posSemiColon]
            data = data[posSemiColon:]
            info = info.split(',')
            status = info[0]
            dataType = info[1]
            data = data.encode()
        else:
            status = 500
            data = data.encode("utf-8")
        self.send_response(int(status))
        self.send_header('Content-type', dataType)
        self.end_headers()
        self.wfile.write(data)

    def run_and_capture_output(self, file_path, input_object):
        try:
            # Serialize the input object to JSON
            input_json = json.dumps(input_object)
            open(file_path)
            # process = subprocess.Popen(['python', file_path], stdout=subprocess.PIPE)
            process = subprocess.run(['python3', file_path], input=input_json.encode('utf-8'), check=True,
                                     stdout=subprocess.PIPE)
            # output, _ = process.communicate(input=input_json.encode('utf-8'))
            sortie = process.stdout.decode('utf-8')
            return sortie
        except Exception as e:
            return str(f"An error occurred while running the script:\n{e}")

    def get_param_from_url(self, url, param_name):
        if url.find("?") > -1:
            return [i.split("=")[-1] for i in url.split("?", 1)[-1].split("&") if i.startswith(param_name + "=")][0]
        return ""

    def get_all_params_from_url(self, url):
        if url.find("?") > -1:
            return url.split("?")[1]
        return ""

    def get_json_post_params(self):
        from urllib import request
        return request.get_json()

    def ApplyRedirectionsIfExists(self, regex, destination):
        matches = re.search(regex, self.path)
        if self.path.find("?") > -1:
            self.path = destination + self.path[matches.end() - 1:]
        else:
            self.path = destination

    def Execute_htaccess_like(self):
        try:
            with open("config.xml", 'r') as f:
                output = f.read()
        except Exception:
            print("There is no config file on this server for Execute_htaccess_like")
            return None
        # Parse XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(output)

        if root.tag != 'config':
            print('Error: main root must be <config>')
            return None

        req_host = self.headers.get('Host')
        for Host in root.iter('host'):
            if Host.get('value') == req_host:
                for Directory in Host.iter('directory'):
                    if Directory.get('path'):
                        self.root = Directory.get('path')
                for Rule in Host.iter('rule'):
                    if Rule.get('action') == "replace":
                        replace = True
                        if Rule.get('skip') == "existing":
                            replace = False
                            pos = self.path.find("?")
                            if pos > -1:
                                file_to_check = self.root + self.path[:pos]
                            else:
                                file_to_check = self.root + self.path
                            if not self.file_exists(file_to_check):
                                replace = True
                        if replace:
                            value = Rule.find('regex').text
                            replace = Rule.find('value').text
                            self.ApplyRedirectionsIfExists(value, replace)

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    @staticmethod
    def file_extension(file_path):
        return str(os.path.splitext(file_path)[1])[1:]

    def loadCustomErrorFile(self, errCode):
        try:
            with open("config.xml", 'r') as f:
                output = f.read()
        except Exception:
            print("There is no config file on this server for loadCustomErrorFile")
            return None

        import xml.etree.ElementTree as ET
        root = ET.fromstring(output)

        if root.tag != 'config':
            print('Error: main root must be <config>')
            return None

        req_host = self.headers.get('Host')
        for Host in root.iter('host'):
            if Host.get('value') == req_host:
                for Error in Host.iter('error'):
                    page = Error.find('page')
                    if page.get("code") == str(errCode):
                        try:
                            with open(self.root + "/" + page.text, 'r') as f:
                                return f.read()
                        except Exception:
                            print("There is no custom file for this type of error")
                            return None
