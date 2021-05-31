import apikey
import requests
import re
from bs4 import BeautifulSoup


####################
### scraping new tokens from CMC html ### 
####################
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
    new_hash_x = td.select_one('td:nth-child(3)', style='text').a['href']
    print(f'Released: {new_release}')
    print(f'--- *{new_name}* : {new_symbol} ---')
    print(f'Token Image x: {new_img}')
    print(f'Price: {new_price}')
    print(f'% Change 1hr: % {new_change1hr}')
    print(f'% Change 24hr: % {new_change24hr}')
    print(f'Volume: {new_volume}')
    print(f'Blockchain: {new_chain}')
    print(f'CMC x: https://coinmarketcap.com{new_hash_x}')
    print('------')
####################
### pulling token data from CMC api ###
####################
### take user input ###
user_input = input ("Enter the token name:")
# user_input = ['']
### CMC api urls ###
x_query = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
x_latest = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
x_meta = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
### CMC api key ###
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY' : apikey.cmc_apikey,
}
### parameters ###
params = {
    'symbol' : user_input,
}
####################
### CMC api token stats ###
####################
query_data = requests.get(x_query, params=params , headers=headers).json()
coins_query = query_data['data']

for key, value in coins_query.items():
    name = value['name']
    symbol = value['symbol']
    slug = value['slug']
    platform = value['platform']
    date_added = value['date_added']
    is_active = ['is_active']
    total_supply = value['total_supply']
    circulating_supply = value['circulating_supply']
    market_cap = value['quote']['USD']['market_cap']        
    price = value['quote']['USD']['price']
    volume_24h = value['quote']['USD']['volume_24h']
    change_1h = value['quote']['USD']['percent_change_1h']
    change_24h = value['quote']['USD']['percent_change_24h']
    change_7d = value['quote']['USD']['percent_change_7d']
    change_30d = value['quote']['USD']['percent_change_30d']
    change_60d = value['quote']['USD']['percent_change_60d']
    change_90d = value['quote']['USD']['percent_change_90d']
    ####################
    ### CMC api token urls ###
    ####################
    meta_data = requests.get(x_meta, params=params , headers=headers).json()
    coins_meta = meta_data['data']
    token_urls = []
    for key, value2 in coins_meta.items():
        if value['name'] == value2['name']:
            logo = value2['logo']
            for x in value2['urls']['explorer']:
                token_urls.append(x)
    ####################
    ### CMC html scrape token stats1 ###
    ####################
    url_name = name.replace(' ', '-')
    source_1 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
    bs_cmc1 = BeautifulSoup(source_1, 'lxml')
    block1 = bs_cmc1.find('div', class_='statsBlock___11SXA').div
    mc1_text = block1.div.text
    mc1_2text = block1.select_one('div:nth-child(2)').div.text
    mc1_change = []
    if '-' in mc1_2text:
        mc1_change.append('-' + block1.select_one('div:nth-child(2)').span.text)
    else: 
        mc1_change.append('+' + block1.select_one('div:nth-child(2)').span.text)
    ################
    ### Volume stats ###
    b2 = bs_cmc1.find('div', class_='hide___2JmAL statsContainer___2uXZW')
    block2 = b2.select_one('div:nth-child(3)')
    v_text = block2.div.div.text
    v_2text = block2.find('div', class_='statsItemRight___yJ5i-').div.text
    ################
    ### Circulating stats ###
    b3 = b2.select_one('div:nth-child(4)')
    ts_text = b3.select_one('div', class_='sc-16r8icm-0 lpaFj statsLabel___1Mkfd').text
    ts_2text = b3.find('div', class_='sc-16r8icm-0 kkJvVq').text
    ####################
    ### CMC html scrape token stats2 ###
    ####################
    stats = bs_cmc1.find('div', class_='sc-16r8icm-0 jIZLYs container___E9axz')
    body = stats.find('tbody')
    ### Price stats ###
    tr2 = body.select_one('tr:nth-child(2)')
    tr2_text = tr2.th.text
    tr2td_text = tr2.td.span.text
    tr2td_change = []
    if '-' in tr2td_text:
        tr2td_change.append('-' + tr2.td.div.span.text)
    else: 
        tr2td_change.append('+' + tr2.td.div.span.text)
    ### 24hr change stats ###
    tr3 = body.select_one('tr:nth-child(3)')
    tr3_text = tr3.th.text
    tr3td_text = tr3.td.text
    ### Trading volume stats ###
    tr4 = body.select_one('tr:nth-child(4)')
    tr4_text = tr4.th.text
    tr4td_text = tr4.td.text
    tr4td_change = []
    if '-' in tr4td_text:
        tr4td_change.append('-' + tr4.td.div.span.text)
    else: 
        tr4td_change.append('+' + tr4.td.div.span.text)
    ### Market dominance stats ###
    tr5 = body.select_one('tr:nth-child(6)')
    tr5_text = tr5.th.text
    tr5td_text = tr5.td.text
    ####################
    ### CMC html scrape token hash ###
    ####################
    url_name = name.replace(' ', '-')
    token_hash = []
    hash_url = []
    platform = []
    source_1 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
    bs_cmc1 = BeautifulSoup(source_1, 'lxml')
    ### Token hash ###
    for head in bs_cmc1.find_all('div', class_='sc-16r8icm-0 dOJIkS container___2dCiP contractsRow'):

        if 'Con' in head.div.text:
            content = head.find('div', class_= 'content___MhX1h')
            thash = content.div.a['href']
            hash_url.append(thash)
            plat  = content.div.a.span.text
            if 'Eth' in plat:
                token_hash.append(thash[27:])
            else:
                token_hash.append(thash[26:]) 
    ### Token description ###
    token_description = []
    for desc in bs_cmc1.find_all('div', class_='sc-1lt0cju-0 srvSa'):
        if desc.div.text != None:
            des = desc.div
            token_description.append(des.text)
    ####################
    ### CMC html scrape token articles ###
    ####################
    url_name = name.replace(' ', '-')
    token_articles = []
    source_2 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
    bs_cmc2 = BeautifulSoup(source_2, 'lxml')
    sp = bs_cmc2.find('div', class_='sc-16r8icm-0 elzRBB container')
    hold = sp.find('div', class_='sc-16r8icm-0 feGaPs desktopShow___2995-')
    article = hold.find('div', class_='alexandriaArticles___2__ss')
    links = article.find('ul')
    for li in links.find_all('li'):
        token_articles.append([li.a.text, li.a['href']])
    ####################
    ## prints ### 
    ####################
    print('*****')
    print(f"--- *{name}* {symbol} : Price Info ---")
    print('Token Image x:', logo)
    print('Token Hash:', token_hash)
    print('Token Hash URL:', hash_url)
    print('Token Description:', token_description)
    print(f'Price: $ {price}')
    print('Total Supply:', "{:,}".format(float(total_supply)))
    print('Circulating Supply: $', circulating_supply)
    print('24hr Volume: ' "$ " "{:,}".format(volume_24h))
    print(f'% Change 1hr:   % {change_1h}')
    print(f'% Change 24hr:  % {change_24h}')
    print(f'% Change 7d:    % {change_7d}')
    print(f'% Change 30d:   % {change_30d}')
    print(f'% Change 60d:   % {change_60d}')
    print(f'% Change 90d:   % {change_90d}')
    for x in token_urls:
        print(f'URL: {x}')
    for x in token_articles:
        print(f'Article: {x}')
    print('------')
    print(f'Market Cap: $ {mc1_2text}')
    print(f'% Change Market Cap: % {mc1_change}')
    print(f'Token Volume: $ {v_2text}')
    print(f'Circulating Supply: {ts_2text}')
    print(f'Token Price: $ {tr2td_text}')
    print(f'Token Price Change: $ {tr2td_change}')
    print(f'24hr low / 24hr high: {tr3td_text}')
    print(f'Trading Volume: {tr4td_text}')
    print(f'Market Dominance: {tr5td_text}')

