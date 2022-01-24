import requests 

# s1 为官网获取的APIKEY，s2为官网获取的Secret Key
client_id='client_id='+'s1'
client_secret='client_secret='+'s2'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'+client_id+'&'+client_secret
response = requests.get(host)
if response:
    print(response.json()['access_token'])