import requests
from bs4 import BeautifulSoup
import csv

###Writing into a CSV file
new_file = open("C:/Users/user/Desktop/Univelcity/Jumia Smartphones.csv", mode = "w", encoding = "utf-8", newline = "")
pen = csv.writer(new_file)
pen.writerow(["S|N", "brand Name", "specifications", "old Price", "new Price", "discount", "rating"])

entire_data = []
index = 1

for num in range(1, 50):
    url = f"https://jumia.com.ng/smartphones/?page={num}#catalog-listing"
    if num == 1:
        url = "https://jumia.com.ng/smartphones/"
        
    headers = requests.utils.default_headers()
    headers.update(
        {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}
    )

    my_result = requests.get(url, headers)
    f_soup = BeautifulSoup(my_result.content, features = "lxml")
    s_soup = f_soup.find("div", attrs = {"class" : "-paxs row _no-g _4cl-3cm-shs"})
    list_of_soups = s_soup.find_all("article", attrs = {"class" : "prd _fb col c-prd"})

    for soup in list_of_soups:
        smartphones_details = soup.find("a")

        ###To get the brand
        try:
            smartphone_brand_name = smartphones_details.get("data-brand")
        except:
            smartphone_brand_name = None

        ###To get the Specifications
        try:
            smartphone_specifications = smartphones_details.get("data-name")
        except:
            smartphone_specifications = None


        ###To get the Old Price
        try:
            old_div =  soup.find("div", attrs = {"class" : "old"})
            old_div_raw = old_div.text
            smartphone_old_price = int(old_div_raw.lstrip("₦ ").replace("," , ""))
        except:
            smartphone_old_price = None
            
        ###To get the New price
        try:
            new_div = soup.find("div", attrs = {"class" : "prc"})
            new_div_raw = new_div.text
            smartphone_new_price = int(new_div_raw.lstrip("₦ ").replace("," , ""))
        except:
            smartphone_new_price = None

        ###To get the discount
        try:
            discount_div = soup.find("div", attrs = {"class" : "tag _dsct _sm"})
            smartphone_discount = discount_div.text
        except:
            smartphone_discount = None

        ###To get the rating
        try:
            rating_div = soup.find("div", attrs = {"class" : "stars _s" })
            rating_phrase = rating_div.text
            smartphone_rating = float(rating_phrase.split(" ")[0])
        except:
            smartphone_rating = None


        entire_data.append([index, smartphone_brand_name, smartphone_specifications, smartphone_old_price, smartphone_new_price, smartphone_discount, smartphone_rating])
        index += 1

pen.writerows(entire_data)
new_file.close()
    





