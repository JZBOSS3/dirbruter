import requests
import sys
import socket
from colorama import Fore, Style
from datetime import datetime

verbose = False
quiet = False
write = False
write_file_name = ''
directories_file = ''
base_url = ''
wrote_target = False

def print_banner():
    print(Fore.YELLOW + '-'*50 + Style.RESET_ALL)
    print(Fore.RED + "Usage: script.py [options] <url> -f <directories_file>" + Style.RESET_ALL)
    print(Fore.MAGENTA + 'Options:' + Style.RESET_ALL)
    print(Fore.WHITE + '-h\tDisplay Help Menu' + Style.RESET_ALL)
    print(Fore.WHITE + '-f\tSpecify File Containing List of Directories' + Style.RESET_ALL)
    print(Fore.WHITE + '-v\tVerbose Mode' + Style.RESET_ALL)
    print(Fore.WHITE + '-q\tQuiet Mode' + Style.RESET_ALL)
    print(Fore.WHITE + '-o\tOutput To File' + Style.RESET_ALL)
    print(Fore.YELLOW + '-'*50 + Style.RESET_ALL)

def file_exists(arguments):
    exists = False
    for argument in arguments:
        if argument == '-f':
            exists = True
    return exists

def checkArguments(arguments):
    if len(arguments) < 3:
        print_banner()
        sys.exit()
    if not file_exists(arguments):
        print_banner()
        sys.exit()
    i = 0
    global verbose, quiet, write, directories_file, base_url, write_file_name
    for arg in arguments:
        if arg == '-h':
            print_banner()
            sys.exit()
        elif arg == '-v':
            verbose = True
        elif arg == '-q':
            quiet = True
        elif arg == '-o':
            write = True
            write_file_name = arguments[i + 1]
        elif arg == '-f':
            directories_file = arguments[i + 1]
        elif arg.startswith('https:') or arg.startswith('http:'):
            base_url = arguments[i]
        i += 1

def print_ip_target(target):
    target = target.split('www.')
    return socket.gethostbyname(target[1])
    

def print_top():
    print(Fore.YELLOW + '-'*50 + Style.RESET_ALL)
    print(Fore.BLUE + f'\tStarted Scanning Target: {base_url}/' + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + f'\tTarget IP Address: {print_ip_target(base_url)}' + Style.RESET_ALL)
    file = directories_file.split('\\')
    print(Fore.MAGENTA + f'\tUsed File: {file[len(file) - 1]}' + Style.RESET_ALL)
    print(Fore.GREEN + "\tTime Started " + str(datetime.now()) + Style.RESET_ALL)
    print(Fore.YELLOW + '-'*50 + Style.RESET_ALL)

   
def write_file(url, msg):
    try:
        with open(write_file_name, mode='a') as file:
            global wrote_target
            if not wrote_target:
                file.write('-'*50 + '\n')
                file.write(f'\tStarted Scanning Target: {base_url}/' + '\n')
                file.write(f'\tTarget IP Address: {print_ip_target(base_url)}' + '\n')
                dir_file = directories_file.split('\\')
                file.write(f'\tUsed File: {dir_file[len(dir_file) - 1]}' + '\n')
                file.write("\tTime Started " + str(datetime.now()) + '\n')
                file.write('-'*50 + '\n')
                wrote_target = True

            file.write(f'{url}{msg}\n')
    except IOError:
        print('Error Writing To The File... Try Again!')
    except Exception as e:
        print(f'Exception: {e}')

arguments = sys.argv
checkArguments(arguments)
print_top()

try:
    with open(directories_file, mode='r') as file:
        for line in file:
            directory = line.strip()
            url = f"{base_url}/{directory}"
            response = requests.get(url)
            if not quiet:
                if response.status_code == 200:
                    print(Fore.GREEN + f'{url}: Code 200' + Style.RESET_ALL)
                    if write:
                        write_file(url, ': Code 200')
                if verbose:    
                    if response.status_code == 301:
                        print(Fore.LIGHTBLACK_EX + f'{url}: Code 301' + Style.RESET_ALL)
                        if write:
                            write_file(url, ': Code 301')
                    elif response.status_code == 404:
                        print(Fore.RED + f'{url}: Code 404' + Style.RESET_ALL)
                        if write:
                            write_file(url, ': Code 404')
                    else:
                        print(Fore.LIGHTYELLOW_EX + f'{url}: Code {response.status_code}' + Style.RESET_ALL)
                        if write:
                            write_file(url, ': Code ' + str(response.status_code))
            else:
                if write:
                    write_file(url, ': Code ' + str(response.status_code))

except FileNotFoundError:
    print(f"Error: File '{directories_file}' not found.")
except requests.RequestException as e:
    print(f"Error: An error occurred with the request: {e}")
except KeyboardInterrupt:
    print('Exiting Program...')
except Exception as e:
    print(f"An unexpected error occurred: {e}")