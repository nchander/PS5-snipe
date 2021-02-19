from selenium import webdriver as WD
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path
import time
import random

# TODO:
# - only use selenium to get uid of cart, POST requests are faster when not blocked
#   - Figure out how to bypass manual checkout without getting blocked


# wait random between x and y seconds
def waitRand():
    time.sleep(random.randrange(15,30) / 10 )

class wmBot:

    # map button names to xpaths
    elemPaths = {
        'addToCart': "/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/button[1]",
        'checkout': "/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[3]/div[2]/button[1]",
        'proceedToCheckout': "/html/body/div[1]/div/div/div[3]/div[4]/div[2]/div/div[1]/div[11]/a/button",
        'emailGuest': '//*[@id="email"]',
        'nextGuest': "/html/body/div[1]/div/div/div[1]/div[3]/main/div/div[1]/div[1]/div[2]/form/div/div[5]/button",
        'selectShipping': '//*[@id="shipping-tab"]/div/div/div/div/span[2]',
        'firstName': '//*[@id="firstName"]',
        'lastName': '//*[@id="lastName"]',
        'addressAutoComplete0': '/html/body/div[5]/div[1]/div[2]/div[1]',
        'addressOne': '//*[@id="address1"]',
        'addressTwo': '//*[@id="address2"]',
        'province': '//*[@id="province"]/option[10]',
        'city': '//*[@id="city"]',
        'postalCode': '//*[@id="postalCode"]',
        'phone': '//*[@id="phoneNumber"]',
        'nextShipping': '//*[@id="shippingAddressForm"]/div[3]/button',
        'nextShippingFinal': '//*[@id="step2"]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/button',
        'ccNum': '//*[@id="cardNumber"]',
        'ccExpM': '//*[@id="expiryMonth"]',
        'ccExpY': '//*[@id="expiryYear"]',
        'ccSecCode': '//*[@id="securityCode"]',
        'changeBilling': '//*[@id="billingForm"]/div/div[3]/div/label',
        'billingAddressOne': '//*[@id="address1"]',
        'billingPostalCode': '//*[@id="postalCode"]',
        'applyNewBilling': '//*[@id="billingForm"]/div/button[1]',
        'checkoutApply': '//*[@id="billingForm"]/div/button',
        'placeOrder': '/html/body/div[1]/div/div/div[1]/div[3]/div/div/div/button'
    }

    def __init__(self, link, purchaseInfo, billing):
        self.link = link
        self.purchaseInfo = purchaseInfo
        self.billing = billing

        # Setup driver
        options = WD.ChromeOptions()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Set driver options to avoid bot detection
        #self.driver = WD.Firefox()
        self.driver = WD.Chrome(options=options, executable_path=binary_path)
        self.driver.delete_all_cookies()
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"})
        self.driver.maximize_window()
        print(self.driver.execute_script("return navigator.userAgent;"))


        # -- Testing ----------------------------------------------------------
        # Eventually make them into their own functions... reuse drivers, save cc

        # Open link on the driver, start at home so origin isn't messed
        time.sleep(2)
        self.driver.get(link)
        time.sleep(3)

        # Add product from link to cart and go to checkout
        self.clickElement('addToCart')
        self.clickElement('checkout')
        self.clickElement('proceedToCheckout')

        # Select guest checkout, enter email
        self.fillForm('emailGuest', self.purchaseInfo['email'])
        self.clickElement('nextGuest')

        # comment out of you dont get captchas - add death by captcha maybe
        time.sleep(10)

        # select shipping option instead of default pickup - uncomment if there is pickup option
        self.clickElement('selectShipping')

        # fill out shipping info
        for i in ['firstName', 'lastName', 'addressOne', 'province', 'city', 'postalCode', 'phone']:
            self.fillForm(i, self.purchaseInfo.get(i))

        # go to payment section - comment if cookie has address saved
        self.clickElement('nextShipping')

        # Select first shipping option
        self.clickElement('nextShippingFinal')

        # Enter CC information and billing address
        for i in ['ccNum','ccExpM','ccExpY','ccSecCode']:
            self.fillForm(i,self.billing.get(i))


        # Change billing address if different from shipping, press apply
        self.click('changeBilling')
        self.fillForm('billingAddressOne', self.billing['addressOne'])
        self.fillForm('billingPostalCode', self.billing['postalCode'])
        self.clickElement('checkoutApply')

        # Place order
        self.clickElement('placeOrder')


        # ---- End test -------------------------------------------------------


    # login so you can checkout faster...
    def login(self, username, password):
        print('not yet implemented...')

    # login so you can checkout faster...
    def guestCheckout(self):
        print('not yet implemented...')

    # login so you can checkout faster...
    def authdCheckout(self, username, password):
        print('not yet implemented...')

    # wait up to 10 seconds for button to be clickable, then click it
    def clickElement(self,e):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.elemPaths.get(e)))
        )
        waitRand()
        element.click()


    # fill input form from element e with input
    def fillForm(self,e,input):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.elemPaths.get(e)))
        )
        waitRand()
        element.send_keys(input)
