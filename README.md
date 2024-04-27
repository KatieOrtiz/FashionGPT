# FashionGPT

# Prerequisites:
- VS Code
- Python installed
- Pip installed

# Python Modules to Install (use VS Code Terminal):
    pip install selenium
    pip install flask_login
    pip install flask_cors
    pip install flask_sqlalchemy
    pip install jwt
    pip install python-env
    pip install python-dotenv

(please upgrade pip if there are errors installing anthropic)
    pip install anthropic

# Install the Following Extensions on VS Code:
Extension ID: cweijan.vscode-mysql-client2
Extension ID: cweijan.dbclient-jdbc

# Connect to the Database with the Following Steps:
On the left side toolbar, click "Database" icon
Click "Create Connection"
Select "SQLite" under "Server Type
Browse for Database Path (projectpath\instance\mydb.db)
Click "Save" 
Click "Connect"

# Comment out the following lines in app.py
lines 39, 42, 74, 76

# Create a file called .env on project root and add the following line:
API_KEY="" <- the value between the quotations should be the first API key from the email channel in our discord for claude anthropic AI

# URL for application: 127.0.0.1:5555

# To Run Application with AI/Web Scraper Script for Windows:

  1. Download the appropriate version of chromedriver.exe from Stable section here: https://googlechromelabs.github.io/chrome-for-testing/
  2. Comment out lines 15 - 23 in scraper.py and add the following code above the commented out code with paths replaced to your chromedriver.exe file:

    options = Options()
    # options.add_argument('--headless=new')
    options.add_argument("--incognito")

    # Set the path to your chromedriver.exe file
    chrome_driver_path = "C:\\path\\to\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)

    # Set the path to your Chrome executable
    chrome_binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    options.binary_location = chrome_binary_location

    # Pass the options when creating the driver instance
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.5)


# To Run Application with AI/Web Scraper Script for MacOS:


# repetitive scripts
docker build -t fashiongpt .
docker run -p 8000:8000 -v "$(pwd):/opt" fashiongpt
pip list 

# Documentation will be added here for the application

To connect to mysql db from docker container:
1. Log in via root (mysql -u root -p)
2. Run the command: 
    SHOW VARIABLES LIKE 'validate_password%';
3. Run the following commands to change password policy:
    SET GLOBAL validate_password.length = 0;
    SET GLOBAL validate_password.policy = LOW;
    SET GLOBAL validate_password.number_count = 0;
    SET GLOBAL validate_password.special_char_count = 0;

4. Create a user for docker container to connect with: 
    CREATE USER 'db_admin'@'%' IDENTIFIED BY 'dbpass';

5. Give privileges to newly created user:
    GRANT ALL PRIVILEGES ON *.* TO 'db_admin'@'%';

6. Run this command:
    FLUSH PRIVILEGES;

7. Make sure in the app.py you have the db connection settins:
    # db connection settings
    db_config = {
        'user': 'db_admin',
        'password': 'dbpass',
        'host': '130.166.160.21',
        'database': 'fashion_gpt',
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

8. I put the following config settings in the following files:
    port = 3306
    bind-address = 0.0.0.0

    in /etc/mysql/mysql.conf.d in both mysql.cnf and mysqld.cnf just in case