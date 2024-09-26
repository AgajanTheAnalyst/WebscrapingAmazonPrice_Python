from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

"""
Web scraping the price of the item
"""

link = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

response = requests.get(link)
text = response.text

soup = BeautifulSoup(text, 'html.parser')
price_in_website = float(79.95)
price = soup.find_all('span', class_='a-offscreen')
price_float = None
for i in range(len(price)):
    try:
        price_value = float(price[i].get_text().replace('$', '').replace(',', ''))
        if price_value == price_in_website:
            price_float = price_value
            break
    except ValueError:
        continue

title = soup.find('span', id="productTitle").text.replace("  "," ")


"""
Sending an email to us, if the price our cooker gets cheaper than our target price.
"""

target = float(90)

smtp_gmail = os.getenv("SMTP_ADDRESS")
sender_email = os.getenv("EMAIL")
receiver = os.getenv("RECEIVER")
password = os.getenv("PASSWORD")
message = f"{title} is now ${price_float} \n {link}"
message = message.encode("utf-8")
if price_float <= target:
    with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), port=587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr = sender_email,
            to_addrs = receiver,
            msg = message
        )

