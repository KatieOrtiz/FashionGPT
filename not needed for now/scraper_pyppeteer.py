import asyncio, json, re
from pyppeteer import launch

async def HM(search):
    '''
        Asynchronously scrapes hm.com using user preferences.
    '''
    browser = await launch({
        'headless': True,  # Ensures Chromium runs in headless mode
        'args': [
            '--no-sandbox',  # Disables the sandbox for the browser process
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',  # Overcomes limited resource problems
            '--disable-accelerated-2d-canvas',  # Disable hardware acceleration
            '--no-first-run',
            '--no-zygote',  # Manage Zygote process for Chrome
            '--single-process',  # Runs the browser in a single process
            '--disable-gpu'  # Disables GPU hardware acceleration
        ]
    })
    # Launch a browser
    page = await browser.newPage()

    # Go to the webpage
    await page.goto(f'https://www2.hm.com/en_us/search-results.html?q={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    try:
        # Wait for the product items to load on the page
        await page.waitForSelector('.product-item', {'timeout': 15000})
    except Exception as e:
        print("Failed to load H&M products:", str(e))
        await browser.close()
        return

    # Extract product details
    products = await page.querySelectorAll('.product-item')

    for product in products[:10]:
        try:
            # Product name
            name = await product.querySelectorEval('.item-heading', 'node => node.textContent')
            # Price
            price = await product.querySelectorEval('.item-price', 'node => node.textContent')
            price2 = price[1::]

            # Colors
            swatches_ul = await product.querySelectorAll('.list-swatches')
            colors = []
            for ul in swatches_ul:
                color_elements = await ul.querySelectorAll('.item')
                for elem in color_elements:
                    title = await (await elem.getProperty('title')).jsonValue()
                    if title:
                        colors.append(title)

            # Image
            image_element = await product.querySelector('.item-image')
            image = await (await image_element.getProperty("src")).jsonValue()

            # Link
            link_element = await product.querySelector('.item-link')
            link = await (await link_element.getProperty("href")).jsonValue()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details", str(e))

    # Clean up
    await browser.close()

    # Serialize the list into JSON
    return json.dumps(all_products, indent=4)


async def BR(search):
    '''
        Asynchronously scrapes Banana Republic Factory website using user preferences.
    '''
    browser = await launch({
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    })
    page = await browser.newPage()

    # Go to the webpage
    await page.goto(f'https://bananarepublicfactory.gapfactory.com/browse/search.do?searchText={search}')

    # Initialize an empty list to hold all product details
    all_products = []

    # Ensure that the product cards are loaded
    try:
        await page.waitForSelector('div.product-card', {'timeout': 10000})
    except Exception as e:
        print("Failed to load Banana Republic products:", str(e))
        await browser.close()
        return

    # Find all product cards
    products = await page.querySelectorAll('div.product-card')

    for product in products[:10]:  # Limit to first 10 for simplicity
        try:
            # Product name extraction
            name = await product.querySelectorEval('[data-testid="product-info-wrapper"] div', 'e => e.textContent')

            # Price extraction
            try:
                price = await product.querySelectorEval('.product-price__highlight--br, .product-price--line-item', 'e => e.textContent')
                price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
                price = re.sub(r"\$\d+\.\d+ - ", "", price)
                price = re.sub("Now ", "", price)
            except Exception:
                price = "Price not found"

            # Image extraction
            try:
                image_element = await product.querySelector('img')
                image = await (await image_element.getProperty('src')).jsonValue()
            except Exception:
                image = "Image not available"

            # Link extraction
            try:
                link_element = await product.querySelector('a')
                link = await (await link_element.getProperty('href')).jsonValue()
            except Exception:
                link = "Link not available"

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print(f"An error occurred while extracting product details: {str(e)}")

    # Clean up
    await browser.close()

    # Serialize the list into JSON
    return json.dumps(all_products, indent=4)


async def F21(search):
    '''
        Asynchronously scrapes Forever 21 website using user preferences.
    '''
    browser = await launch({
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    })
    page = await browser.newPage()

    # Go to the webpage
    await page.goto(f'https://www.forever21.com/us/search?q={search}&lang=en_US')

    # Initialize an empty list to hold all product details
    all_products = []

    # Wait for product items to be loaded
    try:
        await page.waitForSelector(".product-grid__item", {'timeout': 10000})
    except Exception as e:
        print("Failed to load Forever 21 products:", str(e))
        await browser.close()
        return

    # Find all product items
    products = await page.querySelectorAll('.product-grid__item')

    # Loop through each product and extract details
    for product in products[:10]:
        try:
            # Product name
            name = await (await product.querySelector('.product-tile__body-section.product-tile__name')).evaluate('node => node.textContent')

            # Price extraction
            price = "Price not found"
            price_elements = await product.querySelectorAll('.value.price__default.font-weight--bold')
            if price_elements:
                price = await (await price_elements[0].getProperty('textContent')).jsonValue()
                price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
                price = re.sub(r"\$\d+\.\d+ - ", "", price)
                price = re.sub("Now ", "", price)

            # Colors extraction
            color_elements = await product.querySelectorAll('.product-tile__swatches a')
            colors = []
            for color_element in color_elements:
                color_title = await (await color_element.getProperty('title')).jsonValue()
                if color_title:
                    colors.append(color_title)

            # Image extraction
            image_elements = await product.querySelectorAll('.product-tile__image img')
            images = [await (await img.getProperty('src')).jsonValue() for img in image_elements]
            image = images[0] if images else "Image not available"

            # Link extraction
            link_element = await product.querySelector('a.product-tile__anchor')
            link = await (await link_element.getProperty('href')).jsonValue()

            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print(f"An error occurred while extracting product details: {str(e)}")

    # Clean up
    await browser.close()

    # Serialize the list into JSON
    return json.dumps(all_products, indent=4)

async def uniqlo(search):
    browser = await launch({
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    })
    page = await browser.newPage()

    await page.goto(f'https://www.uniqlo.com/us/en/search?q={search}')

    all_products = []

    try:
        await page.waitForSelector(".fr-ec-product-tile-resize-wrapper", {'timeout': 10000})
    except Exception as e:
        print("Failed to load UNIQLO:", str(e))
        await browser.close()
        return

    products = await page.querySelectorAll('.fr-ec-product-tile-resize-wrapper')

    for product in products[:10]:
        try:
            name = await product.querySelectorEval('.fr-ec-title', '(el) => el.textContent')
            price = await product.querySelectorEval('.fr-ec-price-text', '(el) => el.textContent')
            price = re.sub(r"Now \$\d+\.\d+ - ", "", price)
            price = re.sub(r"\$\d+\.\d+ - ", "", price)
            price = re.sub("Now ", "", price)

            colors = []
            color_elements = await product.querySelectorAll('.fr-ec-chip__default-image')
            for color_element in color_elements:
                image_url = await (await color_element.getProperty('src')).jsonValue()
                color_code_match = re.search(r"goods_(\d+)_", image_url)
                if color_code_match:
                    color_code = int(color_code_match.group(1))
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

            image = await product.querySelectorEval('.fr-ec-image__img', '(el) => el.src')
            link = await product.querySelectorEval('.fr-ec-tile', '(el) => el.href')

            all_products.append({
                'name': name,
                'price': price,
                'colors': colors,
                'image': image,
                'link': link
            })

        except Exception as e:
            print(f"Error extracting product details: {str(e)}")

    await browser.close()

    return json.dumps(all_products, indent=4)


async def zara(search: str) -> str:
    '''
        An asynchronous function that scrapes data from the Zara website including product name, color, price, image, and URL.
    '''
    sex = "M"
    gender = "MAN" if sex == "M" else "WOMAN"

    browser = await launch({
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    })
    page = await browser.newPage()

    await page.goto(f'https://www.zara.com/us/en/search?searchTerm={search}&section={gender}')

    all_products = []

    try:
        await page.waitForSelector("li._product", {'timeout': 10000})
    except Exception as e:
        print("Failed to load ZARA:", str(e))
        await browser.close()
        return json.dumps([])

    products = await page.querySelectorAll("li._product")

    for product in products[:10]:  # Limiting to first 10 products for brevity
        try:
            name = await product.querySelectorEval('h2', 'el => el.textContent || "Name not found"')
            price = await product.querySelectorEval('.price__amount-wrapper .price__amount .money-amount__main', 'el => el.textContent', default="Price not found")
            image = await product.querySelectorEval('img.media-image__image', 'el => el.src', default="Image not found")
            link = await product.querySelectorEval('a.product-link.product-grid-product__link', 'el => el.href', default="Link not found")

            # Assuming db.session and Product setup is not necessary for the script adaptation here
            # Append product details to all_products list
            all_products.append({
                'name': name,
                'price': price,
                'image': image,
                'link': link
            })

        except Exception as e:
            print("Error extracting product details:", str(e))

    await browser.close()

    # Serialize the list into JSON and return
    return json.dumps(all_products, indent=4)



async def outfit_suggestions_scraper(outfit_json):
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
        }
        
        tasks = []
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
                    
                    # Schedule the respective brand function to run asynchronously
                    task = asyncio.create_task(search_function(query))
                    tasks.append((item, task))
                else:
                    print(f"Brand {brand} not recognized")
            else:
                print(f"Details for item {item} are incomplete or not a list")

        # Wait for all asynchronous tasks to complete
        results = await asyncio.gather(*[task for _, task in tasks])
        
        # Combine results back to the item names
        for (item, _), result in zip(tasks, results):
            comprehensive_results[item] = result

        return comprehensive_results

    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"
