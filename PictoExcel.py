from operator import imod
from django.http import request
import requests
import base64
import copy
from baidubce import bce_base_client
from baidubce.auth import bce_credentials
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import bce_client_configuration
import time
import urllib

# s1为官网获取的API Key， s2为官网获取的Secret Key
client_id='client_id='+'s1'
client_secret='client_secret='+'s2'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'+client_id+'&'+client_secret
response = requests.get(host)
if response:
    access_token=response.json()['access_token']

#access_token = '24.cdebea13a8c07668cc7ffba9d1032b48.2592000.1645594004.282335-25551721'
#表格文字识别(异步接口)

picture=input('请输入Pic文件夹下待处理的图片名(包含后缀)')
print('正在云端处理')

request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
f = open('Pic/'+picture, 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    request_id=response.json()['result'][0]['request_id']

time.sleep(5)   #等待云端表格文字识别完成,再获取结果
print('云端处理完成')

# 表格文字识别-异步接口-获取结果
class ApiCenterClient(bce_base_client.BceBaseClient):
    
    def __init__(self, config=None):
        self.service_id = 'apiexplorer'
        self.region_supported = True
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)
        
        if config is not None:
            self.config.merge_non_none_values(config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def demo(self):
        path = b'/rest/2.0/solution/v1/form_ocr/get_request_result'
        headers = {}
        headers[b'Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        params = {}
        params['access_token'] = access_token
        body = 'request_id='+request_id+'&result_type=excel'
        return self._send_request(http_methods.POST, path, body, headers, params)

if __name__ == '__main__':
    endpoint = 'https://aip.baidubce.com'
    ak = ''
    sk = ''
    config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(ak, sk),
                                                             endpoint=endpoint)
    client = ApiCenterClient(config)
    res = client.demo()
    print ("正在下载")
    url = (res.__dict__['raw_data'].split(':')[2]+':'+res.__dict__['raw_data'].split(':')[3].split(',')[0]).split('"')[1]
    f = urllib.request.urlopen(url)
    data = f.read()
    with open("Excel/"+picture.split('.')[0]+'.xls', "wb") as code:
        code.write(data)
    print('下载完成!')



