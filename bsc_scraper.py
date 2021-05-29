import apikey
import requests
import re
from bs4 import BeautifulSoup

################
### scraping new tokens ### 
source_new = requests.get(f'https://coinmarketcap.com/new/').text
soup_4 = BeautifulSoup(source_new, 'lxml')
card_5 = soup_4.find('tbody')
print('--- New Release Tokens ---')
for td in card_5.find_all('tr')[:3]:
    new_num = td.select_one('td:nth-child(2)', style='text').text
    new_name = td.select_one('td:nth-child(3)', style='text').a.div.div.p.text
    new_symbol = td.select_one('td:nth-child(3)', style='text').a.div.div.div.p.text
    new_img = td.select_one('td:nth-child(3)', style='text').a.div.img['src']
    new_price = td.select_one('td:nth-child(4)', style='text').text
    new_change1hr = td.select_one('td:nth-child(5)', style='text').span.text
    new_change24hr = td.select_one('td:nth-child(6)', style='text').span.text
    new_volume = td.select_one('td:nth-child(8)', style='text').text
    new_chain = td.select_one('td:nth-child(9)', style='text').div.text
    new_release = td.select_one('td:nth-child(10)', style='text').text
    new_hash_url = td.select_one('td:nth-child(3)', style='text').a['href']
    print(f'Released: {new_release}')
    print(f'--- *{new_name}* : {new_symbol} ---')
    print(f'Token Image URL: {new_img}')
    print(f'Price: {new_price}')
    print(f'% Change 1hr: % {new_change1hr}')
    print(f'% Change 24hr: % {new_change24hr}')
    print(f'Volume: {new_volume}')
    print(f'Blockchain: {new_chain}')
    print(f'Hash url: https://coinmarketcap.com{new_hash_url}')
    print('------')
################
### take user input ###
user_input = input ("Enter the token name:")
# user_input = ['']

### function to scrape sites for coin ###
def bsc_coin_scrape(user_input):
    ### CMC urls ###
    url_query = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    url_latest = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url_meta = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    url_idmap = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    url_fiat = 'https://pro-api.coinmarketcap.com/v1/fiat/map' 
    ### CMC api key ###
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY' : apikey.apikey,
    }
    ### parameters ###
    params = {
    'symbol' : user_input,
    }
####################
    query_data = requests.get(url_query, params=params , headers=headers).json()
    coins_query = query_data['data']
    meta_data = requests.get(url_meta, params=params , headers=headers).json()
    params = {
    'slug' : user_input,
    }
    coins_meta = meta_data['data']
    for key, value in coins_query.items():
        name = value['name']
        symbol = value['symbol']
        total_supply = value['total_supply']
        price = value['quote']['USD']['price']
        volume_24h = value['quote']['USD']['volume_24h']
        change_1h = value['quote']['USD']['percent_change_1h']
        change_24h = value['quote']['USD']['percent_change_24h']
        change_7d = value['quote']['USD']['percent_change_7d']
        change_30d = value['quote']['USD']['percent_change_30d']
        change_60d = value['quote']['USD']['percent_change_60d']
        change_90d = value['quote']['USD']['percent_change_90d']
####################
        for key, value2 in coins_meta.items():
            if value['name'] == value2['name']:
                logo = value2['logo']
                for x in value2['urls']['explorer']:
                    if x.count('bscscan') == 1:
                        bsc_url = x
                    elif x.count('blockchair') == 1:
                        blockchair_url = x
                    elif x.count('etherscan') == 1:
                        etherscan_url = x
                    elif x.count('ethplorer') == 1:
                          ethplorer_url = x
############################################################################################################
            if bsc_url != None:
                hash_num = bsc_url[26:]
                source_info = requests.get(f'https://bscscan.com/token/{hash_num}').text
            source_holders = requests.get(f'https://bscscan.com/token/tokenholderchart/{hash_num}').text
            source_description = requests.get(f'https://bscscan.com/token/{hash_num}#tokenInfo').text
            soup_1 = BeautifulSoup(source_info, 'lxml')
            soup_2 = BeautifulSoup(source_holders, 'lxml')
            soup_3 = BeautifulSoup(source_description, 'lxml')
            overview = soup_1.find('div', class_='row mb-4')
