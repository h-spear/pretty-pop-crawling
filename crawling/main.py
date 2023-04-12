import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import urllib.request as url_req
import os
import time
from web_driver import web_driver_chrome_options
from file_utils import FileUtils

options = web_driver_chrome_options()

# save path
IMG_SAVE_PATH = "save/img/"
EXCEL_SAVE_PATH = "save/"


def extract_goodsno(url):
    goodsno_start_idx = url.index("goodsno=") + 8
    goodsno_end_idx = url.index("&", goodsno_start_idx)
    return url[goodsno_start_idx:goodsno_end_idx]


def url_download(image_url, save_path, file_name):
    ext = image_url.split(".")[-1]
    url_req.urlretrieve(image_url, save_path + "/" + file_name + "." + ext)


def download_goods_img(url, category_code, goods_no):
    FileUtils.create_directory(IMG_SAVE_PATH + category_code)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)

    response = requests.get(url)

    if response.status_code == 200:
        elem_img = driver.find_element(By.CSS_SELECTOR, "#objImg")
        image_url = elem_img.get_attribute("src")
        url_download(image_url, IMG_SAVE_PATH + category_code, goods_no)
    else:
        print(response.status_code)

    driver.close()


def crawling(category_code, max_page):
    print(f"start... category={category_code}")
    results = {"goodsno": [], "name": [], "url": [], "price": [], "category": []}

    start = time.time()
    for i in range(1, max_page + 1):
        print(f"  {i} page crawling...")
        url = (
            "http://prettypop.co.kr/shop/goods/goods_list.php?&category="
            + category_code
            + "&page="
            + str(i)
        )
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)

        # soup = BeautifulSoup(driver.page_source, "html.parser")
        response = requests.get(url)

        if response.status_code == 200:

            # 상품 url로부터 goodsno, 이미지를 추출할 link를 가져옴
            elems_tg_anchor = driver.find_elements(
                By.CSS_SELECTOR, ".thumb-gallery > a"
            )
            for elem in elems_tg_anchor:
                goods_url = elem.get_attribute("href")
                results["goodsno"].append(extract_goodsno(goods_url))
                results["url"].append(goods_url)

            # 상품 이름
            elems_div1_anchor = driver.find_elements(
                By.CSS_SELECTOR, ".gallery-info-wrap > div:nth-child(1) > a"
            )
            for elem in elems_div1_anchor:
                results["name"].append(elem.text)

            # 상품 가격
            elems_div2 = driver.find_elements(
                By.CSS_SELECTOR, ".gallery-info-wrap > div:nth-child(2)"
            )
            for elem in elems_div2:
                results["price"].append(elem.text)
                results["category"].append(category_code)

        else:
            print(response.status_code)

        driver.close()
    end = time.time()
    print(f"  find all infomation! {end - start:.5f} sec")

    # 엑셀 파일로 저장
    start = time.time()
    print(f"  saving to excel...")
    FileUtils.create_directory(EXCEL_SAVE_PATH)
    df = pd.DataFrame(results)
    df.to_excel(EXCEL_SAVE_PATH + category_code + ".xlsx")
    end = time.time()
    print(f"  saved excel successfully! {category_code}.xlsx {end - start:.5f} sec")

    print(f"terminate!")
    print()


tuples = [
    ("001", 5),
    ("003", 6),
    ("005", 27),
    ("006", 26),
    ("007", 2),
    ("008", 2),
    ("010", 1),
    ("013", 4),
]

# crawling
start_index = 0
for i, (category_code, max_page) in enumerate(tuples):
    if i < start_index:
        continue
    for j in range(max_page):
        try:
            crawling(category_code, max_page)
        except:
            print(f"operation be stopped! {category_code} {j}")


# image download
fail = []
for categody_code, _ in tuples:
    df = pd.read_excel(
        EXCEL_SAVE_PATH + categody_code + ".xlsx",
        sheet_name="Sheet1",
        engine="openpyxl",
    )

    for no, url in zip(df["goodsno"], df["url"]):

        if not FileUtils.exist_img_file(IMG_SAVE_PATH + categody_code + "/" + str(no)):
            print(f"download... {url}")
            try:
                download_goods_img(url, categody_code, str(no))
                print(f"success. {no}")
            except:
                fail.append((no, url))
                print(f"fail! {no}")
print(fail)
