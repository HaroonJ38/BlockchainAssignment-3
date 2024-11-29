from flask import Flask, request, jsonify, render_template_string, url_for
import hashlib

# Initialize the Flask application
app = Flask(__name__)

# Simulate a blockchain for supply management
supply_chain = []

# HTML Templates
MAIN_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Supply Chain Management</title>
</head>
<body>
    <h1>Supply Management Smart Contract</h1>
    <!-- Form to add a new item -->
    <form method="POST" action="/add">
        <label for="item">Item Name:</label>
        <input type="text" id="item" name="item" required>
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" name="quantity" required>
        <button type="submit">Add Item</button>
    </form>
    <h2>Supply Chain</h2>
    <ul>
        <!-- Loop through the supply_chain list and display each block's details -->
        {% for block in supply_chain %}
            <li>
                <strong>Index:</strong> {{ block['index'] }} <br>
                <strong>Item:</strong> {{ block['data']['item'] }} <br>
                <strong>Quantity:</strong> {{ block['data']['quantity'] }} <br>
                <strong>Hash:</strong> {{ block['hash'] }} <br>
                <strong>Previous Hash:</strong> {{ block['previous_hash'] }} <br>
            </li>
        {% endfor %}
    </ul>
    <!-- Link to view IDs and Hashes page -->
    <a href="/ids-and-hashes">View IDs and Hashes</a>
</body>
</html>
"""

ID_HASH_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Item IDs and Hashes</title>
</head>
<body>
    <h1>Item IDs and Hashes</h1>
    <ul>
        <!-- Loop through the supply_chain list and display each block's ID and Hash -->
        {% for block in supply_chain %}
            <li>
                <strong>ID:</strong> {{ block['index'] }} <br>
                <strong>Hash:</strong> {{ block['hash'] }}
            </li>
        {% endfor %}
    </ul>
    <!-- Button to navigate back to the main page -->
    <a href="{{ url_for('index') }}"><button>Back to Main Page</button></a>
</body>
</html>
"""

# Utility function to calculate the SHA-256 hash of a block
def calculate_hash(index, previous_hash, data):
    # Concatenate the index, previous hash, and data into a single string
    value = f"{index}{previous_hash}{data}".encode()
    # Return the SHA-256 hash of the concatenated string
    return hashlib.sha256(value).hexdigest()

# Utility function to create a new block in the supply chain
def create_block(item, quantity):
    # Determine the index of the new block
    index = len(supply_chain)
    # Get the hash of the previous block, or use a default value if it's the first block
    previous_hash = supply_chain[-1]['hash'] if supply_chain else '0' * 64
    # Create the data dictionary for the new block
    data = {'item': item, 'quantity': quantity}
    # Calculate the hash for the new block
    hash_value = calculate_hash(index, previous_hash, data)
    # Return the new block as a dictionary
    return {
        'index': index,
        'previous_hash': previous_hash,
        'data': data,
        'hash': hash_value
    }

# Route for the main page
@app.route('/')
def index():
    # Render the main page template with the current supply chain data
    return render_template_string(MAIN_PAGE_TEMPLATE, supply_chain=supply_chain)

# Route to add a new item to the supply chain
@app.route('/add', methods=['POST'])
def add_item():
    # Get the item name and quantity from the form data
    item = request.form.get('item')
    quantity = int(request.form.get('quantity'))
    # Create a new block with the provided item and quantity
    block = create_block(item, quantity)
    # Append the new block to the supply chain
    supply_chain.append(block)
    # Return a JSON response indicating success and include the new block's data
    return jsonify({'message': 'Item added to the supply chain', 'block': block})

# Route to display the IDs and hashes of all blocks
@app.route('/ids-and-hashes')
def ids_and_hashes():
    # Render the IDs and Hashes page template with the current supply chain data
    return render_template_string(ID_HASH_PAGE_TEMPLATE, supply_chain=supply_chain)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
