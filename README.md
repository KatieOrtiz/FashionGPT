# FashionGPT
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