import sys
import socket
import requests
from colorama import Fore, Style

domain = ""
domains_file = ""
directories_file = "big.txt"

s200 = []  # 200 OK
s301 = []  # 301 Moved Permanently
s403 = []  # 403 Forbidden
s404 = []  # 404 Not Found
s405 = []  # 405 Method Not Allowed
s500 = []  # 500 Internal Server Error

html_ascii_title = r'''
────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─────────██████─██████████████████─██████████████───██████████████─██████████████─██████████████─██████████████─
─────────██░░██─██░░░░░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
─────────██░░██─████████████░░░░██─██░░██████░░██───██░░██████░░██─██░░██████████─██░░██████████─██████████░░██─
─────────██░░██─────────████░░████─██░░██──██░░██───██░░██──██░░██─██░░██─────────██░░██─────────────────██░░██─
─────────██░░██───────████░░████───██░░██████░░████─██░░██──██░░██─██░░██████████─██░░██████████─██████████░░██─
─────────██░░██─────████░░████─────██░░░░░░░░░░░░██─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
─██████──██░░██───████░░████───────██░░████████░░██─██░░██──██░░██─██████████░░██─██████████░░██─██████████░░██─
─██░░██──██░░██─████░░████─────────██░░██────██░░██─██░░██──██░░██─────────██░░██─────────██░░██─────────██░░██─
─██░░██████░░██─██░░░░████████████─██░░████████░░██─██░░██████░░██─██████████░░██─██████████░░██─██████████░░██─
─██░░░░░░░░░░██─██░░░░░░░░░░░░░░██─██░░░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
─██████████████─██████████████████─████████████████─██████████████─██████████████─██████████████─██████████████─
────────────────────────────────────────────────────────────────────────────────────────────────────────────────
'''

# Function to generate the ASCII logo
def print_ascii():
    ascii_txt = r'''
██████████████████████████████████████████████████████
█▄─▄▄▀█▄─▄█▄─▄▄▀█▄─▄─▀█▄─▄▄▀█▄─██─▄█─▄─▄─█▄─▄▄─█▄─▄▄▀█
██─██─██─███─▄─▄██─▄─▀██─▄─▄██─██─████─████─▄█▀██─▄─▄█
▀▄▄▄▄▀▀▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▀▄▄▀▀▄▄▄▄▀▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀'''
    print(Fore.GREEN + ascii_txt + Style.RESET_ALL)

# Function to print the help menu
def print_help_menu():
    print(Fore.BLUE + 40*'*' + Style.RESET_ALL)
    print(Fore.RED + 'Usage python3 dirbruter.py -d example.com' + Style.RESET_ALL)
    print(Fore.BLUE + 40*'*' + Style.RESET_ALL)
    print(Fore.YELLOW + "Flags:" + Style.RESET_ALL)
    print("-d\tDomain to brute force")
    print("-df\tFile containing Domains to brute force")
    print("-f\tFile Containing directories")
    print("-h\tPrint help menu")
    print('')
    sys.exit()

# Check if the domain is alive
def web_alive(domain):
    return requests.get(f'https://{domain}').status_code == 200 or requests.get(f'http://{domain}').status_code == 200

# Scan the domain for directories
def scan_domain(domain, directory_file):
    global s200, s301, s403, s404, s405, s500
    if not web_alive(domain):
        print(f"{Fore.RED}[!] {domain} is not alive{Style.RESET_ALL}")
    else:
        try:
            with open(directory_file, mode='r') as directories:
                for directory in directories:
                    url = f'https://{domain}/{directory.strip()}'
                    response = requests.get(url)
                    sc = response.status_code
                    if sc == 200:
                        s200.append(url)
                        print(Fore.GREEN + f'[!]{sc} Found: {url}' + Style.RESET_ALL)
                    elif sc == 301:
                        s301.append(url)
                    elif sc == 403:
                        s403.append(url)
                        print(Fore.RED + f'[!]{sc} Forbidden: {url}' + Style.RESET_ALL)
                    elif sc == 404:
                        s404.append(url)
                        print(Fore.RED + f'[!]{sc} Not Found: {url}' + Style.RESET_ALL)
                    elif sc == 405:
                        s405.append(url)
                    elif sc == 500:
                        s500.append(url)
        except FileNotFoundError:
            print(f"{Fore.RED}[!] {directory_file} not found{Style.RESET_ALL}")

