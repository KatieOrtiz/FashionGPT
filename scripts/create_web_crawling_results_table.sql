CREATE TABLE Web_Crawling_Results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    request_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    item_url VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    price DECIMAL(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (request_id) REFERENCES API_Requests(request_id)
);