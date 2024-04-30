import requests
from bs4 import BeautifulSoup
import smtplib
import os

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
BUY_PRICE = 130

URL = "https://www.amazon.com/Bleach-Box-Set-Vol-1-21/dp/1421526107/ref=sr_1_1?crid=3RFPOKW63EXOJ&dib=eyJ2IjoiMSJ9.gb2c7xHvl4_pjZ_LMHc05A07C9pBebcNU-o7MLQUNJS7Jwby66DF1nFsn3DsPXBBg0tcDA6-eYwNlSSq8125C8AglP2OOfijss7vILUeftbfACUJgjaQgLwkysMqIGOi6bkbCS-ey70oOYmdUXcUaDgL9s7HiS_a70KxN92eTWQ6oeLVCHJ_yugxAqy-FQxcy2U8Xm8R0t8E5a49OTHOoLScqjVeJK0rBfHgeYN8-1s.dOLftQNF7BX8xzrttIk1dhDndLfpwKTDdIMz4uPQWIk&dib_tag=se&keywords=bleach+box+set&qid=1714507047&sprefix=bleach+bo%2Caps%2C129&sr=8-1"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Need to add some headers when using a get request on Amazon
response = requests.get(URL, headers=header)
item_page = response.text

soup = BeautifulSoup(item_page, "lxml")
product_title = soup.find(id="productTitle").get_text().strip() # Grab the product tile
float_price_item = float(soup.find(name="span", class_="a-offscreen").get_text().strip("$")) # Grab the product price

# If the current price is lower than your buy price then send an email
if float_price_item < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Change!!!\n\n{product_title} is now ${float_price_item}. \n{URL}".encode("utf-8")
        )

