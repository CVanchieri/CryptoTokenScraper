from bs4 import BeautifulSoup
import requests
import csv 
import re

token_hash = '0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe'

def bsc_scanner(token_hash):
    source_info =requests.get(f'https://bscscan.com/token/{token_hash}').text
    source_holders =requests.get(f'https://bscscan.com/token/tokenholderchart/{token_hash}').text
    soup_1 = BeautifulSoup(source_info, 'lxml')
    soup_2 = BeautifulSoup(source_holders, 'lxml')
    overview = soup_1.find('div', class_='row mb-4')

    name = overview.find('div', class_='font-weight-medium').b.text
    supply = overview.find('span', class_='hash-tag text-truncate').text
    c_supply = overview.find('span', class_='text-secondary ml-1').text
    holders = overview.find('div', class_='mr-3').text
    print(f'--- Token name: *{name}* ---')
    print(f'Total Supply: {supply}')
    print(f'Circulating Supply: {c_supply[10:-1]}')
    print(f'Current Holders: {holders[1:-1]}')

    for card in soup_1.find_all('div', class_='col-md-6'):
        if card.find('h2', class_='card-header-title') != None and card.find('div', class_='col-md-4').text == 'Contract:':
                contract = card.find('a', class_='text-truncate d-block mr-2').text
                url = card.find('div', id='ContentPlaceHolder1_tr_officialsite_1')
                url = url.find('div', class_='col-md-8').a['href']
                print(f'Token Hash: {contract}')
                print(f'Token Hash URL: https://bscscan.com/address/{contract}')
                print(f'Website URL: {url}')

    card_2 = soup_2.find('div', id='ContentPlaceHolder1_resultrows')
    ta = soup_2.find('div', class_='mb-0').p.text[1:-1]
    ta = ta.replace('token', 'tokens')
    ta = ta.replace('tokenss', 'tokens')
    print('-----')
    print(ta)
    print('-----')
    card_3 = soup_2.find('div', class_='card-header py-4')
    header2 = card_3.find('div', class_='col-md-6').text
    print(header2)
    print('-----')
    print('--- Top token holders --')
    for addre in card_2.find_all('tr'):
        if addre.select_one('td:nth-child(1)') != None:
            rank = addre.select_one('td:nth-child(1)').contents[0]
            print('-----')
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
                no_exchange = 'Exchange not found'
                print('no_exchange')
                print(f'Holder: {holder}')
                print(f'Holder Hash: {holder_hash}')
                print(f'Holder Hash URL: https://bscscan.com/address/{holder_hash}')
                quantity = addre.select_one('td:nth-child(3)').contents[0]
                print(f'Quantity: {quantity}')
                percentage = addre.select_one('td:nth-child(4)').contents[0]
                print(f'Percentage: {percentage}')

bsc_scanner(token_hash)