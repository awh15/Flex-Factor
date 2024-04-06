#!/bin/bash

# Start User Service
echo "Starting User Service..."
FLASK_APP=user/user_app.py FLASK_RUN_PORT=5000 flask run &
echo "User Service started"

# Start Product Service
echo "Starting Product Service..."
FLASK_APP=product/product_app.py FLASK_RUN_PORT=5100 flask run &
echo "Product Service started"

# Start Review Service
echo "Starting Review Service..."
FLASK_APP=review/review_app.py FLASK_RUN_PORT=5200 flask run &
echo "Review Service started"

# Start Wishlist Service
echo "Starting Wishlist Service..."
FLASK_APP=wishlist/wishlist_app.py FLASK_RUN_PORT=5250 flask run &
echo "Wishlist Service started"

# Start Profile Service
echo "Starting Profile Service..."
FLASK_APP=profile/profile_app.py FLASK_RUN_PORT=5050 flask run &
echo "Profile Service started"

# Wait for all services to finish

