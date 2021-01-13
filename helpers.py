import json
import requests
import os

# change depending on host os. uncomment depending on host os
def clear():
    os.system('clear')      # Linux/MacOS
    # os.system('cls')      # Windows


# Get BB json response for category id
def checkCategory_bb(cat):
    # Best buy Categories
    # 17583383 - PS5 consoles

    payload = {'currentRegion':'ON','include':'all', 'lang':'en-CA'}
    head = {
    'Host': 'www.bestbuy.ca',
    'filename': '/api/v2/json/category/{}'.format(str(cat)),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': '*/*',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }

    return requests.get('https://{}{}'.format(head['Host'],head['filename']), headers=head, params=payload).json()

# Get BB json response for SKU
def checkSKU_bb(SKU):
    # Best buy SKUs
    # 14962185 - PS5 Console
    # 14962184 - PS5 Console (Digital Edition)
    # b0014216 - PS5 with 2 controllers bundle

    payload = {'currentRegion':'ON','include':'all', 'lang':'en-CA'}
    head = {
    'Host': 'www.bestbuy.ca',
    'filename': '/api/v2/json/product/{}'.format(str(SKU)),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': '*/*',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip',
    'Referer': 'https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }

    return requests.get('http://{}{}'.format(head['Host'],head['filename']), headers=head, params=payload).json()

# Get walmart product information json
def checkID_wm(id):

    # --- Product ID --------- SKU ---------------- Name --------------
    #   6000202198562       6000202198563       PS5 (Disc)
    #   6000202198823       6000202198824       PS5 (Digital Edition)
    #   6000201790922       6000201790923       PS5 (Disc) with extra DualSense
    #   6000202282463       6000202282464       PS5 (Disc) with extra DualSense + Spiderman
    #   6000202283428       6000202283429       PS5 (Disc) with extra DualSense + Black Ops

    # Map product ID to SKU,Name
    m = {
    6000202198562: [6000202198563, "PS5 Console (Disc)"],
    6000202198823: [6000202198824, "PS5 Console (Digital Edition)"],
    6000201790922: [6000201790923, "PS5 Console (Disc) with extra DualSense"],
    6000202282463: [6000202282464, "PS5 Console (Disc) with extra DualSense + Spiderman"],
    6000202283428: [6000202283429, "PS5 Console (Disc) with extra DualSense + Black Ops"]
    }

    payload = {
    "fsa":"M6H",
    "products": [{"productId":"6000202198562", "skuIds": [str(m[id][0])]}],
    "lang":"en",
    "pricingStoreId":"3106",
    "fulfillmentStoreId":"3106",
    "experience":"whiteGM"
    }

    head = {
    'Host':'www.walmart.ca',
    'filename': '/api/product-page/v2/price-offer',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'content-type': 'application/json',
    'Origin': 'https://www.walmart.ca',
    'Referer': 'https://www.walmart.ca/en/ip/{}'.format(id),
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'max-age=0, no-cache'
    }


    res = requests.post('https://{}{}'.format(head['Host'],head['filename']), headers=head, json=payload).json()

    for i in res['offers'].keys():
        if (res['offers'][i]['sellerInfo']['en'] == 'Walmart') and (res['offers'][i]['sellerId'] == '0'):

            # Add link and name attributes then return
            update = {
            'productUrl': 'https://www.walmart.ca/en/ip/{}'.format(id),
            'name': m[id][1],
            'sku': m[id][0]
            }

            res['offers'][i].update(update)
            return res['offers'][i]

# Output SKU product info to store/log, return 1 if stock is available online
def outputdata(store,item):

    # Best buy
    if store == 'bestbuy':
        avail = item.get('availability')
        cat = checkCategory_bb(int(item['primaryParentCategoryId']))

        print('{:>20} {} ({})'.format('Product (SKU):',item['name'], item['sku']))
        # print('{:>10}{:>20} {} ({})'.format('','Category (ID):',cat['name'], cat['id']))
        print('{:>10}{:>20} {}{}'.format('','Price:','$',item['regularPrice']))
        # print('{:>10}{:>20} {}{}'.format('','Sale Price:','$',item['salePrice']))
        # print('{:>10}{:>20} {}'.format('','Has Promotion:',item['hasPromotion']))

        print('{:>10}{:>20} {}'.format('','Available Online:',avail['isAvailableOnline']))
        print('{:>10}{:>20} {}'.format('','Online Stock:',avail['onlineAvailabilityCount']))
        print('{:>10}{:>20} {}'.format('','Next Stock Update:',avail['onlineAvailabilityUpdateDate'].replace('T',' ')))
        print('{:>10}{:>20} {}\n'.format('','Link:',item['productUrl']))

        return 1 if ((avail['isAvailableOnline']) or (avail['onlineAvailabilityCount'] > 0)) else 0

    # Walmart
    if store == 'walmart':
        print('{:>20} {} ({})'.format('Product (SKU):',item['name'], item['sku']))
        print('{:>10}{:>20} {}{}'.format('','Price:','$',item['pricePerUnit']))
        print('{:>10}{:>20} {} ({})'.format('','Seller (ID):',item['sellerInfo']['en'], item['sellerId']))
        print('{:>10}{:>20} {}'.format('','Available Online:',item['gmAvailability']))
        print('{:>10}{:>20} {}'.format('','Online Stock:',item['availableQuantity']))
        print('{:>10}{:>20} {}\n'.format('','Link:',item['productUrl']))

        return 1 if ((item['gmAvailability'] != 'OutOfStock') or (item['availableQuantity'] > 0)) else 0

# write data to logfile - break up logs later...
def writelog(s):
    with open("./log.txt", "a+") as f:
        f.write(s)
        f.close()
