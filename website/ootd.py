

# from urllib.parse import quote
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import asyncio
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# options = Options()
# options.add_argument('--headless')
# options.add_experimental_option("detach", True)
# wd = webdriver.Chrome(options=options)

# KEYWORD = "穿搭"
# keyword = quote(KEYWORD)

# def get_image_from_google_BEFORE(wd, keyword, delay, max_images):
#     encoded_keyword = quote(keyword)
#     def scroll_down(wd):
#         wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(delay)

#     url = f'https://www.google.com/search?&q={encoded_keyword}&tbm=isch'
#     wd.get(url)
    
#     image_urls = set()
#     skips = 0
    
#     # 這裡是為了讓網頁滾動，直到找到足夠的圖片
#     while len(image_urls) < max_images:    # + skip
#         # scroll_down(wd)
        
#         thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")  # 縮圖
        
#         for img in thumbnails[len(image_urls): max_images]:
            
#             try:
#                 img.click()
#                 time.sleep(delay)
#             except:
#                 continue
            
#             images = wd.find_elements(By.CLASS_NAME, "iPVvYb")  # 大張的
            
#             for image in images:
                
#                 img_height = image.get_attribute('height')
                
#                 # if image.get_attribute('src') in image_urls:
#                 #     max_images += 1
#                 #     skips += 1
#                 #     break
 
#                 if image.get_attribute('src') and 'http' in image.get_attribute('src'):
#                     image_urls.add(image.get_attribute('src'))
#                     print(f"Found {len(image_urls)}")
#                     if len(image_urls) >= max_images:
#                         break
             
    
#     image_urls_list = list(image_urls)                
#     return image_urls_list



import requests
from dotenv import load_dotenv
import os
# import random

load_dotenv()
GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
SEAECH_ENGINE_ID = os.getenv('SEAECH_ENGINE_ID')

def get_image_from_google(search_query, max_images):
    google_search_url = "https://customsearch.googleapis.com/customsearch/v1"
    params = { 
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEAECH_ENGINE_ID,
        "q": search_query,
        "searchType": "image",
        "dateRestrict" : "y[2]",
        "num": max_images,  # maximum 10
        "imgSize": "large",
    }

    response = requests.get(google_search_url, params=params)
    results = response.json()['items']

    # image list
    image_urls = []
    for item in results:
        image_urls.append(item['link'])
    
    if len(image_urls) == max_images:
        print("Found enough images")  
    
    return image_urls


    
    
    




def get_ootd(temp):
    clothes_temp = 26 - temp
    # clothes_temp_max = 26 - temp_max
    # clothes_temp_min = 26 - temp_min

    if clothes_temp < 1:
        # print("衣服推薦: 短袖短褲")
        recommend = "短袖短褲穿搭男" 
    elif 1 <= clothes_temp <= 6:
        # print("衣服推薦: 襯衫 + 長褲")
        recommend = "襯衫長褲穿搭男" 
    elif 5 <= clothes_temp <= 14:
        # print("衣服推薦: 帽T + 長褲 + 外套")
        recommend = "厚帽T穿搭男" 
    elif 14 <= clothes_temp:
        # print("衣服推薦: 厚長袖or厚帽T + 厚外套")
        recommend = "厚外套穿搭" 
    
    print(recommend)
    image_urls = get_image_from_google(recommend, 6)
    
    return image_urls
    
         
if __name__ == "__main__":
    search_query = "穿搭"
    image_urls = get_image_from_google(search_query, 6)
    
    for url in image_urls:
        print(url)

    # for url in image_urls:
    #     print(url)
    # wd.quit()





