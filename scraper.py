from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
def callAPI(name, price):
            # URL của endpoint Strapi API
            api_url = 'http://localhost:1337/api/products?populate=*' 

            # Dữ liệu cần gửi
            data = { "data" : {
                 "name": name,
                "description": "Mô tả sản phẩm",
                "price": int(price),
                "category": 4,  
                "image": [25],
                "status": 1,
                "discount": 10,
                "details": "Chi tiết sản phẩm"
            }
                
            }

            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.post(api_url, json=data, headers=headers)

            if response.status_code == 200:
                print('Dữ liệu đã được gửi thành công.')
                print('Phản hồi:', response.json())
            else:
                print('Lỗi khi gửi dữ liệu.')
                print('Mã lỗi:', response.status_code)
                print('Nội dung lỗi:', response.json())
def get_amazon_product_details(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Đường dẫn tới chromedriver
    service = Service(r"C:\Users\pc\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        
        # Lấy tiêu đề sản phẩm
        product_title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        ).text.strip()
        print(f"Product Title: {product_title}")
        
        # Lấy giá sản phẩm
        try:
            price_whole = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            ).text.replace(',', '')
            price = f"{price_whole}"
        except:
            price = "N/A"
        
        print(f"Price: {price}")

        callAPI(product_title, price)
    except Exception as e:
        print(f"Error: Unable to retrieve product details from {url}. Exception: {e}")
    finally:
        driver.quit()

def main():
    # Thiết lập ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Đường dẫn tới chromedriver
    service = Service(r"C:\Users\pc\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = "https://www.amazon.com/gp/goldbox/"
    driver.get(url)
    
    try:
        # Chờ cho các liên kết sản phẩm xuất hiện
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-card-link']"))
        )
        
        product_links = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card-link']")
        
        # Lấy href từ từng liên kết và xử lý
        for link in product_links:
            href = link.get_attribute('href')
            print(f"Link product: {href}")
            get_amazon_product_details(href)
    except Exception as e:
        print(f"Error: Unable to retrieve product links. Exception: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
