import requests
import json
from datetime import datetime

def get_news():
    response = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=a8659717dffa4285a8036634688953a0')
    json_data = json.loads(response.text)
    articles = json_data['articles'][:5]
    list = []
    for article in articles: 
        title = article['title']
        url = article['url']
        
        list.append({'title': title, "url": url})
    return list

def get_stocks(t):
    month = str(datetime.today().replace(day=1).strftime('%Y-%m-%d'))
    url = 'https://api.polygon.io/v1/open-close/'+t+'/'+month+'?adjusted=true&apiKey=SX7dhy9JpYxpVvijGUWaeQj6Sn_qUH_q'
    response = requests.get(url)
    json_data = json.loads(response.text)
    list = []
    open = json_data['open']
    close = json_data['close']
    list.append(open)
    list.append(close)
    return list

def get_yomama():
    # url = 'https://api.yomomma.info/'
    url = 'https://yomama-stage.herokuapp.com/api/v1/get/random'
    response = requests.get(url)
    json_data = json.loads(response.text)
    # return json_data['joke']
    return json_data['text']

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)