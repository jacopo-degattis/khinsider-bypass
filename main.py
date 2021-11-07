import os
import time
import requests
from bs4 import BeautifulSoup

def download(uri=None, quality="mp3"):
    website = requests.get(uri)
    soup = BeautifulSoup(website.content, "html.parser")
    table = soup.find("table", {"id": "songlist"})
    track_list = table.find_all("tr")
    for track in track_list[1:-1]:
        # print(track)
        url = "https://downloads.khinsider.com{}"
        track_uri = track.find_all("a")[0]["href"]
        track_name = track.find_all("td")[2].text
        track_page = requests.get(url.format(track_uri))
        page_scraper = BeautifulSoup(track_page.content, "html.parser")
        download_url = page_scraper.find("span", {"class": "songDownloadLink"})
        download_url = str(download_url.parent["href"]).replace(".mp3", ".{}".format(quality))
        folder_name = uri.split("/")[-1].replace("-", " ").capitalize()
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        with open(os.path.join(folder_name, track_name + ".flac"), "wb") as output_file:
            print("[!] Saving track {}".format(track_name), "\r")
            track_bytes = requests.get(download_url).content
            output_file.write(track_bytes)
            print("[+] Track {} saved succesfully !".format(track_name), "\r")
            time.sleep(0.5)
        
if __name__ == "__main__":
    format = input("Download quality (flac, mp3): ")
    
    if not format in ["mp3", "flac"]:
        print("You have to specify either MP3 or FLAC")
        # TODO: add fallback to mp3
        exit(-1)
    
    uri = input("Paste the url you want to download track from: (ex. https://downloads.khinsider.com/game-soundtracks/album/red-dead-redemption-2-original-soundtrack): ")
    
    if uri:
        download(uri, format)
    else:
        print("You must specify a valid URL")
