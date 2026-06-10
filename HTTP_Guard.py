import requests
import sys
import colorama
colorama.init()
# color define
G = '\033[92m'#Green
R = '\033[91m'#Red
Y = '\033[93m'#Yellow
r = '\033[0m'#Reset

def check_url():
    parts = []
    url = input("Enter the URL: ")
    raw_parts = url.split("/")
    for raw in raw_parts: parts.append(raw+'/')
    if parts[0]=="http:/" or parts[0]=="https:/" or parts[0]=="ftp:/":
        print(G + "****************** Valid Url ******************" + r)
    else: print(R + "###############################\n#         Invalid Url         #\n###############################" + r); sys.exit()
    return url

def analyze_headers():
    url = check_url()
    # send request and get response
    print(Y + f"Connecting to {url} ....." + r)
    session = requests.Session()
    try:
        response = session.get(url,timeout=(10,60))
        header = response.headers
        # checking security headers
        security_header = [
            "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options",
            "X-XSS-Protection", "Strict-Transport-Security", "Referrer-Policy",
        ]
        print(Y + "Analyzing Headers..." + r)
        print("Headers: ")
        for i in security_header:
            if header.get(i) is None:
                print(R + f"⚠ Missing Header: {i}" + r)
            else:
                print(G + f"✔ Header: {i}" + r)
    except requests.exceptions.Timeout:
        print(R + "[!] Error: The server took too long to respond!" + r); sys.exit()
    except requests.exceptions.ConnectionError:
        print(R + "[!] Error: The server did not respond!" + r); sys.exit()
    except Exception as e:
        print(R + f"[!] An unexpected error occured: {e}" + r); sys.exit()


def file_downloader():
    url = check_url()
    raw_parts = url.split("/")
    file_name = raw_parts[-1]
    session = requests.Session()
    try:
        response = session.get(url,timeout=(10,60),stream=True)
        path = input("Enter the download path: ")
        print(Y + "Downloading .... " + r)
        with open(f"{path}/{file_name}", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(G + f"File: {file_name} (",response.headers.get("Content-Length")," bytes) Downloaded Successfully!" + r)
    except requests.exceptions.Timeout:
        print(R + "[!] Error: The server took too long to respond!" + r); sys.exit()
    except requests.exceptions.ConnectionError:
        print(R + "[!] Error: The server did not respond!" + r); sys.exit()
    except Exception as e:
        print(R + f"[!] An unexpected error occured: {e}" + r); sys.exit()

def source_downloader():
    url = check_url()
    session = requests.Session()
    try:
        response = session.get(url,timeout=(10,60),stream=True)
        path = input("Enter the download path: ")
        print(Y + "Downloading .... " + r)
        with open(f"{path}/index.html","w",encoding="utf-8") as f:
            f.write(response.text)
        print(G + "File Downloaded Successfully!" + r)
    except requests.exceptions.Timeout:
        print(R + "[!] Error: The server took too long to respond!" + r); sys.exit()
    except requests.exceptions.ConnectionError:
        print(R + "[!] Error: The server did not respond!" + r); sys.exit()
    except Exception as e:
        print(R + f"[!] An unexpected error occured: {e}" + r); sys.exit()

print("1. Website Security Check\n2. Download File\n3. Source Code Download\n--------------------------")
option = input("Enter your option: ")
if option == "1":
    analyze_headers()
elif option == "2":
    file_downloader()
elif option == "3":
    source_downloader()
else:
    print(R + "##################################\n#         Invalid Option         #\n##################################" + r); sys.exit()
