# Bestbuy/Walmart Sniper (Canada)
Automation script to quickly add products to cart and checkout. Can be used for any product as long as you adjust for the product id/sku
Purely for education and not for scalping...

## Prerequisites
   Google chrome (v87.X.X)
   Python (v3.X)
   pip

## Install packages from pip
   `pip install -r requirements.txt`

## Usage
#### Configure
Edit the following in `./snipe.py` for user details. Make sure postal code has the space.
```
settings = {
    'firstName': 'XXXXXX',
    'lastName': 'XXXXXXXXX',
    'addressOne': 'XXXXXXXXX',
    'addressTwo': '',
    'city': 'XXXXXXXX',
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
```



#### Run

 `python3 snipe.py [-h] [-w] [-b] [-s] -r R -m {1,2}`



##### Arguments and Flags:

` -h`, `--help` show this help message and exit

 `-w`     Check Walmart stock

 `-b`     Check BestBuy stock

 `-s`     Stop scanning once stock is available

 `-r R`    Delay in seconds between scans

 `-m {1,2}`  Mode of operation. 1: scan, 2: scan and buy



##### Example

`python3 snipe.py -w -b -s -r 60 -m1`

This will search BestBuy and Walmart every 60 seconds, stopping once available stock is found and will not attempt to purchase the available product. 



## To Do

1. Fix BestBuy purchasing now that queue likely isn't a problem
2. Read links to check from text file so it can be easily used for any product
3. Create setup script for user to input billing and shipping details
4. Re-enable single product mode for quickly running program for a user given link from command line arguments
