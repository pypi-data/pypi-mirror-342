# Wubby VOD Downloader (aka Wubby Snatch)

A simple script to snatch those autism VODs from the Wubby TV archive, for when you need to grab the best of the chaos.

## Install this ADHD-fueled masterpiece

Install this package from PyPI using `pip`:

```bash
pip install wubby-vod-downloader==1.2.0
```

## Usage

Navigate to the directory where you want to store your VODs. By default, the script will create a new folder named `vod_downloads` where the files will be saved.

Run the command to download your desired VODs:

```bash
wubby-snatch month -c <number_of_vods>
```

## Arguments

Month: Specify the month in `MMM_YYYY` format (e.g., `mar_2025`) from which you want to download VODs.

-c <number_of_vods> (optional): Specify how many VODs you want to download. For example, `-c 5` to download the 5 most recent VODs. Default is 1.

-dlf <path to folder> (optional): Specify the full file path of where to download VODs. If not specified, will revert to default.

-k (optional): Kick Streams Only

-t (optional): Twitch Streams Only

## Examples

```bash
wubby-snatch mar_2025 -c 5
```
This will download the 5 most recent VODs from March 2025.

```bash
 wubby-snatch apr_2025 -c 6 -dlf "V:\Stream VODs" -k
```
This will download the 6 most recent Kick VODs from April, 2025 to "V:\Stream VODs".

## Skipping Already Downloaded VODs

The script will check if VODs have already been downloaded and skip them

## Important

After installing via pip, if you get a warning about `wubby-snatch` not being in PATH, you can add `~/.local/bin` to your PATH manually.

This typically happens on Linux systems. You can add it by running:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this line to the end of your .`bashrc` or `.zshrc` file to make it permanent.

License
This project is licensed under the MIT License - see the LICENSE file for details if you care.
