from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
def download_image(image_url, file_name):
    """Download an image from a URL and save it locally."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {file_name}")
    else:
        print(f"Failed to download image from {image_url}. Status code: {response.status_code}")



    strapi_url = 'http://localhost:1337/api/upload'

    try:
        with open(file_name, 'rb') as image_file:
            files = {'files': image_file}
            upload_response = requests.post(strapi_url, files=files)
            upload_response.raise_for_status()
            
            print('Upload thành công:', upload_response.json())
            return upload_response.json()[0]['id'] 
    except Exception as err:
        print(f"An error occurred while uploading the image: {err}")

def callAPI(name, price, imgId):
            api_url = 'http://localhost:1337/api/products?populate=*' 

            data = { "data" : {
                 "name": name,
                "description": "Mô tả sản phẩm",
                "price": int(price),
                "category": 4,  
                "image": [imgId],
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


        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "imgTagWrapperId"))
        )
        image_url = image_element.find_element(By.TAG_NAME, "img").get_attribute("src")
        print(f"Image URL: {image_url}")

        # Đặt tên file ảnh dựa trên tên sản phẩm
        image_file_name = f"{product_title.replace(' ', '_')}.jpg"
        imgId = download_image(image_url, image_file_name)

        callAPI(product_title, price, imgId)
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
