# Bestbuy/Walmart Sniper
Automation script to quickly add products to cart and checkout.

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



If on windows, change the command run by `clear()` in `./helpers.py` to this:

```
def clear():
    # os.system('clear')    # Linux/MacOS
    os.system('cls')    # Windows
```



#### Run

 `python3 snipe.py [-h] [-w] [-b] [-s] -r R -m {1,2}`



##### Arguments:

` -h`, `--help` show this help message and exit

 `-w`     Check Walmart stock

 `-b`     Check BestBuy stock

 `-s`     Stop scanning once stock is available

 `-r R`    Delay in seconds between scans

 `-m {1,2}`  Mode of operation. 1: scan, 2: scan and buy



##### Example

`python3 snipe.py -w -b -s -r 60 -m1`



This will search BestBuy and Walmart every 60 seconds, stopping once available stock is found and will not attempt to purchase the available product. 