####################
            card_4 = soup_3.find('div', id='ContentPlaceHolder1_maintab')
            token = overview.find('div', class_='font-weight-medium').b.text
            description = card_4.find('div', id='tokenInfo').div.text
            description = description.split('MarketVolume', 1)
            description = description[0]
            supply = overview.find('span', class_='hash-tag text-truncate').text
            c_supply = overview.find('span', class_='text-secondary ml-1').text
            holders = overview.find('div', class_='mr-3').text
####################
            for card in soup_1.find_all('div', class_='col-md-6'):
                if card.find('h2', class_='card-header-title') != None and card.find('div', class_='col-md-4').text == 'Contract:':
                        contract = card.find('a', class_='text-truncate d-block mr-2').text
                        url = card.find('div', id='ContentPlaceHolder1_tr_officialsite_1')
                        url = url.find('div', class_='col-md-8').a['href']
####################
            card_2 = soup_2.find('div', id='ContentPlaceHolder1_resultrows')
            ta = soup_2.find('div', class_='mb-0').p.text[1:-1]
            ta = ta.replace('token', 'tokens')
            ta = ta.replace('tokenss', 'tokens')
            card_3 = soup_2.find('div', class_='card-header py-4')
            header2 = card_3.find('div', class_='col-md-6').text
            name = blockchair_url.split('.com/', 1)
            token_name = name[1].upper()
###################            
## prints ### 
            print('*****')
            print(f"--- *{token}* {token_name} : Price Info ---")
            print('Token Image Url:', logo)
            print('Token Description:', description[9:])
            print(f'Price: $ {price}')
            print('Total Supply:', "{:,}".format(float(total_supply)))
            print('Circulating Supply:', c_supply[10:-1])
            print('24hr Volume: ' "$ " "{:,}".format(volume_24h))
            print(f'% Change 1hr:   % {change_1h}')
            print(f'% Change 24hr:  % {change_24h}')
            print(f'% Change 7d:    % {change_7d}')
            print(f'% Change 30d:   % {change_30d}')
            print(f'% Change 60d:   % {change_60d}')
            print(f'% Change 90d:   % {change_90d}')
            print(f'Token Hash: {hash_num}')
            if bsc_url != None:
                print('BSC Hash Url:', [bsc_url])
                print('BlockChair Url:', [blockchair_url])
            else: 
                print('Etherscan Url:', [etherscan_url])
                print('Ethplorer Url:', [ethplorer_url])
            print('Technical doc url:', value2['urls']['technical_doc'])
            print('Announcements url:', value2['urls']['announcement'])
            print('Source code url:', value2['urls']['source_code'])
            print(f'Website URL: {[url]}')

            print('*****')
            print(f"--- *{token}* {token_name} : Holders Info ---")
            print(f'Number of Holders: {holders[1:-1]}')
            print(f'- {ta}')
            print(f'- {header2[1:]}')
            print('-----')
            print(f"--- Top 10 {token} Holders ---")
####################
### token holder ###
            for addre in card_2.find_all('tr')[:6]:
                if addre.select_one('td:nth-child(1)') != None:
                    rank = addre.select_one('td:nth-child(1)').contents[0]
                    print(f'Rank: {rank}')
                    holder = addre.select_one('td:nth-child(2)').span
                    hash = holder.a['href']
                    hash = re.sub(r'^.*?=', '=', hash)
                    holder_hash = hash[1:]
                    if ': ' in holder.a.text:
                        exchange, holder = holder.a.text.split(':')
                        print(f'Exchance: {exchange}')
                        print(f'Holder: {holder}')
                        print(f'Holder Hash: {holder_hash}')
                        print(f'Holder Hash URL: https://bscscan.com/address/{holder_hash}')
                        quantity = addre.select_one('td:nth-child(3)').contents[0]
                        print(f'Quantity: {quantity}')
                        percentage = addre.select_one('td:nth-child(4)').contents[0]
                        print(f'Percentage: {percentage}')
                    else:
                        holder = holder.a.text
                        no_exchange = 'Exchange: Missing'
                        print(no_exchange)
                        print(f'Holder: {holder}')
                        print(f'Holder Hash: {holder_hash}')
                        print(f'Holder Hash URL: https://bscscan.com/address/{holder_hash}')
                        quantity = addre.select_one('td:nth-child(3)').contents[0]
                        print(f'Quantity: {quantity}')
                        percentage = addre.select_one('td:nth-child(4)').contents[0]
                        print(f'Percentage: {percentage}')
                    print('-----')

bsc_coin_scrape(user_input)