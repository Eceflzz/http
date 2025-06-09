import json
import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        return users if isinstance(users, dict) else {}
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading users.json: {e}")
        return {}

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

users = load_users()
shown_recommendations = {}

def load_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading {filename}: {e}")
        return []

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session['username'] = username
            if 'favorites' not in session:
                session['favorites'] = {}
            return redirect(url_for('mood_page'))

        return render_template("login.html", error="Kullanıcı adı veya şifre yanlış.")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("register.html", error="Username already exists.")

        users[username] = password
        save_users(users)
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/mood", methods=["GET", "POST"])
def mood_page():
    if request.method == "POST":
        mood = request.form["mood"]
        return redirect(url_for('category_page', mood=mood))
    return render_template("mood_selection.html")

@app.route("/category/<mood>", methods=["GET", "POST"])
def category_page(mood):
    if request.method == "POST":
        category = request.form.get("category")
        if category:
            category_files = {
                "movie": "movie.json",
                "book": "book.json",
                "music": "music.json"
            }

            recommendations = load_data(category_files.get(category, ""))
            if not recommendations:
                return render_template("no_suggestions.html", mood=mood)

            # Mood’a göre filtrele
            recommendations = [r for r in recommendations if r["mood"].upper() == mood.upper()]

            # Kullanıcıya gösterilen önerilerde tekrar gösterilmeyenleri seç
            shown_recommendations[mood] = shown_recommendations.get(mood, [])
            available_recommendations = [r for r in recommendations if r not in shown_recommendations[mood]]

            if not available_recommendations:
                return render_template("no_suggestions.html", mood=mood)

            # Rastgele öneri seç
            random_recommendation = random.choice(available_recommendations)
            shown_recommendations[mood].append(random_recommendation)

            return render_template("recommendation.html", mood=mood, category=category, recommendation=random_recommendation)

    return render_template("category_selection.html", mood=mood)

@app.route("/retry/<mood>/<category>")
def retry_page(mood, category):
    category_files = {
        "movie": "movie.json",
        "book": "book.json",
        "music": "music.json"
    }

    recommendations = load_data(category_files.get(category, ""))
    if not recommendations:
        return render_template("no_suggestions.html", mood=mood)

    # Mood’a göre filtrele
    recommendations = [r for r in recommendations if r["mood"].upper() == mood.upper()]

    # Kullanıcıya gösterilen önerilerde tekrar gösterilmeyenleri seç
    shown_recommendations[mood] = shown_recommendations.get(mood, [])
    available_recommendations = [r for r in recommendations if r not in shown_recommendations[mood]]

    if not available_recommendations:
        return render_template("no_suggestions.html", mood=mood)

    # Rastgele öneri seç
    random_recommendation = random.choice(available_recommendations)
    shown_recommendations[mood].append(random_recommendation)

    return render_template("recommendation.html", mood=mood, category=category, recommendation=random_recommendation)

@app.route('/no_suggestions/<mood>')
def no_suggestions(mood):
    return render_template('no_suggestions.html', mood=mood)

@app.route('/add-favorite', methods=['POST'])
def add_favorite():
    data = request.get_json(force=True)
    
    if not data:
        return 'No data received', 400

    item_id = data.get('item')
    category = data.get('category')
    
    if not item_id or not category:
        return 'Item or Category missing', 400
    
    user_id = session.get('username')
    if not user_id:
        return 'User not logged in', 401
    
    if 'favorites' not in session:
        session['favorites'] = {}

    if category not in session['favorites']:
        session['favorites'][category] = []

    # Eğer item zaten favorilere eklenmişse, tekrar eklenmesin
    if item_id not in session['favorites'][category]:
        session['favorites'][category].append(item_id)
        session.modified = True  # Favoriler güncellenmiş olarak işaretlenmeli

    # --- JSON dosyasına da kaydet ---
    try:
        with open('favorites.json', 'r', encoding='utf-8') as f:
            all_favorites = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_favorites = {}

    if user_id not in all_favorites:
        all_favorites[user_id] = {'favorites': {}}

    if category not in all_favorites[user_id]['favorites']:
        all_favorites[user_id]['favorites'][category] = []

    if item_id not in all_favorites[user_id]['favorites'][category]:
        all_favorites[user_id]['favorites'][category].append(item_id)

    # JSON dosyasını güncelle
    with open('favorites.json', 'w', encoding='utf-8') as f:
        json.dump(all_favorites, f, ensure_ascii=False, indent=4)

    return '', 200

@app.route('/remove-favorite', methods=['POST'])
def remove_favorite():
    # Correct way to get the JSON data
    data = request.get_json()

    # Verifying if the data is correctly parsed
    if not data:
        return 'No data received', 400

    item_id = data.get('item_id')
    category = data.get('category')

    # Verifying that item_id and category are present
    if not item_id or not category:
        return "Missing item or category", 400

    # Checking if user is logged in
    user_id = session.get('username')
    if not user_id:
        return "User not logged in", 401

    # Checking and updating the session favorites
    if 'favorites' in session:
        if category in session['favorites'] and item_id in session['favorites'][category]:
            session['favorites'][category].remove(item_id)

            # Remove the category if it's empty
            if not session['favorites'][category]:
                del session['favorites'][category]

            session.modified = True
        else:
            return "Favorite not found", 400

    # Update the favorites in the JSON file
    try:
        with open('favorites.json', 'r', encoding='utf-8') as f:
            all_favorites = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_favorites = {}

    if user_id in all_favorites and category in all_favorites[user_id]['favorites']:
        if item_id in all_favorites[user_id]['favorites'][category]:
            all_favorites[user_id]['favorites'][category].remove(item_id)

            # Remove the category if it's empty
            if not all_favorites[user_id]['favorites'][category]:
                del all_favorites[user_id]['favorites'][category]

            # Save the updated data
            with open('favorites.json', 'w', encoding='utf-8') as f:
                json.dump(all_favorites, f, ensure_ascii=False, indent=4)

            session.modified = True
        else:
            return "Favorite not found in JSON", 400
    else:
        return "User's favorites not found", 400

    return '', 200

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['username']
    detailed_favorites = []

    try:
        with open('favorites.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        user_favorites = data.get(user_id, {}).get('favorites',{})

        for category, ids in user_favorites.items():
            for item_id in ids:
                item_data = get_item_by_id(item_id, category)
                if item_data:
                    detailed_favorites.append(item_data)

    except FileNotFoundError:
        pass                

    return render_template('favorites.html', favorites=detailed_favorites)


def get_item_by_id(item_id, category):
    category_files = {
        "movie": "movie.json",
        "book": "book.json",
        "music": "music.json"
    }

    if category not in category_files:
        return None

    try:
        with open(category_files[category], "r", encoding="utf-8") as file:
            items = json.load(file)
        return next((item for item in items if item['id'] == item_id), None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    app.secret_key = 'your_secret_key'
    app.run(port=5050)