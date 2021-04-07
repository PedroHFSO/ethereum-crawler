import requests
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
#url = 'https://etherchain.org/blocks/data?draw=1&start=0&length=0'
url = 'https://www.etherchain.org/txs/data?draw=1&start=0&length=2'
response = json.loads(requests.get(url, headers = headers).text)
#response = json.loads(opener.open(url).read().decode())['data']
response = response['data']
print(response[0])
