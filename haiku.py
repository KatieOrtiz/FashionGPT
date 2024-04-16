from dotenv import load_dotenv
import anthropic
import os, re, time
from scraper import outfit_suggestions_scraper


load_dotenv()
suggestion = ""
start_time = time.time()

def GPT(system_prompt: str, msg: str): 
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key= os.environ.get("API_KEY"),
    )
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": msg
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "{"
                    }
                ]
            }
        ]
    )
    return "{" + response.content[0].text


def one_getUserData(gender, weight, waist, length, Skintone, height, hair, build, Budget, Colors, age, Style, Season, fabric, usersRequest):
    start_time = time.time()
    msg = '''
    <INSTRUCTIONS_TO_FOLLOW>

    1. You don't have to fill all the values for each key, just the appropriate ones.

    2. It's RECOMMENDED that you give colors too, for when its appropriate.

    3. The hashtags are general values and uses may divert sometimes from using them so make destines appropriately

    4. ALWAYS return the optimum recommendation then the color then brand and finally price all in an array.

    6. for now the only brands you can suggest are as follows H&M, Banana Republic, Forever 21, Uniqlo, and Zara

    7. dont be too specific be less specific and more general.

    </INSTRUCTIONS_TO_FOLLOW>

    <BLUEPRINT>
    <INPUT>
    {
    "gender":"", #M is male; F is female
    "weight":"", #wight of person in pounds
    "waist":"", #waist size in inches
    "length":"", #length for pants size
    "Skintone": "", #skin tone for bet fitting colors
    "height":"", #height in centimeters
    "hair":"", #blond, brunet, ginger, or colors
    "build":"", #how the person looks (underweight, fit, overweight, obese)
    "Budget":"", #price range $50-150
    "Colors":"", #color preferences
    "age":"", #persons age
    "Style":"", #stockholm, old money,...
    "Season":"", #spring, fall, winter, autumn
    "fabric":"", #fabric preferences like cotton,...
    "usersRequest":"" #a customs input by the user detailing more.
    }
    </INPUT>
    <RESPONCE>
    {
    "top":[val,color,brand},
    "outerwear":[val,color,brand},
    "hat":[val,color,brand},
    "necklace": [val,color,brand},
    "earring":[val,color,brand},
    "Bottoms":[val,color,brand},
    "socks":[val,color,brand}
    "footwear":[val,color,brand},
    "bracelet":[val,color,brand},
    "watch":[val,color,brand},
    "belt":[val,color,brand},
    "avgTotalPrice":"",
    "reasoning":""
    }
    </RESPONCE>

    </BLUEPRINT>

    <*** below is an example ***>

    <EXAMPLE>
    <INPUT>
    {
    "gender":"M",
    "weight":"185",
    "weist":"32",
    "length":"32",
    "Skintone": "light brown",
    "height":"184",
    "hair":"brunet",
    "build":"Fit",
    "Budget":"10:400",
    "Colors":"-",
    "age":"29",
    "Style":"old money",
    "Season":"spring",
    "fabric":"-",
    "usersRequest":"lunch outing with friends, at a high scale restaurant"
    }
    </INPUT>
    <RESPONCE>
    {
    "top":[G200 Gildan Adult Ultra Cotton T-Shirt", "white", "Gildan"],
    "outerwear":["quarter zip sweater","black","abercrombie"],
    "hat":"-",
    "necklace": "-",
    "earring":"-",
    "Bottoms":["THLETIC LINEN-COTTON EWAIST PANT","black", "Banana republic"],
    "socks":["White socks", "white", "hanes"],
    "footwear":["Mens Wally Linen", "white", "Hey Dude"],
    "bracelet":"-",
    "watch":"-",
    "belt":"-",
    "avgTotalPrice":"150:170",
    "reasoning":"The old money dress code emphasizes timeless, high-quality pieces that suggest understated elegance and comfort. This look, featuring a classic T-shirt, a quarter-zip sweater, linen-cotton pants, casual shoes, and white socks, conveys a relaxed yet refined aesthetic."
    }
    </RESPONCE>

    </EXAMPLE>
    
    '''
    user_preferences = f'''
    now knowing all things and also knowing your role and task, return the most optimum outfit for the following:
    {{
    "gender": "{gender}",
    "weight": "{weight}",
    "waist": "{waist}",
    "length": "{length}",
    "Skintone": "{Skintone}",
    "height": "{height}",
    "hair": "{hair}",
    "build": "{build}",
    "Budget": "{Budget}",
    "Colors": "{Colors}",
    "age": "{age}",
    "Style": "{Style}",
    "Season": "{Season}",
    "fabric": "{fabric}",
    "usersRequest": "{usersRequest}"
    }}
    '''
    totalMsg = msg+user_preferences
    print(totalMsg)
    print("--------------------------")
    print("---GOT USER DATA----------")
    print("--------------------------")
    # return message_content
    two_ask_GPT_Suggestion(totalMsg)

