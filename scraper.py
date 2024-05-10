from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from extensions import db, app
from models import Product
from datetime import datetime
from time import sleep
import json, re, random


options = Options()
#options.add_argument('--headless=new')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')

# Set the path to your chromedriver.exe file
chrome_driver_path = "C:\\path\\to\\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Set the path to your Chrome executable
chrome_binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
options.binary_location = chrome_binary_location

# Pass the options when creating the driver instance
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(0.5)

app.app_context().push()


# Pass the options when creating the driver instance
driver = webdriver.Chrome(service=service, options=options)
# driver.implicitly_wait(0.5)


#scraper for H&M
def HM(search, sex):
    '''
        Scrapes hm.com using users prefernces  
    '''
    # Go to the webpage
    driver.get(f'https://www2.hm.com/en_us/search-results.html?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article > div.image-container'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, '#main-content > div.deck-text.section > p')
        if len(error_messages) > 0:
            print("No products found on HM")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load H&M.")
        fallback_brand_picker(search, sex)

    print("Loaded H&M.")
    # Find all product items
    products = driver.find_elements(By.CLASS_NAME, 'product-item')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CSS_SELECTOR, 'div.item-details > h3 > a').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            # Price
            price = product.find_element(By.CSS_SELECTOR, 'div.item-details > strong > span').text
            price = re.sub(r'\$ ', '', price)

            # Color(s): Find the ul with class 'list-swatches' and then find all li with class 'item' within
            swatches_ul = product.find_elements(By.CLASS_NAME, 'list-swatches')
            color_elements = [li.find_element(By.TAG_NAME, 'a') for ul in swatches_ul for li in ul.find_elements(By.CLASS_NAME, 'item')]
            colors = [elem.get_attribute('title') for elem in color_elements if elem.get_attribute('title')]
            colors_json = json.dumps(colors)

            # Image
            image = product.find_element(By.CLASS_NAME, 'item-image').get_attribute("src")

            # Link
            link = product.find_element(By.CLASS_NAME, 'item-link').get_attribute("href")

            #adding to db
            new_product = Product(name=name, price=float(price), color=colors_json, image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", e)


    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for Banana Republic
def BR(search, sex):
    # Go to the webpage
    driver.get(f'https://bananarepublicfactory.gapfactory.com/browse/search.do?searchText={search}')

    all_products = []

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, 'div > p.error-message-text')
        if len(error_messages) > 0:
            print("No products found on BR")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load BR.")
        fallback_brand_picker(search, sex)

    print("Loaded BR.")
    # Find all product cards
    products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')

    # Extract details from each product card
    all_products = []
    for product in products:
        try:
            # Extract product name
            name = product.find_element(By.CSS_SELECTOR, 'section > div > div > div > div > a > div').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)

            # Extract price details
            try:
                price = product.find_element(By.CSS_SELECTOR, 'div.product-card-price > div > div > div > span').text
            except NoSuchElementException:
                price = product.find_element(By.CSS_SELECTOR, 'div.product-card-price > div > div > span').text
                
            price = re.sub(r'Was \$', '', price).strip()

            # Extract image details
            image = product.find_element(By.CSS_SELECTOR, 'div.product-card > div > a > img').get_attribute('src')

            # Extract product link
            link = product.find_element(By.CSS_SELECTOR, 'div.cat_product-image > a').get_attribute('href')

            new_product = Product(name=name, price=float(price), color='-', image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append to list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print(f"An error occurred while processing a product: {e}")

    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for Forever 21
def F21(search, sex):
    # Go to the webpage
    driver.get(f'https://www.forever21.com/us/search?q={search}&lang=en_US')

    # Initialize an empty list to hold all product details
    all_products = []
    
    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-tile__media.product-tile__media--default > div > div > div'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, 'div.search-results--null-page.max-width--large.gutter--normal > div')
        if len(error_messages) > 0:
            print("No products found on F21")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load F21.")
        fallback_brand_picker(search, sex)

    print("Loaded F21.")
    products = driver.find_elements(By.CLASS_NAME, 'product-grid__item')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CLASS_NAME, 'product-tile__name').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            # Price
            try:
                price = product.find_element(By.CLASS_NAME, 'price__default').text
                price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
                price = re.sub(r"\$\d+\.\d+ - ", "", price)
                price = re.sub("Now ", "", price)
            except NoSuchElementException:
                price = "Price not found"

            # Color(s)
            colors = [img.get_attribute('title') for img in product.find_elements(By.CSS_SELECTOR, '.product-tile__swatches img')]
            colors_json = json.dumps(colors)
            # Image
            try:
                image_element = product.find_element(By.CLASS_NAME, 'product-tile__image')
                image = image_element.get_attribute("src")
            except NoSuchElementException:
                image = ""

            # Link
            try:
                link_element = product.find_element(By.CLASS_NAME, 'product-tile__name')
                link = link_element.get_attribute("href")
            except NoSuchElementException:
                link = ""

            #adding to db
            price2 = price[1::]
            new_product = Product(name=name, price=float(price2), color=colors_json, image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", e)


    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for UNIQLO
def UNIQLO(search, sex):
    # Go to the webpage
    driver.get(f'https://www.uniqlo.com/us/en/search?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.fr-ec-product-tile__image > div > img'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, 'section > div > div> div > div > p')
        if len(error_messages) > 0:
            print("No products found on UNIQLO")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load UNIQLO.")
        fallback_brand_picker(search, sex)

    print("Loaded UNIQLO.")
    products = driver.find_elements(By.CLASS_NAME, 'fr-ec-product-tile-resize-wrapper')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CLASS_NAME, 'fr-ec-title').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            # Price
            try:
                price = product.find_element(By.CLASS_NAME, 'fr-ec-price-text').text
                price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
                price = re.sub(r"\$\d+\.\d+ - ", "", price)
                price = re.sub("Now ", "", price)
            except NoSuchElementException:
                price = "Price not found"

            # Color(s)
            colors = []  # Initialize an empty list to store colors
            try:
                # Find all elements containing color images
                color_elements = product.find_elements(By.CLASS_NAME, 'fr-ec-chip__default-image')
                for color_element in color_elements:
                    image_url = color_element.get_attribute("src")
                    color_code_match = re.search(r"goods_(\d+)_", image_url)
                    if color_code_match:
                        color_code = int(color_code_match.group(1))
                        # Map color code to color name based on given ranges
                        if 0 <= color_code <= 1:
                            colors.append("White")
                        elif 2 <= color_code <= 8:
                            colors.append("Grays")
                        elif color_code == 9:
                            colors.append("Black")
                        elif 10 <= color_code <= 19:
                            colors.append("Reds")
                        elif 20 <= color_code <= 29:
                            colors.append("Oranges")
                        elif 30 <= color_code <= 39:
                            colors.append("Beige/Browns")
                        elif 40 <= color_code <= 49:
                            colors.append("Yellows")
                        elif 50 <= color_code <= 59:
                            colors.append("Greens")
                        elif 60 <= color_code <= 68:
                            colors.append("Blues")
                        elif color_code == 69:
                            colors.append("Navy")
                        elif 70 <= color_code <= 79:
                            colors.append("Purples")
                        elif 80 <= color_code <= 99:
                            colors.append("Other")
            except NoSuchElementException:
                # If no elements found, keep colors list empty
                pass
            
            # Image
            try:
                image_element = product.find_element(By.CLASS_NAME, 'fr-ec-image__img')
                image = image_element.get_attribute("src")
            except NoSuchElementException:
                image = ""

            # Link
            try:
                link_element = product.find_element(By.CLASS_NAME, 'fr-ec-tile')
                link = link_element.get_attribute("href")
            except NoSuchElementException:
                link = ""

            #adding to db
            colors_json = json.dumps(colors)
            price2 = price[1::]
            new_product = Product(name=name, price=float(price2), color=colors_json, image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", e)


    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for ZARA
def ZARA(search, sex):
    '''
        A function that scrapes data from the website Zara which includes product name, color, price, img, and url
    '''
    if sex == "Female":
        gender = "WOMAN"
    else:
        gender = "MAN"

    # Go to the webpage
    driver.get(f'https://www.zara.com/us/en/search?searchTerm={search}&section={gender}')

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a > div > div > div > div > div.carousel__viewport'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, 'section > div.search-products-message-block > div')
        if len(error_messages) > 0:
            print("No products found on Zara")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load Zara.")
        fallback_brand_picker(search, sex)

    print("Loaded ZARA.")
    # Find all product items
    products = driver.find_elements(By.CSS_SELECTOR, "li._product")
    
    # Initialize an empty list to hold all product details
    all_products = []
    
    # Loop through each product and extract the details
    for product in products[:10]:  # Limiting to first 10 products for brevity
        try:
            # Product name
            name_element = product.find_element(By.CSS_SELECTOR, 'h2')
            name = name_element.text if name_element else "Name not found"
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            
            # Price
            price = product.find_element(By.CSS_SELECTOR, '.price__amount-wrapper .price__amount .money-amount__main').text
            price = re.sub(r'\$ ', '', price).strip()
            # Image
            try:
                image_element = product.find_element(By.CSS_SELECTOR, 'img.media-image__image')
                image = image_element.get_attribute("src")
            except NoSuchElementException:
                image = "Image not found"
            
            # Link
            try:
                link_element = product.find_element(By.CSS_SELECTOR, 'a.product-link.product-grid-product__link')
                link = link_element.get_attribute("href")
            except NoSuchElementException:
                link = "Link not found"
            
            #adding to db
            new_product = Product(name=name, price=float(price), color="-", image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details:", e)
    

    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for H&M
def SHEIN(search, sex):
    '''
        Scrapes shein.com using users prefernces  
    '''
    # Go to the webpage
    driver.get(f'https://us.shein.com/pdsearch/{search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-list-v2__container > section'))
        )
        error_messages = driver.find_elements(By.CSS_SELECTOR, '#product-list-v2 > div > div.search-empty > p')
        if len(error_messages) > 0:
            print("No products found on Shein")
            fallback_brand_picker(search, sex)
        else:
            pass
    except:
        print("Failed to load Shein.")
        fallback_brand_picker(search, sex)

    print("Loaded SHEIN.")
    # Find all product items
    products = driver.find_elements(By.CSS_SELECTOR, 'section.product-card')
    # Loop through each product and extract the details
    for product in products[:4]:
        try:

            # Product name
            name = product.find_element(By.CLASS_NAME, 'goods-title-link').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            # Price
            price = product.find_element(By.CSS_SELECTOR, '.product-card__price span').text.strip('$')
            # Image
            image = product.find_element(By.CSS_SELECTOR, '.crop-image-container img').get_attribute('src')
            # Link
            link = product.find_element(By.CSS_SELECTOR, '.product-card__top-wrapper a').get_attribute('href')
            
            #adding to db
            new_product = Product(name=name, price=float(price), color='-', image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", e)


    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for NIKE
def NIKE(search, sex):
    '''
        Scrapes nike.com using users prefernces  
    '''
    # Go to the webpage
    driver.get(f'https://www.nike.com/w?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for the product cards to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.product-card__img-link-overlay'))
        )
    except:
        print("Failed to load Nike.")
        fallback_brand_picker(search, sex)

    print("Loaded NIKE.")
    # Find all product items
    products = driver.find_elements(By.CSS_SELECTOR, '.product-card__body')
    # Loop through each product and extract the details
    for product in products[:10]:
        try:

            # Product name
            name1 = product.find_element(By.CSS_SELECTOR, '.product-card__title').text
            name2 = product.find_element(By.CSS_SELECTOR, '.product-card__subtitle').text
            name = f"{name1} - {name2}"
            name = re.sub(r'(?<!\\)"', r'\\"', name)

            # Price
            price = product.find_element(By.CSS_SELECTOR, '.product-price.is--current-price').text.strip('$')
            # Image
            image = product.find_element(By.CSS_SELECTOR, 'img.product-card__hero-image').get_attribute('src')
            # Link
            link = product.find_element(By.CSS_SELECTOR, 'a.product-card__link-overlay').get_attribute('href')
            
            #adding to db
            new_product = Product(name=name, price=float(price), color='-', image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", e)


    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump

#scraper for MACYS
def MACYS(search, sex):
    '''
        Scrapes macys.com using users prefernces  
    '''
    # Go to the webpage
    driver.get(f'https://www.macys.com/shop/featured/{search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for the page elements to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".productThumbnail"))
        )
        print("Loaded Macy's")
    except:
        print("failed to load Macys")
        fallback_brand_picker(search, sex)
        pass

    print("Loaded MACYS.")
    # Find all product items
    products = driver.find_elements(By.CSS_SELECTOR, '.productThumbnail')
    
    # Loop through each product and extract the details
    for product in products[:10]:  # Limit to first 10 products for brevity
        try:
            link = product.find_element(By.CSS_SELECTOR, 'a.productDescLink').get_attribute('href')
            name = product.find_element(By.CSS_SELECTOR, '.productDescription a').text
            name = re.sub(r'(?<!\\)"', r'\\"', name)
            price = product.find_element(By.CSS_SELECTOR, '.prices .regular').text.strip('$')
            price = re.sub(r',', '', price)
            image = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')

            new_product = Product(name=name, price=float(price), color='-', image=image, link=link)
            db.session.add(new_product)
            db.session.commit()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details:", e)

    # Serialize the list into JSON
    gptDump = json.dumps(all_products, indent=4)

    # Create a new list excluding the 'image' and 'link' keys
    products_list = json.loads(gptDump)

    # Create a new list excluding the 'image' and 'link' keys
    temp = [{key: value for key, value in product.items() if key not in ['image', 'link']} for product in products_list]

    # Convert to JSON if needed
    dataDump = json.dumps(temp)
    clean_string = re.sub(r'\\', '', dataDump)
    dataDump = re.sub(r'^\[|\]$', '', clean_string)
    return dataDump


#function when a website fails and call on another webpage as backup
brand_list = [HM, BR, F21, UNIQLO, ZARA, SHEIN, NIKE, MACYS]
# Main function that calls a random function from the list
def fallback_brand_picker(search, sex):
    chosen_function = random.choice(brand_list)
    chosen_function(search, sex)


#call on this to pass on to GPT for second step
def outfit_suggestions_scraper(outfit_json, sex):
    try:
        # Parse the input JSON
        outfit = json.loads(outfit_json)
        
        # Dictionary to hold the results
        comprehensive_results = {}
        
        # Mapping brand to its function call
        brand_function_map = {
            "H&M": HM,
            "Banana Republic": BR,
            "Forever 21": F21,
            "Uniqlo": UNIQLO,
            "Zara": ZARA,
            "Shein": SHEIN,
            "Nike": NIKE,
            "Macy's": MACYS
        }
        
        # Iterate over each item in the outfit
        for item, details in outfit.items():
            # Check if details is a JSON string and parse it
            if isinstance(details, str):
                try:
                    details = json.loads(details)
                except json.JSONDecodeError:
                    print(f"Skipping item {item}: details not in JSON format")
                    continue
            
            if details != "-" and isinstance(details, list):
                item_name, color, brand = details
                
                # Get the function based on the brand
                if brand in brand_function_map:
                    search_function = brand_function_map[brand]
                    
                    # Prepare the query with name and color
                    query = f"{sex} {item_name}"
                    
                    # Call the respective brand function and store the results
                    comprehensive_results[item] = search_function(query, sex)
                else:
                    print(f"Brand {brand} not recognized")
            else:
                print(f"Details for item {item} are incomplete or not a list")
        
        # Return the comprehensive JSON object containing all suggestions
        return comprehensive_results       
        driver.quit()

    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"