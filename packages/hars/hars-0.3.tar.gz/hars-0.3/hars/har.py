import json
from datetime import datetime

import requests


class Har:
    def __init__(self, har_file_path: str):
        with open(har_file_path, 'r', encoding='utf-8-sig') as file:
            self.har_data = json.load(file)
            self.log = self.har_data['log']
            self.version = self.log['version']
            self.pages = self.log['pages']
            self.creator = self.log['creator']
            self.entries = [Entry(entry) for entry in self.log['entries']]

    def replay(self, entry_index:int = 0):
        """
        重发指定索引的请求
        :param entry_index: 请求的索引，默认为0
        :return: 响应对象
        """
        entry = self.entries[entry_index]
        request = entry.request

        headers = {}
        for header in request['headers']:
            headers[header['name']] = header['value']

        cookies = {}
        for cookie in request['cookies']:
            cookies[cookie['name']] = cookie['value']

        params = {}
        for param in request['queryString']:
            params[param['name']] = param['value']

        data = request['postData']['text'] if 'postData' in request and 'text' in request['postData'] else None
        files = request['postData']['params'] if 'postData' in request and 'params' in request['postData'] else None
        if files:
            files = {file['name']: (file['fileName'], file['value']) for file in files}
        else:
            files = None
        if data:
            data = json.loads(data)
        else:
            data = None

        response = requests.request(
            request['method'],
            request['url'],
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            files=files
        )
        return response


class Entry:
    def __init__(self, entry_json):
        self._entry = entry_json
        for key, value in entry_json.items():
            setattr(self, key, value)


def load(har_file_path: str):
    return Har(har_file_path)

class RequestParser:
    def __init__(self, entry):
        self.response = None
        self.entry = entry
        self.request_info = self.entry["request"]
        self.url = self.request_info["url"]
        self.method = self.request_info["method"]
        self.headers = {header["name"]: header["value"] for header in self.request_info["headers"]}
        self.cookies = {cookie["name"]: cookie["value"] for cookie in self.request_info["cookies"]}
        self.data = {param["name"]: param["value"] for param in self.request_info["queryString"]}

    def set_url(self, url):
        self.url = url
        return self

    def set_method(self, method):
        self.method = method
        return self

    def set_headers(self, headers):
        self.headers = headers
        return self

    def set_cookies(self, cookies):
        self.cookies = cookies
        return self

    def set_data(self, data):
        self.data = data
        return self

    def request(self):
        self.response = requests.request(self.method, self.url, headers=self.headers, cookies=self.cookies,
                                         params=self.data)
        return self.response



class ResponseParser:
    def __init__(self, response:str|requests.Response):
        if isinstance(response, str):
            if response.endswith("har"):
                self.response = load(response).entries[0].response
        elif isinstance(response, requests.Response):
            self.response = response
        else:
            raise ValueError("response must be a str or requests.Response")

    def save(self, path):
        request = self.response.request
        har = {
            "log": {
                "version": "1.1",
                "creator": {
                    "name": "Python requests",
                    "version": requests.__version__
                },
                "pages": [],
                "entries": [
                    {
                        # 获取当前时间
                        "startedDateTime": datetime.now().isoformat() + "Z",
                        # 获取响应时间
                        "time": self.response.elapsed.total_seconds() * 1000,
                        "request": {
                            # 获取请求方法
                            "method": request.method,
                            # 获取请求URL
                            "url": request.url,
                            "httpVersion": "HTTP/1.1",
                            # 获取请求头
                            "headers": [{"name": k, "value": v} for k, v in request.headers.items()],
                            "cookies": [],
                            "headersSize": -1,
                            # 获取请求体大小
                            "bodySize": len(request.body) if request.body else 0,
                            # 获取请求体内容
                            "postData": {
                                "mimeType": request.headers.get("Content-Type", ""),
                                "text": request.body.decode() if request.body else ""
                            } if request.body else {}
                        },
                        "response": {
                            # 获取响应状态码
                            "status": self.response.status_code,
                            # 获取响应状态信息
                            "statusText": self.response.reason,
                            "httpVersion": "HTTP/1.1",
                            # 获取响应头
                            "headers": [{"name": k, "value": v} for k, v in self.response.headers.items()],
                            # 获取响应cookies
                            "cookies": [{"name": k, "value": v} for k, v in self.response.cookies.get_dict().items()],
                            "content": {
                                # 获取响应内容大小
                                "size": len(self.response.content),
                                # 获取响应内容类型
                                "mimeType": self.response.headers.get("Content-Type", ""),
                                # 获取响应内容
                                "text": self.response.text
                            },
                            # 获取重定向URL
                            "redirectURL": self.response.url if self.response.is_redirect else "",
                            "headersSize": -1,
                            # 获取响应体大小
                            "bodySize": len(self.response.content)
                        },
                        "cache": {},
                        "timings": {
                            # 获取阻塞时间
                            "blocked": -1,
                            # 获取DNS解析时间
                            "dns": -1,
                            # 获取连接时间
                            "connect": -1,
                            # 获取发送时间
                            "send": 0,
                            # 获取等待时间
                            "wait": self.response.elapsed.total_seconds() * 1000,
                            # 获取接收时间
                            "receive": 0,
                            # 获取SSL时间
                            "ssl": -1
                        }
                    }
                ]
            }
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(har, f, ensure_ascii=False, indent=2)

    def get_json(self):
        return json.loads(self.response.text)

    def get_text(self):
        return self.response.text

    def get_status_code(self):
        return self.response.status_code

    def get_headers(self):
        return self.response.headers

    def get_cookies(self):
        return self.response.cookies.get_dict()

    @staticmethod
    def select(data):
        pass

