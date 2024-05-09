from scraper import outfit_suggestions_scraper
from flask import session
from dotenv import load_dotenv
from models import Suggestion, User
from extensions import db
import anthropic
import os, re, time, json, asyncio


load_dotenv()
suggestion_nextstep = ""
start_time = time.time()
query_id =0
global sex 
sex = "Male"

def GPT(system_prompt: str, msg: str): 
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key= os.environ.get("API_KEY"),
    )
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2048,
        temperature=0.6,
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


def one_getUserData(generated_id, gender, weight, waist, length, Skintone, height, hair, build, Budget, Colors, age, Style, Season, fabric, usersRequest):
    start_time = time.time()
    global sex
    sex = gender
    brands = "H&M, Banana Republic, Forever 21, Zara, Shien, Nike, and Macys."
    msg = '''
    <INSTRUCTIONS_TO_FOLLOW>
    </IMPORTANT>dont be too specific be less specific and more general, VERY GENERAL IN-FACT!</IMPORTANT>

    1. You don't have to fill all the values for each key, just the appropriate ones.

    2. It's RECOMMENDED that you give colors too, for when its appropriate.

    3. The hashtags are general values and uses may divert sometimes, so make decisions appropriately.

    4. ALWAYS return the optimum recommendation then the color then brand and finally price all in an array.

    6. for now the ONLY brands you can suggest are from the following brands: '''+ brands +'''

    7. Be VERY gender bias.
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
    <RESPONSE>
    {
    "top":[val,color,brand],
    "outerwear":[val,color,brand],
    "hat":[val,color,brand],
    "necklace": [val,color,brand],
    "earring":[val,color,brand],
    "Bottoms":[val,color,brand],
    "socks":[val,color,brand]
    "footwear":[val,color,brand],
    "bracelet":[val,color,brand],
    "watch":[val,color,brand],
    "belt":[val,color,brand],
    "avgTotalPrice":"",
    "reasoning":""
    }
    </RESPONSE>

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
    <RESPONSE>
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
    </RESPONSE>

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
    print("\033[32m✔\033[0m GOT USER DATA")
    global query_id
    query_id = generated_id
    # return message_content
    two_ask_GPT_Suggestion(totalMsg)

def two_ask_GPT_Suggestion(totalMsg):
    system = "You are an AI assistant known for your excellent fashion sense and ability to provide sleek, stylish, and appropriate outfit suggestions for any occasion. Your role is to suggest outfits that will turn heads and garner appreciation, while still being tasteful and not over-the-top."
    suggestion = GPT(system, totalMsg)
    # print(suggestion)
    global suggestion_nextstep 
    suggestion_nextstep = suggestion
    suggestion = json.loads(suggestion)

    # suggestion = {key.lower(): value for key, value in suggestion.items()}
    for key in suggestion:
        if suggestion[key] == "-":
            suggestion[key] = None

    # Logging to DB
    # email = session['email']
    # user = User.query.filter_by(email=email).first()
    # user_id = user.id
    # query = Suggestion(
    #     user_id=user_id,
    #     query_id=query_id,
    #     choose="general",
    #     top=json.dumps(suggestion["top"]),
    #     outerwear=json.dumps(suggestion["outerwear"]),
    #     hat=json.dumps(suggestion["hat"]),
    #     necklace=json.dumps(suggestion["necklace"]),
    #     earring=json.dumps(suggestion["earring"]),
    #     bottoms=json.dumps(suggestion["Bottoms"]),
    #     socks=json.dumps(suggestion["socks"]),
    #     footwear=json.dumps(suggestion["footwear"]),
    #     bracelet=json.dumps(suggestion["bracelet"]),
    #     watch=json.dumps(suggestion["watch"]),
    #     belt=json.dumps(suggestion["belt"]),
    #     avgTotalPrice=json.dumps(suggestion["avgTotalPrice"]),
    #     reasoning=json.dumps(suggestion["reasoning"])
    # )
    # db.session.add(query)
    # db.session.commit()

    # Assign each value from the dictionary to a variable
    print("\033[32m✔\033[0m GOT SUGGESTION")
    three_Scrape_Data(suggestion_nextstep)

async def scrape(suggestion, sex):
    scraped_data = outfit_suggestions_scraper(suggestion, sex)
    return scraped_data

def three_Scrape_Data(suggestion):
    Scraped_Data = asyncio.run(scrape(suggestion, sex))
    print("\033[32m✔\033[0m GOT SCRAPED DATA")
    
    four_Get_Best_Suggestion(Scraped_Data)

def four_Get_Best_Suggestion(Scraped_Data):
    system = "You are an AI assistant known for your excellent fashion sense and ability to provide sleek, stylish, and appropriate outfit suggestions for any occasion. Your role is to suggest outfits that will turn heads and garner appreciation, while still being tasteful and not over-the-top."
    msg = '''
    You will be acting as an AI fashion assistant to suggest 3 stylish outfit choices based on a previous suggestion and a list of options to choose from. 

    Here is the previous outfit suggestion, provided as a JSON object:
    <suggestion>
    '''+str(suggestion_nextstep)+'''
    </suggestion>

    And here is the list of options to choose from for each piece of the outfit, also in JSON format:
    <options_to_choose_from>
    '''+str(Scraped_Data)+'''
    </options_to_choose_from>

    Your task is to generate 3 new outfit choices, using the previous suggestion as a starting point but selecting items from the options provided. 

    For each of the 3 outfit choices:
    - Select items for each part of the outfit that match the style and color scheme of the original suggestion. If an item category is marked with a "-" in the original suggestion, you can skip it for the new outfits as well.
    - Make sure to choose items that are in the specified price range from the original suggestion.
    - Select items that are appropriate for the gender specified in the original suggestion.

    After you have selected all the items for an outfit, calculate the total price by adding up the individual item prices. 

    Then, take a moment to reflect on the completed outfit in your <reflection> inner monologue. Consider how well the pieces go together, whether the outfit suits the original style request, and how satisfied you think the client would be with it. </reflection>

    Emerge from your reflection and assign the outfit a rating score out of 10. Write out the reasoning for your score in a <reasoning> tag.

    Repeat this process for all 3 outfit choices.

    When you are done, return the 3 completed outfits in JSON format like this:

    <result>
    {"choice1":{
    "top": ["name","color","price"],
    "outerwear": ["name","color","price"],
    "hat": ["name","color","price"],
    "necklace": ["name","color","price"], 
    "earring": ["name","color","price"],
    "Bottoms": ["name","color","price"],
    "socks": ["name","color","price"],
    "footwear": ["name","color","price"],
    "bracelet": ["name","color","price"],
    "watch": ["name","color","price"],
    "belt": ["name","color","price"],
    "TotalPrice": "total_price",
    "rating": "rating_score",
    "reasoning": "reasoning_text"
    },
    "choice2":{
    ...
    },
    "choice3":{
    ...  
    }}
    </result>

    Some important notes:
    - Stick strictly to the price range from the original suggestion.
    - Make sure your outfit choices are appropriate for the specified gender.
    - Use the exact names for items as they appear in the options_to_choose_from object. Do not make up your own names.
    - Skip any item categories that have a "-" in the original suggestion.
    - Always provide exactly 3 choices, no more and no less.
    - Make sure it is for '''+ sex +'''

    Remember, your role is to be a fashionable and thoughtful stylist. Take time to consider each outfit carefully to ensure it will delight the client. Good luck!
    '''
    # totalMsg = msg+"\n suggestion = "+str(suggestion_nextstep)+"\n options_to_choose_from = "+str(Scraped_Data)
    totalMsg = msg
    print(totalMsg)
    Final_suggestions = GPT(system, totalMsg)
    if re.findall(r'"\s*}$', Final_suggestions):
        Final_suggestions = Final_suggestions + "}"
    if re.findall(r'"\s*$', Final_suggestions):
        Final_suggestions = Final_suggestions + "}}"

    email = session['email']
    user = User.query.filter_by(email=email).first()
    user_id = user.id

    try:
        # Assume Final_suggestions is your JSON string
        Final_suggestions = json.loads(Final_suggestions)
        print(Final_suggestions)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:")
        print(Final_suggestions)  # Log the problematic JSON string
        raise

    for key, suggestion in Final_suggestions.items():
        # Replacing "-" with None for a more Pythonic representation
        for item_key, item_value in suggestion.items():
            if isinstance(item_value, list):  # Checking if the value is a list
                suggestion[item_key] = [None if v == "-" else v for v in item_value]
            else:
                suggestion[item_key] = None if item_value == "-" else item_value
        

        # Preparing and adding each suggestion to the database
        suggestion_record = Suggestion(
            user_id=user_id,
            query_id=query_id,
            choose="choice"+key,  # Using key from the dictionary to specify the choice
            top=json.dumps(suggestion.get("top", None)),
            outerwear=json.dumps(suggestion.get("outerwear", None)),
            hat=json.dumps(suggestion.get("hat", None)),
            necklace=json.dumps(suggestion.get("necklace", None)),
            earring=json.dumps(suggestion.get("earring", None)),
            bottoms=json.dumps(suggestion.get("Bottoms", None)),
            socks=json.dumps(suggestion.get("socks", None)),
            footwear=json.dumps(suggestion.get("footwear", None)),
            bracelet=json.dumps(suggestion.get("bracelet", None)),
            watch=json.dumps(suggestion.get("watch", None)),
            belt=json.dumps(suggestion.get("belt", None)),
            avgTotalPrice=json.dumps(suggestion.get("TotalPrice", None)),
            reasoning=json.dumps(suggestion.get("reasoning", None))
        )
        db.session.add(suggestion_record)

    db.session.commit()

    end_time = time.time()
    duration = end_time - start_time
    print("\033[32m✔\033[0m Final Suggestions")
    print(f"-- {duration:.2f} (sec)--")
