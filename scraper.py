import requests
import bs4

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get('http://spys.one/en/socks-proxy-list/', headers=headers)
soup = bs4.BeautifulSoup(r.content, 'lxml')
# print(soup.prettify())

for info in soup.findAll('td', attrs={"colspan": "1"}):
	# print(info.find('font', class_='spy14'))
	s = info.find('font', class_='spy1')
	if s:
		print(s.text)
	input()