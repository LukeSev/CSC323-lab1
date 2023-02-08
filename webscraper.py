import requests
from lxml import html
from bs4 import BeautifulSoup

URL = "http://localhost:8080/forgot"
page = requests.get(URL)
bs = BeautifulSoup(page.content, "html.parser")
results = bs.find(id="centerContainer")
print(results.prettify())
