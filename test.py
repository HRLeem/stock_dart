import urllib.request
from bs4 import BeautifulSoup
import requests

url = "https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=701"
resp = requests.get(url)
html = resp.text
print(html)
# if resp.status_code == 200:
#     soup = BeautifulSoup(html, 'html.parser')
#     list = soup.select('table', id_="highlight_D_A")
#     print(list)
# else:
#     print(18181818)