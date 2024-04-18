@echo off

start cmd /k "cd user\ && set FLASK_APP=user_app.py && flask run --port 5001"
start cmd /k "cd product\ && set FLASK_APP=product_app.py && flask run --port 5100"
start cmd /k "cd review\ && set FLASK_APP=review_app.py && flask run --port 5200"
start cmd /k "cd wishlist\ && set FLASK_APP=wishlist_app.py && flask run --port 5250"
start cmd /k "cd profile\ && set FLASK_APP=profile_app.py && flask run --port 5050"
