from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import json
import re

options = Options()
# options.add_argument('--headless=new')
options.add_argument("--incognito")
service = Service(executable_path="/Users/charitha/Documents/GitHub/FashionGPT/chromedriver")
options.binary_location = '/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'

# Pass the options when creating the driver instance
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(0.5)

#scraper for H&M
def HM(search):
    # Go to the webpage
    driver.get(f'https://www2.hm.com/en_us/search-results.html?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    #Page load timeout
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-item"))
        )
    except:
        pass

    # Find all product items
    products = driver.find_elements(By.CLASS_NAME, 'product-item')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CLASS_NAME, 'item-heading').text
            # Price
            price = product.find_element(By.CLASS_NAME, 'item-price').text
            # Color(s): Find the ul with class 'list-swatches' and then find all li with class 'item' within
            swatches_ul = product.find_elements(By.CLASS_NAME, 'list-swatches')
            color_elements = [li.find_element(By.TAG_NAME, 'a') for ul in swatches_ul for li in ul.find_elements(By.CLASS_NAME, 'item')]
            colors = [elem.get_attribute('title') for elem in color_elements if elem.get_attribute('title')]

            # Image
            image_element = product.find_element(By.CLASS_NAME, 'item-image')
            image = image_element.get_attribute("src")

            # Link
            link_element = product.find_element(By.CLASS_NAME, 'item-link')
            link = link_element.get_attribute("href")

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

    # Clean up (close the browser)
    # driver.quit()
    # Output the JSON data
    # print(gptDump)
    return dataDump

#scraper for Banana Republic
def BR(search):
    # Go to the webpage
    driver.get(f'https://bananarepublicfactory.gapfactory.com/browse/search.do?searchText={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Ensure that the product cards are loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card'))
        )
    except:
        pass

    # Find all product cards
    products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')

    # Loop through each product and extract details
    for product in products[:10]:  # Limit to first 10 for simplicity
        try:
            # Using data-testid for more stable selection if available
            name = product.find_element(By.CSS_SELECTOR, '[data-testid="product-info-wrapper"] div').text

            # Price extraction with alternative strategies if structure changes
            try:
                price_element = product.find_element(By.CSS_SELECTOR, '.product-price__highlight--br, .product-price--line-item')
                price = price_element.text
                price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
                price = re.sub(r"\$\d+\.\d+ - ", "", price)
                price = re.sub("Now ", "", price)
            except NoSuchElementException:
                price = "Price not found"

            # Image extraction using alt attribute
            try:
                image_element = product.find_element(By.CSS_SELECTOR, 'img')
                image = image_element.get_attribute("src")
            except NoSuchElementException:
                image = "Image not available"

            # Link extraction, here assuming 'a' tag inside product card links to product
            try:
                link_element = product.find_element(By.CSS_SELECTOR, 'a')
                link = link_element.get_attribute("href")
            except NoSuchElementException:
                link = "Link not available"

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print(f"An error occurred: {e}")


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

    # Clean up (close the browser)
    # driver.quit()
    # Output the JSON data
    # print(gptDump)
    return dataDump

#scraper for Forever 21
def F21(search):
    # Go to the webpage
    driver.get(f'https://www.forever21.com/us/search?q={search}&lang=en_US')

    # Initialize an empty list to hold all product details
    all_products = []

    # Find all product items
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-grid__item"))
        )
    except:
        pass

    products = driver.find_elements(By.CLASS_NAME, 'product-grid__item')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CLASS_NAME, 'product-tile__name').text
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

    # Clean up (close the browser)
    # driver.quit()
    # Output the JSON data
    # print(gptDump)
    return dataDump

#scraper for UNIQLO
def uniqlo(search):
    # Go to the webpage
    driver.get(f'https://www.uniqlo.com/us/en/search?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Find all product items
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fr-ec-product-tile-resize-wrapper"))
        )
    except:
        pass

    products = driver.find_elements(By.CLASS_NAME, 'fr-ec-product-tile-resize-wrapper')

    # Loop through each product and extract the details
    for product in products[:10]:
        try:
            # Product name
            name = product.find_element(By.CLASS_NAME, 'fr-ec-title').text
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

    # Clean up (close the browser)
    # driver.quit()
    # Output the JSON data
    # print(gptDump)
    return dataDump

#scraper for ZARA
def zara(search):
    sex = "M"
    if sex == "M":
        gender = "MAN"
    else:
        gender = "WOMAN"

    # Go to the webpage
    driver.get(f'https://www.zara.com/us/en/search?searchTerm={search}&section={gender}')

    # Wait for the products to be loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li._product"))
        )
    except:
        pass
    
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
            
            # Price
            try:
                price_element = product.find_element(By.CSS_SELECTOR, '.price__amount-wrapper .price__amount .money-amount__main')
                price = price_element.text
            except NoSuchElementException:
                price = "Price not found"
            
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

    # Clean up (close the browser)
    # driver.quit()
    # Output the JSON data
    # print(gptDump)
    return dataDump

# gptDump, dataDump = zara("black tshirt", "M")
# print(gptDump)
# print(dataDump)

#call on this to pass on to GPT for second step
def outfit_suggestions_scraper(outfit_json):
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
            "Uniqlo": uniqlo,
            "Zara": zara
            # "Zara": lambda item, color: zara(item, color, "unisex")  # Assuming a default sex as 'unisex'
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
                    query = f"{item_name} {color}"
                    
                    # Call the respective brand function and store the results
                    comprehensive_results[item] = search_function(query)
                else:
                    print(f"Brand {brand} not recognized")
            else:
                print(f"Details for item {item} are incomplete or not a list")
        
        # Return the comprehensive JSON object containing all suggestions
        driver.quit()
        return comprehensive_results

    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"


