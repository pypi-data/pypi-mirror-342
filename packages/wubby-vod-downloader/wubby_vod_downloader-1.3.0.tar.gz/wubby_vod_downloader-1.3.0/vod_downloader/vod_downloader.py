import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import argparse

# Base URL of the VOD archive
base_url = "https://archive.wubby.tv/vods/public/"

# Function to get the list of months sorted by timestamp
def get_sorted_months():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all directories (these are links to the month folders)
    month_links = []
    for row in soup.find_all('tr'):
        link = row.find('a', href=True)
        if link and 'title' in link.attrs:
            timestamp = row.find_all('td')[2].text.strip()
            if timestamp:
                # Parse the timestamp into a datetime object
                try:
                    timestamp = datetime.strptime(timestamp, "%Y-%b-%d %H:%M")
                    month_links.append((link['title'], timestamp))
                except ValueError:
                    continue  # Skip any entries that don't have a valid timestamp
    # Sort months by timestamp (descending order)
    sorted_months = sorted(month_links, key=lambda x: x[1], reverse=True)
    return sorted_months

# Function to get and sort VODs by timestamp within a month folder
def get_sorted_vods(month_folder,kickonly,twitchonly):
    month_url = base_url + month_folder + "/"
    response = requests.get(month_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all VOD links and their timestamps
    vod_links = []
    for row in soup.find_all('tr'):
        link = row.find('a', href=True)
        if link and link['href'].endswith('.mp4'):
            # Get the VOD timestamp (the date part) for sorting
            timestamp = row.find_all('td')[1].text.strip()
            timestamp = timestamp.strip(r"[a-zA-Z]")
            if timestamp:
                try:
                    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
                    if (kickonly):
                        if 'kickapilol' in link['href']:
                            vod_links.append((link['href'], timestamp))
                    elif (twitchonly):
                        if 'kickapilol' not in link['href']:
                            vod_links.append((link['href'], timestamp))
                    else:
                        vod_links.append((link['href'], timestamp))
                except ValueError:
                    continue  # Skip any entries that don't have a valid timestamp

    # Sort VODs by timestamp (descending order)
    sorted_vods = sorted(vod_links, key=lambda x: x[1], reverse=True)
    return sorted_vods

# Function to download VODs from the most recent month
def download_vods(month_folder, count=5, kickonly=False, dlfolder='vod_downloads',twitchonly=False):
    sorted_vods = get_sorted_vods(month_folder,kickonly,twitchonly)

    # comment these in to test fetch without actual download
    # print(sorted_vods)
    # return

    if not sorted_vods:
        print(f"No VODs found in the month folder: {month_folder}")
        return

    print(dlfolder)
    # Create a folder for the downloads if it doesn't exist
    download_folder = dlfolder
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Initialize a progress bar with `tqdm`
    for i, (vod_link, _) in enumerate(tqdm(sorted_vods[:count], desc="Downloading VODs", unit="VOD", dynamic_ncols=True)):
        vod_url = base_url + month_folder + "/" + vod_link
        ymd=sorted_vods[:count][0][1].strftime('%Y-%m-')
        vod_filename = os.path.join(download_folder,ymd+vod_link.split('/')[-1])

        # Check if the VOD has already been downloaded
        if os.path.exists(vod_filename):
            print(f"Skipping {vod_filename}, already downloaded.")
            continue  # Skip this VOD if it already exists

        print(f"Downloading VOD {i+1}: {vod_url} to {vod_filename}")
        # return
        response = requests.get(vod_url, stream=True)
        
        # Save the VOD to a file with progress
        with open(vod_filename, 'wb') as f:
            total_length = int(response.headers.get('content-length', 0))
            if total_length == 0:
                f.write(response.content)
            else:
                for chunk in tqdm(response.iter_content(chunk_size=8192), total=total_length // 8192, unit='B', unit_scale=True, leave=False):
                    f.write(chunk)
        print(f"Downloaded {vod_filename}")

# Command line interface setup
def main():
    parser = argparse.ArgumentParser(description="Download VODs from the Wubby TV archive.")
    parser.add_argument('month_folder', help='The folder name of the month to download VODs from')
    parser.add_argument('-c', '--count', nargs='?', default=1, type=int, help='Number of VODs to download (default: 5)')
    parser.add_argument('-dlf', nargs='?', default='vod_downloads', help='The folder name to download to.')
    parser.add_argument('-k', '--kick', action='store_true', help='Kick Vods Only')
    parser.add_argument('-t', '--twitch', action='store_true', help='Twitch Vods Only')
    args = parser.parse_args()
    
    download_vods(args.month_folder, count=args.count, dlfolder=args.dlf, kickonly=args.kick, twitchonly=args.twitch)

if __name__ == "__main__":
    main()