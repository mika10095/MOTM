import requests
from bs4 import BeautifulSoup
def scrape_motm():
    response = requests.get('https://pdb101.rcsb.org/motm/motm-image-download')
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table')
    if table:
        for row in table.find_all('tr'):
            testing = row.find_all('a')
            if testing:
                id = testing[1].text.strip()
                if id:
                    return(testing[1].text.strip() +";"+ testing[2].text +";"+ testing[3].get('href'))
def download_tif(link):
    print("Downloading tif")
    response = requests.get(link, allow_redirects=True)
    open('MOTD.tif', 'wb').write(response.content)
    print("Downloaded tif")
def main():
    print("hello world")
    motd = scrape_motm()
    if motd:
        print(motd)
        download_tif(motd.split(";")[2])

main()