import apikey
import requests
import re
from bs4 import BeautifulSoup


###############
# ## scraping new tokens from CMC html ### 
# source_new = requests.get(f'https://coinmarketcap.com/new/').text
# soup_4 = BeautifulSoup(source_new, 'lxml')
# card_5 = soup_4.find('tbody')
# print('--- New Release Tokens ---')
# for td in card_5.find_all('tr')[:3]:
#     new_num = td.select_one('td:nth-child(2)', style='text').text
#     new_name = td.select_one('td:nth-child(3)', style='text').a.div.div.p.text
#     new_symbol = td.select_one('td:nth-child(3)', style='text').a.div.div.div.p.text
#     new_img = td.select_one('td:nth-child(3)', style='text').a.div.img['src']
#     new_price = td.select_one('td:nth-child(4)', style='text').text
#     new_change1hr = td.select_one('td:nth-child(5)', style='text').span.text
#     new_change24hr = td.select_one('td:nth-child(6)', style='text').span.text
#     new_volume = td.select_one('td:nth-child(8)', style='text').text
#     new_chain = td.select_one('td:nth-child(9)', style='text').div.text
#     new_release = td.select_one('td:nth-child(10)', style='text').text
#     new_hash_x = td.select_one('td:nth-child(3)', style='text').a['href']
#     print(f'Released: {new_release}')
#     print(f'--- *{new_name}* : {new_symbol} ---')
#     print(f'Token Image x: {new_img}')
#     print(f'Price: {new_price}')
#     print(f'% Change 1hr: % {new_change1hr}')
#     print(f'% Change 24hr: % {new_change24hr}')
#     print(f'Volume: {new_volume}')
#     print(f'Blockchain: {new_chain}')
#     print(f'CMC x: https://coinmarketcap.com{new_hash_x}')
#     print('------')
#################
### CMC html scrape token stats ###
url_name = 'ethereum'
hash_url = []
platform = []
source_1 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
bs_cmc1 = BeautifulSoup(source_1, 'lxml')
stats = bs_cmc1.find('div', class_='sc-16r8icm-0 jIZLYs container___E9axz')
body = stats.find('tbody')
for tr in body.find_all('tr'):
    print(tr.th.text)
    print(tr.td.text)

#################
## pulling token data from CMC api ###
### take user input ###
# user_input = input ("Enter the token name:")
# # user_input = ['']
# ### CMC api urls ###
# x_query = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# x_latest = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# x_meta = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
# ### CMC api key ###
# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY' : apikey.cmc_apikey,
# }
# ### parameters ###
# params = {
#     'symbol' : user_input,
# }
# ####################
# ### CMC api token stats ###
# query_data = requests.get(x_query, params=params , headers=headers).json()
# coins_query = query_data['data']

# for key, value in coins_query.items():
#     name = value['name']
#     symbol = value['symbol']
#     slug = value['slug']
#     platform = value['platform']
#     date_added = value['date_added']
#     is_active = ['is_active']
#     total_supply = value['total_supply']
#     circulating_supply = value['circulating_supply']
#     market_cap = value['quote']['USD']['market_cap']        
#     price = value['quote']['USD']['price']
#     volume_24h = value['quote']['USD']['volume_24h']
#     change_1h = value['quote']['USD']['percent_change_1h']
#     change_24h = value['quote']['USD']['percent_change_24h']
#     change_7d = value['quote']['USD']['percent_change_7d']
#     change_30d = value['quote']['USD']['percent_change_30d']
#     change_60d = value['quote']['USD']['percent_change_60d']
#     change_90d = value['quote']['USD']['percent_change_90d']
# # ####################
# ### CMC api token urls ###
#     meta_data = requests.get(x_meta, params=params , headers=headers).json()
#     coins_meta = meta_data['data']
#     token_urls = []
#     for key, value2 in coins_meta.items():
#         if value['name'] == value2['name']:
#             logo = value2['logo']
#             for x in value2['urls']['explorer']:
#                 token_urls.append(x)
# ####################
# ### CMC html scrape token hash ###
#     url_name = name.replace(' ', '-')
#     token_hash = []
#     hash_url = []
#     platform = []
#     source_1 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
#     bs_cmc1 = BeautifulSoup(source_1, 'lxml')
#     for head in bs_cmc1.find_all('div', class_='sc-16r8icm-0 dOJIkS container___2dCiP contractsRow'):
#         if 'Con' in head.div.text:
#             content = head.find('div', class_= 'content___MhX1h')
#             thash = content.div.a['href']
#             hash_url.append(thash)
#             plat  = content.div.a.span.text
#             if 'Eth' in plat:
#                 token_hash.append(thash[27:])
#             else:
#                 token_hash.append(thash[26:]) 

#     token_description = []
#     for desc in bs_cmc1.find_all('div', class_='sc-1lt0cju-0 srvSa'):
#         if desc.div.text != None:
#             des = desc.div
#             # for p in des.find_all('p'):
#             token_description.append(des.text)
# ####################
# ### CMC html scrape token articles ###
#     url_name = name.replace(' ', '-')
#     token_articles = []
#     source_2 = requests.get(f'https://coinmarketcap.com/currencies/{url_name}').text
#     bs_cmc2 = BeautifulSoup(source_2, 'lxml')
#     sp = bs_cmc2.find('div', class_='sc-16r8icm-0 elzRBB container')
#     hold = sp.find('div', class_='sc-16r8icm-0 feGaPs desktopShow___2995-')
#     article = hold.find('div', class_='alexandriaArticles___2__ss')
#     links = article.find('ul')
#     for li in links.find_all('li'):
#         token_articles.append([li.a.text, li.a['href']])
####################
### prints ### 
    # print('*****')
    # print(f"--- *{name}* {symbol} : Price Info ---")
    # print('Token Image x:', logo)
    # print('Token Hash:', token_hash)
    # print('Token Hash URL:', hash_url)
    # print('Token Description:', token_description)
    # print(f'Price: $ {price}')
    # print('Total Supply:', "{:,}".format(float(total_supply)))
    # print('Circulating Supply: $', circulating_supply)
    # print('24hr Volume: ' "$ " "{:,}".format(volume_24h))
    # print(f'% Change 1hr:   % {change_1h}')
    # print(f'% Change 24hr:  % {change_24h}')
    # print(f'% Change 7d:    % {change_7d}')
    # print(f'% Change 30d:   % {change_30d}')
    # print(f'% Change 60d:   % {change_60d}')
    # print(f'% Change 90d:   % {change_90d}')
    # for x in token_urls:
    #     print(f'URL: {x}')
    # for x in token_articles:
    #     print(f'Article: {x}')

