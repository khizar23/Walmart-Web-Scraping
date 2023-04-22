from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as CO
from selenium.webdriver.firefox.options import Options as FO
import warnings, os, sys, threading, re, random, concurrent
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import warnings
import undetected_chromedriver as uc


warnings.filterwarnings("ignore")



l = []


def load_links():
	
	linkss = []
	
	import pandas as pd

	links = pd.read_csv("link2s.csv")
	for i in links["url"]:
		linkss.append(i)
		
	return linkss
		
# print(load_links())

def main_m(url):
	# for i in range(1,5):
	
	global l
	
	obj={}

	options = CO()
	options.headless = True
	options.add_argument("--disable-extensions")
	# options.add_argument("window-size=720,640")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-gpu")
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--disable-blink-features=AutomationControlled')	
	
	# linkss.append(i)
	# url = i

	# driver = webdriver.Chrome("./chromedriver", options=options)
	driver = uc.Chrome(options=options, version_main=112)
	print(f"getting {url}")
	driver.get(f"{url}")
	
	fr_shp = ""
	rev_cnt = 0
	
	for fre_shp in driver.find_elements(by=By.XPATH, value='//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[4]/div/div/div/div[2]/span'):
		# print(fre_shp.text)
		if "Free" in fre_shp.text:
			fr_shp = "TRUE"
		else:
			fr_shp = "FALSE"
			
			# //*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[5]/div/div/div[1]/div[2]/span
			
	for revs_cnt in driver.find_elements(by=By.XPATH, value='//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/section/div/div/a'):
		rev_cnt = revs_cnt.text
		
	# for pro_sell in driver.find_elements(by=By.XPATH, value=''):
	#	 rev_cnt = revs_cnt.text
		

	# time.sleep(5)

	soup = BeautifulSoup(driver.page_source, "html")
	# print(soup)
	# sleep(5)
	driver.quit()
	del driver


	try:
		obj["price"] = soup.find("span",{"itemprop":"price"}).text.replace("Now ","")
	except:
		obj["price"]=None
		
	try:
		obj["name"] = soup.find("h1",{"itemprop":"name"}).text
	except:
		obj["name"]=None

	try:
		obj["rating"] = soup.find("span",{"class":"rating-number"}).text.replace("\n","").replace("(","").replace(")","")
	except:
		obj["rating"]=None
		
	try:
		obj["arrives by"] = soup.find("span",{"class":"b black"}).text.replace("\n","").replace("            ","")
	except:
		obj["arrives by"]=None
		
	try:
		obj["to"] = soup.find("div",{"class":"di"}).text.replace("\n","")
	except:
		obj["to"]=None

	try:
		obj["sold and shipped by"] = soup.find("span",{"class":"lh-title"}).text.replace("\n","").replace("Sold and shipped by","")
	except:
		obj["sold and shipped by"]=None
		
	try:
		obj["pro seller"] = soup.find("span",{"class":"nowrap inline-flex items-center v-btm black"}).text.replace("\n","")
	except:
		obj["pro seller"]=None
		
	try:
		obj["Out Of Stock"] = soup.find("div",{"class":"b gray pr3 pt2-m"}).text.replace("\n","")
	except:
		obj["Out Of Stock"]=None
	
	try:
		obj["Category"] = soup.find("ol",{"class":"w_4HBV"}).text.replace("\n"," ")
	except:
		obj["Category"]=None
		
	obj["URL"] = url
	obj["Free Shipping"] = fr_shp
	obj["Reviews"] = rev_cnt
	
	# print(obj)
	l.append(obj)	



		
try:
	try:		
		# max_work = int(input("num of threads: "))
		max_work = 3								
		with ThreadPoolExecutor(max_workers=max_work) as ex:
			paggg = load_links()
			tasks = {ex.submit(main_m, pag): pag for pag in paggg}
			for task in concurrent.futures.as_completed(tasks):
				login = tasks[task]
				try:
					data = task.result()
				except Exception as exc:
					pass
					# print('exc:...: ', exc , "\n Ignoring...")
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
except Exception as E:
	sys.exit(0)
	# print(E)

df = pd.DataFrame.from_dict(l)
# print(df.head())
df.to_csv("walmartout.csv", index=False)
