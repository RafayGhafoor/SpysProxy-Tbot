import requests
import bs4
import re

enctab = dict()

def scrape_page(url='http://spys.one/en/socks-proxy-list/', soup='n'):
	'''
	Scrape given link and create a beautiful soup object.
	- url:  Url to scrape.
	- soup: "n" to not create soup object and only return request response.
	'''
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	try:
	    request_url = requests.get(url, headers=headers)

	    if request_url.status_code == 401:
	        sys.exit("Username or Password is incorrect.")

	    elif request_url.status_code == 200:
	        if soup == 'y':
	            html_soup = bs4.BeautifulSoup(request_url.content, 'lxml')
	            return html_soup
	        return request_url

	except requests.exceptions.ConnectionError:
	    print("Internet Connection Down.\nExiting...")
	    sys.exit()


# Taken from https://github.com/xanderdin/scrape.spys.one.proxies :)
def fill_enctab(arg):
    '''
    Fill enctab with values from the script
    with encoding values.

    @arg - script body
    '''
    plain_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 4]
    for v in plain_values:
        enctab[v[0]] = int(v[1])
    other_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 6]
    for v in other_values:
        (a, b) = v[1].split('^')
        enctab[v[0]] = int(a) ^ enctab[b]


def calc_port(script):
    port = ''
    port_parts = re.findall('\+\(([a-z0-9^]+)\)+', script)
    for part in port_parts:
        (a, b) = part.split('^')
        port += str(enctab[a] ^ enctab[b])
    return port


def get_proxy_info(proxies_num=5):
	soup = scrape_page(soup='y')
	arg = soup.body.find('script', attrs={'type': "text/javascript"}).text.split(';')
	fill_enctab(arg) # Fills Encoding Tabs ^
	data = []
	proxy_info = {'ip': [], 'port': [], 'country': []}
	counter = 0

	for i, info in enumerate(soup.findAll('td', attrs={"colspan": "1"}), 1):
		info = info.find('font', class_='spy14')

		if info:
			if counter == proxies_num:
				return proxy_info

			elif i % 3 == 0:
				proxy_info['ip'].append(data[0])
				proxy_info['country'].append(data[1])
				data = []
				counter += 1

			elif info.contents:
				if len(info.contents) == 2:
					proxy_info['port'].append(calc_port(str(info.contents[-1])))
				data.append(info.contents[0])
	return proxy_info
