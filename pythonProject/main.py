# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import openpyxl
# from datetime import datetime
#
# # 初始化 WebDriver
# driver = webdriver.Chrome()
#
# # 打开目标网站
# driver.get('https://weixin.sogou.com/')
#
# # 输入关键字并搜索
# search_box = driver.find_element(By.ID, 'query')
# search_box.send_keys('AI')
# search_box.send_keys(Keys.RETURN)
#
# # 等待页面加载
# time.sleep(5)
#
# # 创建 Excel 文件
# workbook = openpyxl.Workbook()
# sheet = workbook.active
# sheet.title = "AI WeChat Articles"
# sheet.append(['Title', 'Summary', 'Link', 'Source'])
#
# # 爬取前5页
# for page in range(1, 6):
#     articles = driver.find_elements(By.XPATH, '//div[@class="news-box"]//li')
#
#     for article in articles:
#         try:
#             title_element = article.find_element(By.XPATH, './/h3')
#             summary_element = article.find_element(By.XPATH, './/p[@class="txt-info"]')
#             link_element = title_element.find_element(By.XPATH, './/a')
#             source_element = article.find_element(By.XPATH, './/div[@class="s-p"]/a')
#
#             title = title_element.text
#             summary = summary_element.text
#             link = link_element.get_attribute('href')
#             source = source_element.text
#
#             sheet.append([title, summary, link, source])
#         except Exception as e:
#             print(f"Error processing article: {e}")
#             continue
#
#     # 点击下一页
#     try:
#         next_page = driver.find_element(By.ID, 'sogou_next')
#         next_page.click()
#         time.sleep(5)
#     except Exception as e:
#         print(f"No more pages or error: {e}")
#         break
#
# # 保存 Excel 文件
# filename = f"AI_微信_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
# workbook.save(filename)
#
# # 关闭 WebDriver
# driver.quit()
#
# print(f"Scraping completed. Data saved to {filename}")

import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from datetime import datetime


# 设置搜索关键字和爬取页数
keyword = "AI"
pages_to_scrape = 5

# 无需指定 ChromeDriver 的路径
service = Service()

# 无需指定 Chrome 浏览器的路径
options = Options()

# options.add_argument("--headless")  # 以无头模式运行，不打开浏览器窗口
driver = webdriver.Chrome(service=service, options=options)

# 打开网页
driver.get("https://weixin.sogou.com/")

# 输入关键字并点击搜索按钮
search_box = driver.find_element(By.ID, "query")
search_box.send_keys(keyword)
search_button = driver.find_element(By.XPATH, '//input[@value="搜文章"]')
search_button.click()

# 创建 Excel 文件
wb = Workbook()
ws = wb.active
ws.append(["标题", "摘要", "链接", "来源"])

# 爬取内容
for page in range(pages_to_scrape):
    print(f"正在爬取第 {page + 1} 页...")
    # 等待页面加载完成
    time.sleep(5)
    # 获取搜索结果列表
    search_results = driver.find_elements(By.XPATH, '//ul[@class="news-list"]/li')
    # 提取信息并写入 Excel
    for result in search_results:
        title = result.find_element(By.XPATH, './/h3/a').text
        abstract = result.find_element(By.XPATH, './/p[@class="txt-info"]').text
        link = result.find_element(By.XPATH, './/h3/a').get_attribute("href")
        source = result.find_element(By.XPATH, './/div[@class="s-p"]').text
        # 去除日期部分
        date_index = source.find("20")  # 找到日期的起始位置
        if date_index != -1:
            source = source[:date_index]  # 截取日期之前的内容
        ws.append([title, abstract, link, source])
    # 滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待下一页按钮出现
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'sogou_next')))
    except TimeoutException:
        print("已到达最后一页")
        break
    # 点击下一页按钮
    next_page_button = driver.find_element(By.ID, 'sogou_next')
    next_page_button.click()

# 保存 Excel 文件
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
file_name = f"{keyword}_微信_{current_time}.xlsx"
wb.save(file_name)

print(f"爬取完成，结果保存在 {file_name}")

# 关闭浏览器
driver.quit()
