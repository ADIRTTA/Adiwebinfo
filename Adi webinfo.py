import os
import re
import requests

# Define colors for terminal
Black = "\033[1;90m"
Red = "\033[1;91m"
Green = "\033[1;92m"
Yellow = "\033[1;93m"
Blue = "\033[1;94m"
Purple = "\033[1;95m"
White = "\033[1;97m"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""
      {Red}        ___    ____  ________  _______________
            /   |  / __ \/  _/ __ \/_  __/_  __/   |
           / /| | / / / // // /_/ / / /   / / / /| |
          / ___ |/ /_/ // // _, _/ / /   / / / ___ |       THANK YOU FOR USING MY TOOL❤️
         /_/  |_/_____/___/_/ |_| /_/   /_/ /_/  |_|
    """)
    print(f"\n{White}     A web scraper to get emails and phone numbers from websites      \n")
    print(f"{Blue}                Developed by: {Red}ADIRTTA\n\n\n")

def is_valid_url(url):
    url_validity = re.compile(r'(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]')
    return re.match(url_validity, url)

def email_scraping(content):
    emails = set(re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', content, re.I))
    if emails:
        print(f"{White}[{Yellow}*{White}] {Yellow}Emails found:{White}")
        with open('email.txt', 'w') as file:
            for email in emails:
                print(email)
                file.write(f'{email}\n')
    else:
        print(f"{White}[{Red}!{White}] {Red}No Emails found")

def phone_scraping(content):
    # Adjusted regex to capture various phone number formats
    phones = set(re.findall(r'?\+?[0-9]*?[-.\s]?[0-9]+[-.\s]?[0-9]+[-.\s]?[0-9]+', content))
    if phones:
        print(f"{White}[{Yellow}*{White}] {Yellow}Phone numbers found:{White}")
        with open('phone.txt', 'w') as file:
            for phone in phones:
                print(phone)
                file.write(f'{phone}\n')
    else:
        print(f"{White}[{Red}!{White}] {Red}No phone numbers found")

def output():
    folder_name = input(f'{White}[{Green}*{White}] {Green}Enter folder name : {White}')
    if os.path.exists(folder_name):
        print(f"{White}[{Red}!{White}] {Red}Folder already exists")
        output()
    else:
        os.mkdir(folder_name)
        if os.path.exists('email.txt'):
            os.rename('email.txt', f'{folder_name}/email.txt')
        if os.path.exists('phone.txt'):
            os.rename('phone.txt', f'{folder_name}/phone.txt')
        print(f"{White}[{Green}*{White}] {Yellow}Output saved")
    print(f"{White}[{Red}!{White}] {Red}Exiting....\n")

def check_internet():
    print(f"{White}[{Red}!{White}] {Red}Checking internet connection")
    try:
        requests.get('http://google.com', timeout=3)
        print(f"{White}[{Yellow}*{White}] {Yellow}Connected")
    except requests.ConnectionError:
        print(f"{White}[{Red}!{White}] {Red}No internet, try later")
        exit()

def main():
    banner()
    check_internet()

    url = input(f'{White}[{Green}*{White}] {Green}Enter URL to begin : {White}')
    if is_valid_url(url):
        email = input(f'{White}[{Green}*{White}] {Green}Scrape emails from website (y/n) : {White}')
        phone = input(f'{White}[{Green}*{White}] {Green}Scrape phone numbers from website (y/n) : {White}')
        if email.lower() == 'y' or phone.lower() == 'y':
            print(f"{White}[{Red}!{White}] {Red}Scraping started")
            scraper(url, email, phone)
        else:
            print(f"{White}[{Red}!{White}] {Red}Exiting....\n")
    else:
        print(f"{White}[{Red}!{White}] {Red}Invalid URL, please check again")
        main()

def scraper(url, email, phone):
    try:
        response = requests.get(url)
        content = response.text
    except requests.exceptions.RequestException as e:
        print(f"{White}[{Red}!{White}] {Red}Error: {str(e)}")
        return

    if email.lower() == 'y':
        email_scraping(content)

    if phone.lower() == 'y':
        phone_scraping(content)

    if os.path.exists('email.txt') or os.path.exists('phone.txt'):
        save_output = input(f'{White}[{Green}*{White}] {Green}Do you want to save the output (y/n) : {White}')
        if save_output.lower() == 'y':
            output()

    print(f"{White}[{Red}!{White}] {Red}Exiting....\n")
    if os.path.exists('email.txt'):
        os.remove('email.txt')
    if os.path.exists('phone.txt'):
        os.remove('phone.txt')

if __name__ == '__main__':
    clear()
    main()
