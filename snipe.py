# Buy products from bestbuy or walmart from SKU/ProductID

# Required modules
import json
from wmBot import *
from helpers import *
from datetime import datetime
import time


# User settings
settings = {
    'email': 'XXXX@XXXX.XXX',
    'firstName': 'XXXXX',
    'lastName': 'XXXXX',
    'addressOne': 'XXXXXXXXXX',
    'addressTwo': '',
    'city': 'XXXXXX',
    'postalCode': 'XXX XXX',
    'province': 'XX',
    'phone': 'XXXXXXXXXX'
}
billing = {
    'addressOne': 'XXXXXXXX',
    'postalCode': 'XXX XXX',
    'ccNum': 'XXXXXXXXXXXXXXXX',
    'ccExpM': 'XX',
    'ccExpY': 'XX',
    'ccSecCode': 'XXX'
}

# Main
wmBot(link,settings, billing)

# User customized variables
check_bestbuy = True
check_walmart = True

SKU_bb = [14962185,14962184]
ID_wm = [6000202198562,6000202198823,6000201790922,6000202282463,6000202283428]

stopOnFound = True
sleepTime = int(60 * 1)
found = False

while (not found) and (stopOnFound):
    # hold links that are in stock and open them after each iteration
    inStockLinks = []

    # else clear console so it doesn't get cluttered...
    if (not found): clear()

    # get and print current time
    now = datetime.now()
    print('\n\n\033[1m{}[{} {}]{}\033[0m\n'.format('-'*30,'DateTime:', now.strftime("%Y-%m-%d %H:%M:%S") , '-'*60))

    if check_bestbuy:
        # for SKUs that best buy didnt delete...
        for sku in SKU_bb:
            item = checkSKU_bb(sku)

            if outputdata('bestbuy', item):
                # Update flag, Append time and which SKU has stock to logfile
                found = True
                log = '[{}][{} - BestBuy]: {} has {} units available.\n'.format(now.strftime("%Y-%m-%d %H:%M:%S"), item['sku'], item['name'], item['availability']['onlineAvailabilityCount'])
                writelog(log)

                # Open in browser to enter queue



    if check_walmart:
        # for SKUs for walmart
        for pid in ID_wm:
            item = checkID_wm(pid)

            if outputdata('walmart', item):
                # Update flag, Append time and which SKU has stock to logfile
                found = True
                log = '[{}][{} - Walmart]: {} has {} units available.\n'.format(now.strftime("%Y-%m-%d %H:%M:%S"), item['sku'], item['name'], item['availableQuantity'])
                writelog(log)

                # Open in browser in new child process, remove product id from list to check
                ID_wm.remove(pid)
                wmBot(item['productUrl'],settings, billing)
                break



    # Exit if anything available
    if stopOnFound and found: break

    # show time until next check
    print('\n\n\n')
    for n in range(sleepTime):
        print('\r   Checking again in {}s'.format(sleepTime-n), end='   ')
        time.sleep(1)
    print()
