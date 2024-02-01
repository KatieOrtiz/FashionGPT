# Use an official Python runtime as a parent image
# If developing locally, keey mysql installation and execution of sql scripts uncommented
FROM python:3.9-slim

# Install Flask and Jinja2 (if not already installed)
RUN pip install Flask Jinja2 mysql-connector-python

# Install Nginx and MariaDB client
RUN apt-get update && apt-get install -y nginx nano && rm -rf /var/lib/apt/lists/*

# Copy files to root of container
COPY app.py /opt/app.py
COPY templates /opt/templates/
COPY static /opt/static/

# # # Install MySQL server
# ENV MYSQL_ROOT_PASSWORD=rootdev
# ENV MYSQL_DATABASE=fashion_gpt
# ENV MYSQL_USER=test
# ENV MYSQL_PASSWORD=testdev

# RUN apt-get update && apt-get install -y mariadb-server && rm -rf /var/lib/apt/lists/*

# Copy SQL files to container
COPY scripts /opt/scripts/


# # Execute SQL files
# RUN /etc/init.d/mysql start && \
#     mysql -u $root -p$rootdev -e "USE $fashion_gpt; SOURCE /opt/scripts/create_users_table.sql;" && \
#     mysql -u $root -p$rootdev -e "USE $fashion_gpt; SOURCE /opt/scripts/create_measurements_table.sql;" && \
#     mysql -u $root -p$rootdev -e "USE $fashion_gpt; SOURCE /opt/scripts/create_api_requests_table.sql;" && \
#     mysql -u $root -p$rootdev -e "USE $fashion_gpt; SOURCE /opt/scripts/create_web_crawling_results_table.sql;" && \
#     /etc/init.d/mysql stop

# Expose the necessary port(s)
EXPOSE 8000
EXPOSE 8080
EXPOSE 3306

WORKDIR /opt/
# Start Nginx and your Flask application (replace 'app.py' with your Python file)
CMD service nginx start && python /opt/app.py

# # Start Nginx, MariaDB server, and your Flask application
# CMD service nginx start && mysqld_safe --skip-syslog --skip-networking --hostname=fashiongpt& python /opt/app.py