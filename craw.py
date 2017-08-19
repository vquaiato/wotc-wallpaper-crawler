import sys, json, urllib.request, time
from urllib.request import urlopen
import re, os.path, threading
from threading import Thread

base_url = "http://magic.wizards.com/en/see-more-wallpaper?page={page}&filter_by=DESC&artist=-1&expansion=&title="
wanted_wallpaper_resolution_patterns = [r'(?<=download=\")(http\S*2560x1600\S*\.jpg)',r'(?<=download=\")(http\S*1920x1080\S*\.jpg)', r'(?<=download=\")(http\S*1280x960\S*\.jpg)']

def get_url_for_page_index(page_index):
    return base_url.format(page=page_index)

def load_json_from(url):
    u = urlopen(url)
    contents = u.read()
    return json.loads(contents.decode())

def has_data_in(json_data):
    return json_data != ""

def load_wallpaper_links(json_data):
    wallpaper_links = []

    for pattern in wanted_wallpaper_resolution_patterns:
        if(wallpaper_links == []):
            wallpaper_links = re.findall(pattern, json_data, re.MULTILINE)

    return wallpaper_links

def init_images_downloads_for(wallpaper_links):
    allowed_threads = 5
    for wallpaper in wallpaper_links:
        while(threading.activeCount() > allowed_threads):
            time.sleep(2)
        th = Thread(target=download_file, args=(wallpaper,))
        th.start()

def download_file(wallpaper):
    file_name = "wallpapers/" + wallpaper.split("/")[-1]
    if not os.path.isfile(file_name):
        print("⏬  " + wallpaper)
        urllib.request.urlretrieve(wallpaper, file_name)

def start():
    page = 0
    while True:
        url = get_url_for_page_index(page)
        json_data = load_json_from(url)['data']
        
        if not has_data_in(json_data):
            break

        wallpaper_urls = load_wallpaper_links(json_data)
        init_images_downloads_for(wallpaper_urls)
        page +=1

start()
