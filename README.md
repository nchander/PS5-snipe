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
   `python3 ./snipe`