# Function to generate the HTML page
def generate_html_page(domain):
    # HTML report template
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Scan Report</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 80%;
            margin: 30px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        h1 {{
            text-align: center;
            color: #4CAF50;
        }}
        .scan-results {{
            font-size: 1em;
            line-height: 1.6;
        }}
        .status-group {{
            margin-bottom: 20px;
            padding-left: 20px;
        }}
        .status-group h3 {{
            color: #333;
        }}
        .status-group ul {{
            list-style-type: none;
            padding: 0;
        }}
        .status-group li {{
            padding: 5px;
        }}
        h3 {{
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <p style="font-size: .5rem; width: 50%; margin: 0 auto;" align="center">{html_ascii_title}</p>
        <div class="scan-results">
            <div class="status-group">
                <h3 style="border-left: 5px solid green;">200 OK</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s200])}
                </ul>
            </div>
            <div class="status-group">
                <h3 style="border-left: 5px solid blue;">301 Moved Permanently</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s301])}
                </ul>
            </div>
            <div class="status-group">
                <h3 style="border-left: 5px solid orange;">403 Forbidden</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s403])}
                </ul>
            </div>
            <div class="status-group">
                <h3 style="border-left: 5px solid red;">404 Not Found</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s404])}
                </ul>
            </div>
            <div class="status-group">
                <h3 style="border-left: 5px solid yellow;">405 Method Not Allowed</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s405])}
                </ul>
            </div>
            <div class="status-group">
                <h3 style="border-left: 5px solid purple;">500 Internal Server Error</h3>
                <ul>
                    {"".join([f"<li>{url}</li>" for url in s500])}
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

    # Write HTML content to a file with utf-8 encoding
    with open(f"{(domain.split('.')[0])}_scan_report.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print(Fore.GREEN + f"HTML Report has been generated: {(domain.split('.')[0])}_scan_report.html" + Style.RESET_ALL)

# Main function to run the tool
def run_tool():
    global domain, domains_file, directories_file
    flags = ['-h', '-f', '-d', '-df']
    args = sys.argv[1:]

    if len(args) < 2:
        print_help_menu()
    else:
        skip_next = False
        for i, arg in enumerate(args):
            if skip_next:
                skip_next = False
                continue

            if arg not in flags:
                print_help_menu()
            else:
                if arg == '-d':
                    domain = args[i + 1]
                    skip_next = True
                elif arg == '-df':
                    domains_file = args[i + 1]
                    skip_next = True
                elif arg == '-f':
                    directories_file = args[i + 1]
                    skip_next = True

        print(Fore.GREEN + 'Starting Scan...' + Style.RESET_ALL)

        try:
            if domain:
                print(Fore.CYAN + f'Scanning {domain}\tIP: {socket.gethostbyname(domain.replace("www.", ""))}' + Style.RESET_ALL)
        except socket.gaierror:
            print(Fore.RED + "Domain name could not be resolved." + Style.RESET_ALL)
            sys.exit()

        if domain and not domains_file:
            scan_domain(domain, directories_file)
            generate_html_page(domain.strip())
        elif not domain and domains_file:
            with open(domains_file, mode='r') as file:
                for domain in file:
                    scan_domain(domain.strip(), directories_file)
                    generate_html_page(domain.strip())
        else:
            print_help_menu()

if __name__ == "__main__":
    try:
        print_ascii()
        run_tool()
    except KeyboardInterrupt:
        generate_html_page()
        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
