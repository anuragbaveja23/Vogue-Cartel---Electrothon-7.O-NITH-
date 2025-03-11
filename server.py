from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__, static_folder="static", template_folder="templates")  # Ensure Flask serves frontend files

@app.route('/')
def home():
    css_url =  url_for('static', filename= 'style.css')
    return render_template("index.html")  # Serves index.html


@app.route('/get-price', methods=['GET'])
def get_price():
    store = request.args.get("store")

    # Define product URLs
    PRODUCT_URLS = {
        "amazon": "https://www.amazon.in/Jordan-Mens-Sneaker-White-Black-sail/dp/B0CH1WTFHZ/",
        "flipkart": "https://www.flipkart.com/nike-full-force-low-sneakers-men/p/itm90e4293b6188a"
    }

    url = PRODUCT_URLS.get(store)
    if not url:
        return jsonify({"error": "Invalid store"}), 400

    # Scraping function
    price = scrape_amazon() if store == "amazon" else scrape_flipkart()

    return jsonify({"store": store, "price": price, "link": url})

# ✅ Amazon Scraping Function
def scrape_amazon():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://www.amazon.in/Jordan-Mens-Sneaker-White-Black-sail/dp/B0CH1WTFHZ/", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    price_element = soup.find("span", {"class": "a-price-whole"})
    if not price_element:
        price_element = soup.find("span", {"class": "priceBlockBuyingPriceString"})

    return price_element.text.strip() if price_element else "Price Not Found"

# ✅ Flipkart Scraping Function
def scrape_flipkart():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.flipkart.com/nike-full-force-low-sneakers-men/p/itm90e4293b6188a")
    driver.implicitly_wait(5)

    try:
        price_element = driver.find_element("xpath", "//div[contains(@class, '_30jeq3')]")
        price = price_element.text.strip()
    except:
        price = "Price Not Found"

    driver.quit()
    return price

if __name__ == "__main__":
    app.run(debug=True)
