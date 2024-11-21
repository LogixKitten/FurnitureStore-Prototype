import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            shipping_street_address TEXT NOT NULL,
            shipping_city TEXT NOT NULL,
            shipping_state TEXT NOT NULL,
            shipping_zip TEXT NOT NULL,            
            username TEXT UNIQUE NOT NULL,
            theme TEXT NOT NULL DEFAULT 'light',
            text_size TEXT NOT NULL DEFAULT 'regular',
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            color TEXT NOT NULL,
            style TEXT NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            variant_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(product_id) REFERENCES Products(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'Pending',
            total_amount DECIMAL(10, 2) NOT NULL,
            shipping_street_address TEXT NOT NULL,
            shipping_city TEXT NOT NULL,
            shipping_state TEXT NOT NULL,
            shipping_zip TEXT NOT NULL,
            billing_street_address TEXT,
            billing_city TEXT,
            billing_state TEXT,
            billing_zip TEXT,
            credit_card_number TEXT,
            credit_card_expiry TEXT,
            credit_card_cvv TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            variant_id TEXT,
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY(order_id) REFERENCES Orders(id)
        )
    ''')    

    # Insert example products into the Products table
    products = [
        ("MCDT01_01", "Walnut Classic Dining Table", "Timeless walnut wood rectangular table with a sleek mid-century aesthetic.", 549.99, "Brown", "Mid-Century", "Dining Table", "static/img/dining_table/MidCentury/Midcentury_Table1_brown.webp"),
        ("MCDT02_01", "Round Marble Top Dining Table", "Elegant round dining table featuring a marble top with natural wood legs.", 699.99, "Multi", "Mid-Century", "Dining Table", "static/img/dining_table/MidCentury/Midcentury_Table2_mixed1.webp"),
        ("MCDT03_01", "Walnut Minimalist Dining Table", "A contemporary dining table with walnut wood and modern black accents on the legs.", 599.99, "Multi", "Mid-Century", "Dining Table", "static/img/dining_table/MidCentury/Midcentury_Table3_mixed1.webp"),
        ("MCDT04_01", "Glass-Topped Mid-Century Table", "Unique mid-century style table with a glass top and angular wooden legs.", 749.99, "Multi", "Mid-Century", "Dining Table", "static/img/dining_table/MidCentury/Midcentury_Table4_brown.webp"),
        ("MDNDT01_01", "Concrete Round Table", "Bold and industrial-style round table with a solid concrete base and top.", 799.99, "Gray", "Modern", "Dining Table", "static/img/dining_table/Modern/Modern_Table1_gray.webp"),
        ("MDNDT02_01", "Tulip-Style Dining Table", "Sleek white dining table with a tulip-inspired base, perfect for minimalist spaces.", 599.99, "White", "Modern", "Dining Table", "static/img/dining_table/Modern/Modern_Table2_white.webp"),
        ("MDNDT03_01", "Rectangular Minimalist Table", "Clean and modern rectangular table with a glossy white finish.", 649.99, "White", "Modern", "Dining Table", "static/img/dining_table/Modern/Modern_Table3_white.webp"),
        ("MDNDT04_01", "All-Glass Modern Dining Table", "Ultra-modern table crafted entirely from glass, offering a transparent and airy design.", 899.99, "Glass", "Modern", "Dining Table", "static/img/dining_table/Modern/Modern_Table4_glass.webp"),
        ("MDNDT05_01", "White Panel Base Table", "Unique dining table with a glossy white surface and striking glass panel base.", 749.99, "Multi", "Modern", "Dining Table", "static/img/dining_table/Modern/Modern_Table5_mixed1.webp"),
        ("RUSDT01_01", "Handcrafted Log Dining Table", "Solid wood table crafted with natural log elements for a rustic and cozy charm.", 699.99, "Tan", "Rustic", "Dining Table", "static/img/dining_table/Rustic/Rustic_Table1_tan.jpg"),
        ("RUSDT02_01", "Round Pine Dining Table", "Beautifully rounded dining table made from polished pine wood for a warm, rustic vibe.", 599.99, "Tan", "Rustic", "Dining Table", "static/img/dining_table/Rustic/Rustic_Table2_tan.jpg"),
        ("RUSDT03_01", "Farmhouse Crossbeam Table", "Sturdy farmhouse-style table with a crossbeam base and distressed wood finish.", 749.99, "Brown", "Rustic", "Dining Table", "static/img/dining_table/Rustic/Rustic_Table3_brown.jpg"),
        ("RUSDT04_01", "Classic Rustic Bench Table", "Long and spacious wooden table with a classic rustic design ideal for family gatherings.", 899.99, "Brown", "Rustic", "Dining Table", "static/img/dining_table/Rustic/Rustic_Table4_brown.jpg"),
        ("SCNDT01_01", "Nordica Glass Dining Table", "Scandinavian-inspired table with a glass top and a warm walnut wood base.", 849.99, "Brown", "Scandinavian", "Dining Table", "static/img/dining_table/Scandinavian/Scandinavian_Table1_brown.webp"),
        ("SCNDT02_01", "Stockholm Oval Table", "Minimalist oval table with a curved oak wood finish, ideal for cozy spaces.", 599.99, "Tan", "Scandinavian", "Dining Table", "static/img/dining_table/Scandinavian/Scandinavian_Table2_tan.webp"),
        ("SCNDT03_01", "Helsinki Dining Table", "Sleek rectangular table featuring Danish design with light tan wood.", 649.99, "Tan", "Scandinavian", "Dining Table", "static/img/dining_table/Scandinavian/Scandinavian_Table3_tan.webp"),
        ("SCNDT04_01", "Oslo Angled Dining Table", "Stylish rectangular table with Scandinavian-style angled wood legs.", 699.99, "Tan", "Scandinavian", "Dining Table", "static/img/dining_table/Scandinavian/Scandinavian_Table4_tan.webp"),
        ("MCSOFA01_01", "The Moderne Curve", "Curved sofa with retro vibes and plush cushions for ultimate comfort.", 499.99, "Blue", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa1-blue.webp"),
        ("MCSOFA01_02", "The Moderne Curve", "Curved sofa with retro vibes and plush cushions for ultimate comfort.", 499.99, "Gray", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa1-gray.webp"),
        ("MCSOFA01_03", "The Moderne Curve", "Curved sofa with retro vibes and plush cushions for ultimate comfort.", 499.99, "Tan", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa1-tan.webp"),
        ("MCSOFA02_01", "The Grid Luxe", "A boxy silhouette with textured upholstery and geometric accents.", 549.99, "Blue", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa2-blue.webp"),
        ("MCSOFA02_02", "The Grid Luxe", "A boxy silhouette with textured upholstery and geometric accents.", 549.99, "Tan", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa2-tan.webp"),
        ("MCSOFA03_01", "Velvet Haven", "Luxurious tufted velvet sofa bringing timeless sophistication.", 599.99, "Green", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa3-green.webp"),
        ("MCSOFA04_01", "Heritage Luxe", "Streamlined design with finely stitched upholstery for elegance.", 549.99, "Tan", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa4-tan.webp"),
        ("MCSOFA04_02", "Heritage Luxe", "Streamlined design with finely stitched upholstery for elegance.", 549.99, "White", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa4-white.webp"),
        ("MCSOFA05_01", "Scandi Comfort", "Minimalist design focusing on functionality and elegance.", 479.99, "White", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa5-white.webp"),
        ("MCSOFA06_01", "The Urbane Lounge", "Spacious design combining comfort and simplicity for modern living.", 529.99, "Gray", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa6-gray.webp"),
        ("MCSOFA07_01", "Metro Relax", "Refined sofa perfect for urban lifestyles with modern aesthetics.", 509.99, "Gray", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa7-gray.webp"),
        ("MCSOFA08_01", "Tapered Retreat", "Stylish design with tapered legs and exceptional durability.", 569.99, "Green", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa8-green.webp"),
        ("MCSOFA09_01", "The Timeless Flair", "Blending mid-century design with modern versatility for any decor.", 579.99, "Tan", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa9-tan.webp"),
        ("MCSOFA10_01", "Retro Elegance", "Seamless blend of vintage aesthetics and modern comfort.", 599.99, "Blue", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa10-blue.webp"),
        ("MCSOFA10_02", "Retro Elegance", "Seamless blend of vintage aesthetics and modern comfort.", 599.99, "Green", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa10-green.webp"),
        ("MCSOFA11_01", "Grove Sofa", "A minimalist masterpiece, this sofa blends modern simplicity with a classic mid-century frame.", 599.99, "Gray", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa11-gray.webp"),
        ("MCSOFA11_02", "Grove Sofa", "A minimalist masterpiece, this sofa blends modern simplicity with a classic mid-century frame.", 599.99, "Green", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa11-green.webp"),
        ("MCSOFA11_03", "Grove Sofa", "A minimalist masterpiece, this sofa blends modern simplicity with a classic mid-century frame.", 599.99, "White", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa11-white.webp"),
        ("MCSOFA11_04", "Grove Sofa", "A minimalist masterpiece, this sofa blends modern simplicity with a classic mid-century frame.", 599.99, "Yellow", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa11-yellow.webp"),
        ("MCSOFA12_01", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Blue", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-blue.webp"),
        ("MCSOFA12_02", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Gray", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-gray.webp"),
        ("MCSOFA12_03", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Green", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-green.webp"),
        ("MCSOFA12_04", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Lavender", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-lavender.webp"),
        ("MCSOFA12_05", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Pink", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-pink.webp"),
        ("MCSOFA12_06", "Royale Sofa", "A luxurious statement piece, this sofa features tufted upholstery and a timeless mid-century curved design.", 799.99, "Red", "Mid-Century", "Sofa", "static/img/sofa/MidCentury/midcentury-sofa12-red.webp"),
        ("MDNSOFA01_01", "Urban Luxe Sofa", "Contemporary elegance meets luxurious comfort in this modern sofa, crafted with sleek materials and minimalist metal legs.", 899.99, "Black", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa1-black.webp"),
        ("MDNSOFA01_02", "Urban Luxe Sofa", "Contemporary elegance meets luxurious comfort in this modern sofa, crafted with sleek materials and minimalist metal legs.", 899.99, "White", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa1-white.webp"),
        ("MDNSOFA02_01", "Minimalist Comfort Sofa", "Designed for the modern minimalist, this sleek sofa offers clean lines and an understated elegance perfect for any contemporary space.", 749.99, "Black", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa2-black.webp"),
        ("MDNSOFA02_02", "Minimalist Comfort Sofa", "Designed for the modern minimalist, this sleek sofa offers clean lines and an understated elegance perfect for any contemporary space.", 749.99, "Green", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa2-green.webp"),
        ("MDNSOFA02_03", "Minimalist Comfort Sofa", "Designed for the modern minimalist, this sleek sofa offers clean lines and an understated elegance perfect for any contemporary space.", 749.99, "Yellow", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa2-yellow.webp"),
        ("MDNSOFA03_01", "Vintage Streamline Sofa", "A bold statement of retro-modern design, this sofa features handcrafted leather panels and a distinct silhouette for timeless appeal.", 1099.99, "Brown", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa3-brown.webp"),
        ("MDNSOFA03_02", "Vintage Streamline Sofa", "A bold statement of retro-modern design, this sofa features handcrafted leather panels and a distinct silhouette for timeless appeal.", 1099.99, "Green", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa3-green.webp"),
        ("MDNSOFA03_03", "Vintage Streamline Sofa", "A bold statement of retro-modern design, this sofa features handcrafted leather panels and a distinct silhouette for timeless appeal.", 1099.99, "Tan", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa3-tan.webp"),
        ("MDNSOFA04_01", "Metro Luxe Lounge Sofa", "This ultra-modern sofa combines geometric precision with plush comfort, making it the centerpiece of your stylish living room.", 1199.99, "Black", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa4-black.webp"),
        ("MDNSOFA04_02", "Metro Luxe Lounge Sofa", "This ultra-modern sofa combines geometric precision with plush comfort, making it the centerpiece of your stylish living room.", 1199.99, "White", "Modern", "Sofa", "static/img/sofa/Modern/Modern-Sofa4-white.webp"),
        ("RUSSOFA01_01", "Woodland Retreat Sofa", "Crafted with rich wooden paneling and plush leather cushions, this sofa brings the charm of a cabin retreat to your living space. Its robust frame and timeless design make it perfect for cozy evenings by the fire.", 479.99, "Brown", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa1_brown.jpg"),
        ("RUSSOFA01_02", "Woodland Retreat Sofa", "Crafted with rich wooden paneling and plush leather cushions, this sofa brings the charm of a cabin retreat to your living space. Its robust frame and timeless design make it perfect for cozy evenings by the fire.", 479.99, "Gray", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa1_gray.jpg"),
        ("RUSSOFA01_03", "Woodland Retreat Sofa", "Crafted with rich wooden paneling and plush leather cushions, this sofa brings the charm of a cabin retreat to your living space. Its robust frame and timeless design make it perfect for cozy evenings by the fire.", 479.99, "White", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa1_white.jpg"),
        ("RUSSOFA02_01", "Timber Haven Sofa", "Featuring a solid wood frame with a natural finish, this sofa embodies rustic elegance. Its durable cushions offer comfort and style, ideal for any lodge-inspired home.", 499.99, "Brown", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa2_brown.jpg"),
        ("RUSSOFA03_01", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi1.jpg"),
        ("RUSSOFA03_02", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi2.jpg"),
        ("RUSSOFA03_03", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi3.jpg"),
        ("RUSSOFA03_04", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi4.jpg"),
        ("RUSSOFA03_05", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi5.jpg"),
        ("RUSSOFA03_06", "Lodgeview Sofa", "A true centerpiece for rustic homes, this sofa boasts intricately patterned upholstery and solid wood accents. Its warm, inviting design is perfect for creating a welcoming atmosphere.", 549.99, "Multi", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa3_multi6.jpg"),
        ("RUSSOFA04_01", "Barnwood Charm Sofa", "With distressed wood details and supple leather seating, this sofa blends rustic aesthetics with modern comfort. It's a perfect addition to homes seeking character and sophistication.", 529.99, "Brown", "Rustic", "Sofa", "static/img/sofa/Rustic/Rustic_Sofa4_brown.jpg"),
        ("SCNSOFA01_01", "Nordic Haven Recliner - Gray", "Elegant Scandinavian-style recliner with clean lines and adjustable comfort.", 649.99, "Gray", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa1_gray.jpg"),
        ("SCNSOFA02_01", "BJÖRKSTA Sofa", "Elegant Scandinavian-inspired sofa with soft curves and timeless appeal, perfect for modern living spaces.", 649.99, "Green", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa2_green.jpg"),
        ("SCNSOFA02_02", "BJÖRKSTA Sofa", "Elegant Scandinavian-inspired sofa with soft curves and timeless appeal, perfect for modern living spaces.", 649.99, "Tan", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa2_tan.jpg"),
        ("SCNSOFA03_01", "Skandi Charm Couch", "Minimalist tufted design for a perfect blend of comfort and style.", 749.99, "Gray", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa3_gray.jpg"),
        ("SCNSOFA04_01", "Oslo Luxe Lounger", "Sleek leather-inspired design with timeless Nordic appeal.", 899.99, "Gray", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa4_gray.webp"),
        ("SCNSOFA05_01", "Green Fjord Lounger", "Relax in style with Scandinavian simplicity and plush seating.", 799.99, "Green", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa5_green.jpg"),
        ("SCNSOFA06_01", "Crimson Fjord Sofa", "Brighten up your space with this bold and cozy Scandinavian-inspired couch.", 829.99, "Red", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa6_red.jpg"),
        ("SCNSOFA07_01", "Emerald Bay Couch", "Bring the serenity of nature indoors with this vibrant Scandinavian seating.", 849.99, "Green", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa7_green.jpg"),
        ("SCNSOFA08_01", "Arctic Cloud Recliner", "Ultra-cozy recliner with modern Scandinavian aesthetics and soft fabric.", 879.99, "White", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa8_white.jpg"),
        ("SCNSOFA09_01", "Rustic Fjell Seat", "Classic Scandinavian sofa with earthy tones and a charming wooden frame.", 899.99, "Tan", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa9_tan.webp"),
        ("SCNSOFA09_02", "Rustic Fjell Seat", "Classic Scandinavian sofa with earthy tones and a charming wooden frame.", 899.99, "Yellow", "Scandinavian", "Sofa", "static/img/sofa/Scandinavian/Scandinavian_Sofa9_yellow.webp")
    ]

    # Insert the products into the table
    cursor.executemany("""
        INSERT INTO Products (id, name, description, price, color, style, category, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    connection.commit()
    connection.close()
    print("Database initialized and populated!")

if __name__ == '__main__':
    init_db()