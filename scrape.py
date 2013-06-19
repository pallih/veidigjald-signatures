import scraperwiki
import requests
import lxml.html

url = 'http://www.petitions24.com/signatures/obreytt_veidigjald/start/%s'
headers = {'User-Agent': 'Mozilla/5.0'}

#setup at start
'''
record = {}
record['last_page'] = '0'
scraperwiki.sqlite.save(['last_page'], data=record, table_name='runtime_info')
exit()
'''

selection_statement = 'last_page from runtime_info'
last_page = int(scraperwiki.sqlite.select(selection_statement)[0]['last_page'])

s = requests.Session()
s.headers.update(headers)


def scrape(last_page):
    print last_page
    response = s.get(url % str(int(last_page)*10).strip())
    html = response.text
    root = lxml.html.fromstring(html)
    signatures = root.xpath('//table[@id="signatures"]/tr')
    batch = []
    for signature in signatures:
        data = {}
        data['nr'] = signature[0].text_content().strip()
        data['name'] = signature[1].text_content()
        if data['name'] != 'The signatory decided not to show his/her name on the Internet.':
            data['place'] = signature[2].text_content()
            data['place_url'] = signature[2][0].attrib['href']
            data['kt'] = signature[3].text_content()
            data['date'] = signature[4].text_content()
        batch.append(data)
    scraperwiki.sqlite.save(['nr'], data=batch, table_name='veidigjald')
    update_statement= 'update runtime_info SET last_page=' + str(last_page)
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    pagination = root.xpath('//div[@class="pagination"]/a[@class="go_next"]')
    if pagination:
        return True
    else:
        return False

for x in range(last_page,10000000): # How crappy is this? Probably 11.
    result = scrape(x)
    if result != False:
        x = x +1
    else:
        break