def two_ask_GPT_Suggestion(totalMsg):
    system = "you are a fashion designer, your role as a fashion designer is to give good suggestions on which outfits go with what; you have been known give amazing suggestions and have always been known for giving appropriate and not over the top suggestion, sleek and stylish designs which make people stare and appreciate. You are also known for getting right to the point and output your response only in JSON format and in a very strict order and way (explained more about how you respond in the examples below)."
    suggestion = GPT(system, totalMsg)
    print(suggestion)
    print("--------------------------")
    print("---GOT SUGGESTION---------")
    print("--------------------------")
    three_Scrape_Data(suggestion)

def three_Scrape_Data(suggestion):
    Scraped_Data = outfit_suggestions_scraper(suggestion)
    print(Scraped_Data)
    print("--------------------------")
    print("---GOT SCRAPED DATA-------")
    print("--------------------------")
    
    four_Get_Best_Suggestion(Scraped_Data)

def four_Get_Best_Suggestion(Scraped_Data):
    system = "you are a fashion designer, your role as a fashion designer is to give good suggestions on which outfits go with what; you have been known give amazing suggestions and have always been known for giving appropriate and not over the top suggestion, sleek and stylish designs which make people stare and appreciate. You are also known for getting right to the point and output your response only in JSON format and in a very strict order and way (explained more about how you respond in the examples below)."
    msg = '''

    <INSTRUCTIONS_TO_FOLLOW>

    1. You had provided a suggestion eailier which we WILL call suggestions, depending on that make decitions.

    2. you WILL be given a json like list in which you WILL choose the best fitting option and return it as an JSON object back.

    3. you also WILL calculate the total cost for the outfit.

    4. you WILL give a rating out of 10 of how sattifited you are with the outfit and why, this hgoes under "reasoning", you are allowed to be as desciptive as you want.
    
    5. you WILL give 3 choices and strickly stick to 3

    6. strickly stick to the price range
    </INSTRUCTIONS_TO_FOLLOW>

    <BLUEPRINT>
    <INPUT>
    suggestion = {
    "top": ["NAME", "COLOR", "BRAND"],
    "outerwear": ["NAME", "COLOR", "BRAND"],
    "hat": ["NAME", "COLOR", "BRAND"],
    "necklace": ["NAME", "COLOR", "BRAND"],
    "earring": ["NAME", "COLOR", "BRAND"],
    "Bottoms": ["NAME", "COLOR", "BRAND"],
    "socks": ["NAME", "COLOR", "BRAND"],
    "footwear": ["NAME", "COLOR", "BRAND"],
    "bracelet": ["NAME", "COLOR", "BRAND"],
    "watch": ["NAME", "COLOR", "BRAND"],
    "belt": ["NAME", "COLOR", "BRAND"],
    "TotalPrice": "price",
    "reasoning": "reason..."
    }
    options_to_choose_from = {'top': '{"name": "...", "price": "...", "colors": [...]}, 
                            {"name": "...", "price": "...", "colors": [...]}...',...}
    </INPUT>
    <RESPONCE>
    {"choice1":{
    "top": [name,color,price],
    "outerwear":[name,color,price],
    "hat":[name,color,price],
    "necklace": [name,color,price],
    "earring":[name,color,price],
    "Bottoms":[name,color,price],
    "socks":namel,colorprice]}
    "footwear":[name,color,price],
    "bracelet":[name,color,price],
    "watch":[name,color,price],
    "belt":[name,color,price],
    "TotalPrice":"total_cost",
    "reasoning":"..."
    },{"choice2":{
    "top": [name,color,price],
    "outerwear":[name,color,price],
    "hat":[name,color,price],
    "necklace": [name,color,price],
    "earring":[name,color,price],
    "Bottoms":[name,color,price],
    "socks":namel,colorprice]}
    "footwear":[name,color,price],
    "bracelet":[name,color,price],
    "watch":[name,color,price],
    "belt":[name,color,price],
    "TotalPrice":"total_cost",
    "reasoning":"..."
    }, {"choice2":{
    "top": [name,color,price],
    "outerwear":[name,color,price],
    "hat":[name,color,price],
    "necklace": [name,color,price],
    "earring":[name,color,price],
    "Bottoms":[name,color,price],
    "socks":namel,colorprice]}
    "footwear":[name,color,price],
    "bracelet":[name,color,price],
    "watch":[name,color,price],
    "belt":[name,color,price],
    "TotalPrice":"total_cost",
    "reasoning":"..."
    }}
    </RESPONCE>

    </BLUEPRINT>

    <*** below is an example ***>

    <EXAMPLE>
    <INPUT>
    suggestion = {
    "top": ["Slim Fit Crew Neck T-Shirt", "white", "H&M"],
    "outerwear": ["Lightweight Denim Jacket", "light blue", "Zara"],
    "hat": ["Baseball Cap", "red", "Forever 21"],
    "necklace": "-",
    "earring": "-",
    "Bottoms": ["Slim Fit Chino Shorts", "khaki", "Uniqlo"],
    "socks": ["Ankle Socks", "white", "H&M"],
    "footwear": ["Canvas Sneakers", "white", "Converse"],
    "bracelet": "-",
    "watch": "-",
    "belt": ["Casual Canvas Belt", "brown", "Banana Republic"],
    "TotalPrice": "100-150",
    "reasoning": "For a casual spring look for a shorter, slimmer build with light skin and red hair, this outfit featuring a slim fit t-shirt, lightweight denim jacket, chino shorts, canvas sneakers, and a casual canvas belt provides a comfortable yet stylish look. The cotton fabrics and spring-appropriate colors work well for the season."
    }
    options_to_choose_from = {'top': '{"name": "Printed T-shirt", "price": "$ 9.99", "colors": ["White/Fender", "Black/Spiritualized", "White/Nirvana", "Dark gray"]}, {"name": "Printed T-shirt", "price": "$ 9.99", "colors": ["White/Nirvana", "White/Fender", "Black/Spiritualized", "Dark gray"]}', 'outerwear': '', 'hat': '{"name": "Curved-Brim Baseball Cap", "price": "$6.99", ...}'}
    </INPUT>
    <RESPONCE>
    {"choice1":{
    "top": ["Printed T-shirt","Black/Spiritualized","$ 9.99"],
    "hat":["Embroidered Rose Baseball Cap","WHITE/RED","$ 8.00"],
    ..., "TotalPrice": "$ 189",...
    },{"choice2":{...
    </RESPONCE>

    </EXAMPLE>
    
    '''
    totalMsg = msg+"\n suggestion = "+str(suggestion)+"\n options_to_choose_from = "+str(Scraped_Data)
    print(totalMsg)
    Final_suggestions = GPT(system, totalMsg)
    print(Final_suggestions)
    print("--------------------------")
    print("---Final Suggestions------")
    print("--------------------------")
    end_time = time.time()
    duration = end_time - start_time
    print("The program took", duration, "to run")