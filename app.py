from flask import Flask, request, render_template, jsonify, redirect, session, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to 'login' view if not authenticated

# Flask-Login will need a User class with certain properties
login_manager.login_message = 'Please log in to access this page.'

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries for easier use
    return conn

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, first_name, last_name, street_address, city, state, zip_code):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

# Load user function to retrieve a user from the database
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, first_name, last_name, shipping_street_address, shipping_city, shipping_state, shipping_zip FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(id=user_data[0], username=user_data[1], first_name=user_data[2], last_name=user_data[3], street_address=user_data[4], city=user_data[5], state=user_data[6], zip_code=user_data[7])
    return None

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, first_name, last_name, shipping_street_address, shipping_city, shipping_state, shipping_zip, theme, text_size FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            user_obj = User(id=user[0], username=user[1], first_name=user[3], last_name=user[4],
                            street_address=user[5], city=user[6], state=user[7], zip_code=user[8])
            login_user(user_obj)  # Log in the user

            # Apply user preferences            
            session['theme'] = user[9]
            session['text_size'] = user[10]
            return redirect(url_for('browse'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Route for Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Add logic for resetting password here
        return redirect(url_for('login'))
    return "This is a prototype, you really expected password reset functionality?"

# Route for Sign-Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        data = request.get_json()  # Assuming JSON format from AJAX

        # Extract user info
        username = data['username']
        email = data['email']
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        first_name = data['firstName']
        last_name = data['lastName']
        street_address = data['streetAddress']
        city = data['city']
        state = data['state']
        zip_code = data['zipCode']

        try:
            # Create a database connection
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Insert new user details into the Users table
            cursor.execute('''
                INSERT INTO Users (username, email, password, first_name, last_name,
                                  shipping_street_address, shipping_city, shipping_state, shipping_zip)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, first_name, last_name, street_address, city, state, zip_code))

            # Commit the transaction and close the connection
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()

            # Log the user in by adding user info to the session
            user_obj = User(id=user_id, username=username, first_name=first_name, last_name=last_name,
                            street_address=street_address, city=city, state=state, zip_code=zip_code)
            login_user(user_obj)

            # Redirect to /browse after successful signup
            return jsonify({'success': True, 'redirect': url_for('browse')})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    # Handle GET request
    return render_template('signup.html')

# Flask Route for Browse Page
@app.route('/browse')
@login_required
def browse():
    conn = get_db_connection()
    products = conn.execute(
        '''
        SELECT id, name, description, price, color, style, category, image_path 
        FROM Products
        '''
    ).fetchall()
    conn.close()
    
    # Creating a dictionary to hold unique products and their color variants
    unique_products = {}
    
    for product in products:
        
        base_id = product['id'].split('_')[0]  # Get the base ID (without variant number)
        if base_id not in unique_products:
            unique_products[base_id] = {
                'id': base_id,
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
                'style': product['style'],
                'category': product['category'],
                'image_path': product['image_path'],
                'variants': []
            }
        unique_products[base_id]['variants'].append({
            'color': product['color'],
            'image_path': product['image_path'],
            'variant_id': product['id']
        })

    cart_count = get_cart_count(current_user.id)    

    return render_template('browse.html', products=list(unique_products.values()), cart_count=cart_count)

# Route to handle adding items to the cart
@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    print(data)

    # Extract data from request
    variant_id = data.get('variantId')    
    product_id = data.get('productId')    
    quantity = data.get('quantity')    
    
    user_id = current_user.id  # Get the logged-in user's id

    try:
        # Create a database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the item is already in the cart
        cursor.execute('''
            SELECT id, quantity FROM Cart WHERE user_id = ? AND product_id = ? AND variant_id = ?
        ''', (user_id, product_id, variant_id))
        cart_item = cursor.fetchone()

        if cart_item:
            # If the item is already in the cart, update the quantity
            new_quantity = cart_item[1] + int(quantity)
            cursor.execute('''
                UPDATE Cart SET quantity = ? WHERE id = ?
            ''', (new_quantity, cart_item[0]))
        else:
            # Otherwise, insert a new item into the cart
            cursor.execute('''
                INSERT INTO Cart (user_id, product_id, variant_id, quantity)
                VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, variant_id, quantity))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Route for Cart Page
@app.route('/cart')
@login_required
def cart():
    try:
        # Create a database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()        

        # Fetch cart items for the logged-in user
        cursor.execute('''
            SELECT Cart.id, Cart.product_id, Cart.variant_id, Cart.quantity, Products.name, Products.price
            FROM Cart
            LEFT JOIN Products ON Cart.variant_id = Products.id
            WHERE Cart.user_id = ?
        ''', (current_user.id,))

        cart_items = cursor.fetchall()

        try:
            # Format the fetched items for rendering in the template
            formatted_items = [
                {
                    'cart_id': item[0],  # Cart ID
                    'product_id': item[1],  # Product ID
                    'variant_id': item[2],  # Variant ID
                    'quantity': int(item[3]),  # Quantity (converted from text)
                    'name': item[4],  # Product Name
                    'price': float(item[5]),  # Price (converted from text)
                    'total': int(item[3]) * float(item[5])  # Calculate total as quantity * price
                }
                for item in cart_items
            ]            

        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Error occurred while formatting cart items: {str(e)}")

        # Continue with the rest of the function
        try:
            # Calculate total amount for the cart
            cart_total = sum(item['total'] for item in formatted_items)

            # Pass cart count to update the cart icon
            cart_count = sum(item['quantity'] for item in formatted_items)

            # Render the cart template with the fetched items
            return render_template('cart.html', cart_items=formatted_items, cart_total=cart_total, cart_count=cart_count)

        except Exception as e:
            # Print the exception if the above fails
            print(f"Error occurred after formatting items: {str(e)}")
            flash(f'Error fetching cart items: {str(e)}', 'danger')
            return render_template('cart.html', cart_items=[], cart_total=0, cart_count=0)
        
    except Exception as e:
        flash(f'Error fetching cart items: {str(e)}', 'danger')
        return render_template('cart.html', cart_items=[], cart_total=0, cart_count=0)

# Route to Update Cart Item Quantity
@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    try:
        # Get the data from the AJAX request
        data = request.get_json()

        # Extract the cart information
        product_id = data['product_id']
        new_quantity = data['quantity']

        # Update the cart item quantity in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Cart
            SET quantity = ?
            WHERE user_id = ? AND product_id = ?
        ''', (new_quantity, current_user.id, product_id))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        # Return success response
        return jsonify({'success': True, 'message': 'Cart updated successfully.'})

    except Exception as e:
        # Handle errors
        return jsonify({'success': False, 'message': str(e)})

# Route to Remove Item from Cart
@app.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    try:
        # Get the data from the AJAX request
        data = request.get_json()

        # Extract the product ID to be removed
        product_id = data['product_id']

        # Delete the item from the cart in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Cart
            WHERE user_id = ? AND product_id = ?
        ''', (current_user.id, product_id))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        # Return success response
        return jsonify({'success': True, 'message': 'Item removed from cart successfully.'})

    except Exception as e:
        # Handle errors
        return jsonify({'success': False, 'message': str(e)})

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch cart items for the logged-in user
        cursor.execute('''
            SELECT Cart.id, Cart.product_id, Cart.variant_id, Cart.quantity, Products.name, Products.price
            FROM Cart
            LEFT JOIN Products ON Cart.variant_id = Products.id
            WHERE Cart.user_id = ?
        ''', (current_user.id,))

        cart_items = cursor.fetchall()       

        # Format the fetched items for rendering in the template
        formatted_items = [
            {
                'cart_id': item[0],  # Cart ID
                'product_id': item[1],  # Product ID
                'variant_id': item[2],  # Variant ID
                'quantity': int(item[3]),  # Quantity (converted from text)
                'name': item[4],  # Product Name
                'price': float(item[5]),  # Price (converted from text)
                'total': int(item[3]) * float(item[5])  # Calculate total as quantity * price
            }
            for item in cart_items
        ]

        # Calculate total amount for the cart
        cart_total = sum(item['total'] for item in formatted_items)

        # Handle POST request for order submission
        if request.method == 'POST':
            # Extract form data from the AJAX request
            data = request.get_json()
            street_address = data['streetAddress']
            city = data['city']
            state = data['state']
            zip_code = data['zipCode']
            card_number = data['cardNumber']
            expiry = data['expiry']
            cvv = data['cvv']

            # Hash sensitive information before saving to the database
            hashed_card_number = bcrypt.generate_password_hash(card_number).decode('utf-8')
            hashed_expiry = bcrypt.generate_password_hash(expiry).decode('utf-8')
            hashed_cvv = bcrypt.generate_password_hash(cvv).decode('utf-8')

            # Insert order into Orders table
            cursor.execute('''
                INSERT INTO Orders (user_id, shipping_street_address, shipping_city, shipping_state, shipping_zip, billing_street_address, billing_city, billing_state, billing_zip,
                                    credit_card_number, credit_card_expiry, credit_card_cvv, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_user.id, current_user.street_address, current_user.city, current_user.state, current_user.zip_code, street_address, city, state, zip_code, hashed_card_number, hashed_expiry, hashed_cvv, cart_total))
            
            # Retrieve the newly created order ID
            order_id = cursor.lastrowid

            # Insert items into OrderItems table
            for item in formatted_items:
                cursor.execute('''
                    INSERT INTO OrderItems (order_id, product_id, variant_id, quantity, price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, item['product_id'], item['variant_id'], item['quantity'], item['price']))

            # Clear the user's cart after successful order placement
            cursor.execute('DELETE FROM Cart WHERE user_id = ?', (current_user.id,))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

            # Return success response with redirect URL to confirmation page
            return jsonify({'success': True, 'redirect': url_for('confirmation')})

        # If it's a GET request, render the checkout page
        cart_count = sum(item['quantity'] for item in formatted_items)
        return render_template('checkout.html', cart_items=formatted_items, total=cart_total, cart_count=cart_count)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_accessibility', methods=['POST'])
