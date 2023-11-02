from flask import Flask, render_template

app = Flask(__name__)

# Define a list of fashion items (you can replace these with your own data)
fashion_items = [
    {
        'name': 'Stylish T-Shirt',
        'description': 'A comfortable and stylish t-shirt for any occasion.',
        'price': '$19.99',
        'image_url': 'https://example.com/tshirt.jpg',
    },
    {
        'name': 'Elegant Dress',
        'description': 'An elegant dress that is perfect for special events.',
        'price': '$49.99',
        'image_url': 'https://example.com/dress.jpg',
    },
    # Add more fashion items as needed
]

@app.route('/home')
def index():
    return render_template('index.html', fashion_items=fashion_items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)