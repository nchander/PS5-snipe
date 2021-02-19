# Buy products from bestbuy or walmart from SKU/ProductID

# Required modules
import json
from wmBot import *
from helpers import *
from datetime import datetime
import time
import argparse


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

SKU_bb = [14962185,14962184]
ID_wm = [6000202198562,6000202198823,6000201790922,6000202282463,6000202283428]



# Read args from command line input and update default values
parser = argparse.ArgumentParser()

# Create options and setup
parser.add_argument('-w', required=False, action='store_true', help='Check Walmart stock')
parser.add_argument('-b', required=False, action='store_true', help='Check BestBuy stock')
parser.add_argument('-s', required=False, action='store_true', help='Stop scanning once stock is available')
parser.add_argument('-r', required=True, default=60, type=int, help='Delay in seconds between scans')
parser.add_argument('-m', required=True, type=int, choices=[1,2], help='Mode of operation. 1: scan, 2: scan and buy')

# Get arg values
arguments = parser.parse_args()
check_walmart = arguments.w
check_bestbuy = arguments.b
stopOnFound = arguments.s
sleepTime = arguments.r
mode = arguments.m

# flag current stock
found = False

while (not found):
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

                # Open in browser to enter queue/buy if mode is 2
                # if (mode == 2):



    if check_walmart:
        # for SKUs for walmart
        for pid in ID_wm:
            item = checkID_wm(pid)

            if outputdata('walmart', item):
                # Update flag, Append time and which SKU has stock to logfile
                found = True
                log = '[{}][{} - Walmart]: {} has {} units available.\n'.format(now.strftime("%Y-%m-%d %H:%M:%S"), item['sku'], item['name'], item['availableQuantity'])
                writelog(log)

                # If in buy mode, open in browser in new child process, remove product id from list to check
                if (mode == 2):
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