@login_required
def update_accessibility():
    data = request.get_json()
    theme = data.get('theme')
    text_size = data.get('textSize')

    try:
        # Update user preferences in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Users SET theme = ?, text_size = ? WHERE id = ?
        ''', (theme, text_size, current_user.id))
        conn.commit()
        conn.close()

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route for Confirmation Page
@app.route('/confirmation', methods=['GET'])
@login_required
def confirmation():
    try:
        # Fetch recent order information for the logged-in user
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, total_amount
            FROM Orders
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (current_user.id,))
        order = cursor.fetchone()
        conn.close()

        if order:
            order_id, total_amount = order
        else:
            # If no order is found, set some defaults
            order_id, total_amount = None, 0

        # Render confirmation page with order details
        return render_template('confirmation.html', order_id=order_id, total_amount=total_amount)
    
    except Exception as e:
        # Handle exceptions gracefully and show an error message
        flash(f'Error fetching order details: {str(e)}', 'danger')
        return redirect(url_for('checkout'))

# Function to get the current cart count for the logged-in user
def get_cart_count(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantity) FROM Cart WHERE user_id = ?", (user_id,))
    cart_count = cursor.fetchone()[0]
    conn.close()

    return cart_count if cart_count else 0

@app.route('/cart_count', methods=['GET'])
@login_required
def cart_count():
    try:
        count = get_cart_count(current_user.id)
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Route for Account Page
@app.route('/account', methods=['GET'])
@login_required
def account():
    try:
        # Create a database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch user details from Users table
        cursor.execute('''
            SELECT username, first_name, last_name, shipping_street_address, shipping_city, shipping_state, shipping_zip
            FROM Users
            WHERE id = ?
        ''', (current_user.id,))
        user_data = cursor.fetchone()

        # Fetch orders for the current user
        cursor.execute('''
            SELECT id, order_date, status, total_amount
            FROM Orders
            WHERE user_id = ?
        ''', (current_user.id,))
        orders = cursor.fetchall()

        # Fetch order items for each order
        order_items_dict = {}
        for order in orders:
            order_id = order[0]
            cursor.execute('''
                SELECT product_id, variant_id, quantity, price
                FROM OrderItems
                WHERE order_id = ?
            ''', (order_id,))
            order_items = cursor.fetchall()
            order_items_dict[order_id] = order_items

        conn.close()

        # Format user data for rendering
        user = {
            'username': user_data[0],
            'first_name': user_data[1],
            'last_name': user_data[2],
            'street_address': user_data[3],
            'city': user_data[4],
            'state': user_data[5],
            'zip_code': user_data[6]
        }        

        return render_template('account.html', user=user, orders=orders, order_items_dict=order_items_dict)

    except Exception as e:
        flash(f'Error fetching account details: {str(e)}', 'danger')
        return render_template('account.html', user=None, orders=[], order_items_dict={})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
