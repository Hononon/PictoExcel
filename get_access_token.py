import requests 

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id='client_id='+'72FXWDzlWTNsGdNOkkg88bGN'
client_secret='client_secret='+'LlqVGHhG4qeHYEkWYQOesipS4H4vdo1o'
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'+client_id+'&'+client_secret
response = requests.get(host)
if response:
    print(response.json()['access_token'])