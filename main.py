import requests
from bs4 import BeautifulSoup
import re
import json
import psycopg2

def cleanTransaction(info_div):
    name = info_div.find('div', {'class' : 'col-md-2'}).text
    name = name.replace(':', '')
    text = info_div.find('div', {'class' : 'col-md-10'}).text
    href = info_div.find('a', href = True)
    href_content = ''
    if href: #caso haja link (hash p/ to ou from) deixar apenas a hash
        href_content = href['href']
        href_content = re.sub('/.*/','', href_content)
    #últimos ajustes
    if name == 'Gas used':
        reg = re.search('of (.*) gas', text)
        text = reg.group(1).replace(',','.')
    elif name == 'Value':
        text = text.replace('ETH','').strip()
    elif name == 'Gas Price':
        text = text.replace('GWei','').strip()
    elif name == 'Time':
        reg = re.search('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*', text)
        text = reg.group(1)
    return text, name, href_content

def getTransaction(transaction_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    transaction = {}
    main_div = soup.find("div", {"class": "card-body px-0 py-1"}) #div principal que agrupa todas as informações necessárias
    try:
        for info in main_div.find_all('div', recursive = False): #itera por cada informação individualmente
            text, name, href_content = cleanTransaction(info)
            if name == 'To' or name == 'From':
                transaction[name] = href_content
            elif name != 'Block' and name != 'Status' and name != 'ERC20 Transfers' and name != 'Fee': #dados que não estão sendo armazenados na database
                transaction[name] = text
        return transaction
    except Exception as ex:
        print('Transação não encontrada:')
        print(ex)

def insertToDB(transaction):
    finalSQL = "INSERT INTO transactions3(joined_pool,user_from,user_to,hash,value,gas_offered,gas_price) VALUES"

    sqlToDo = finalSQL + " ('" + transaction['Time'] + "', '" + transation['From'] + "', '" + transaction['To'] + "','"
    transaction['Hash'] + "','" + transaction['Value'] + "','" + str(int(float(transaction['Gas used']))) + "','"
    transaction['Gas Price'] + "')"

    conn = psycopg2.connect(host="localhost", database="ethscan", user="postgres", password="")#"cp65482jf")
    cur = conn.cursor()
    cur.execute(sqlToDo)
    conn.commit()

url = 'https://etherchain.org/tx/0x82bf1d58c1e0e0a83db4a9fd53c117b26a7c5250c8badb13f397f3d5bed7b21d'
t = getTransaction(url)
insertToDB(t)
