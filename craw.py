import sys, json, urllib.request
from urllib.request import urlopen
import re, os.path, threading
from threading import Thread

base_url = "http://magic.wizards.com/en/see-more-wallpaper?page={page}&filter_by=DESC&artist=-1&expansion=&title="

def get_url(page):
    return base_url.format(page=page)

def read(url):
    u = urlopen(url)
    contents = u.read()
    return json.loads(contents.decode())

def load_wallpaper_links(current_url):
    contents = read(current_url)['data']
    wallpaper_links = re.findall(r'(?<=download=\")(http\S*2560x1600\S*\.jpg)', contents, re.MULTILINE)

    if(wallpaper_links == []):
        wallpaper_links = re.findall(r'(?<=download=\")(http\S*1920x1080\S*\.jpg)', contents, re.MULTILINE)

    if(wallpaper_links == []):
        wallpaper_links = re.findall(r'(?<=download=\")(http\S*1280x960\S*\.jpg)', contents, re.MULTILINE)

    return wallpaper_links

def download_files(wallpaper_links):
    allowed_threads = 5
    for wallpaper in wallpaper_links:
        while(threading.activeCount() > allowed_threads):
            time.sleep(5)
        th = Thread(target=download_file, args=(wallpaper,))
        th.start()

def download_file(wallpaper):
    file_name = "wallpapers/" + wallpaper.split("/")[-1]
    if not os.path.isfile(file_name):
        print("downloading > " + wallpaper)
        urllib.request.urlretrieve(wallpaper, file_name)

def start():
    for page in range(0, 110):
        url = get_url(page)
        wall_paper_urls = load_wallpaper_links(url)
        download_files(wall_paper_urls)

start()