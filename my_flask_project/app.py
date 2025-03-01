from flask import Flask, jsonify, render_template, send_from_directory
import json
import os

app = Flask(__name__)

# JSON verilerini yükleyen fonksiyon
def load_data():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommendations/<mood>")
def recommend(mood):
    try:
        data = load_data()
        movies = [movie for movie in data["movies"] if mood in movie["moods"]]
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)})

# Statik resim dosyalarını almak için
@app.route('/static/images/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

if __name__ == "__main__":
    app.run(debug=True)
