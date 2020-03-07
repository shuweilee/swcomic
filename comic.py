#!/usr/bin/python -tt

import json
import requests
import time
import webbrowser
import argparse
from sys import exit


def create_browser(browser, path):
    if browser == 'chrome':
        return webbrowser.Chrome(path)
    if browser == 'firefox':
        return webbrowser.Mozilla(path)

    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("browser")
    parser.add_argument("tmp_col_file")
    parser.add_argument("col_file")

    args = parser.parse_args()

    browser_path = args.browser
    browser_name = browser_path.split('/')[-1]
    browser_obj = create_browser(browser_name, browser_path)

    tmp_col_file = args.tmp_col_file
    col_file = args.col_file

    if False == browser_obj:
        exit(1)

    modified = False
    with open(tmp_col_file) as f:
        comics = json.load(f)
    
    read_list = []
    
    print('check')
    
    for comic in comics:
        protocol = 'https://'
        domain = 'www.comicbus.com'
        path = '/html'
        resource = '/' + str(comic['comic_id']) + '.html'
        url = protocol + domain + path + resource
        response = requests.get(url, verify=True)
    
        while(True):
            pattern = str(comic['comic_id']) + '-' + \
                str(comic['newest'] + 1) + '.html'
            if response.content.find(bytes(pattern, 'utf-8')) == -1:
                break
    		#print(comic['name'].encode('utf8') + ' is not updated.')
            else:
                comic['newest'] = comic['newest'] + 1
                print('[updated]' + str(comic['name']) + '[' + str(comic['newest']) + '] is now available.')
                modified = True
                open_url = 'http://v.comicbus.com/online/comic-' + \
                    str(comic['comic_id']) + '.html?ch=' + \
                    str(comic['newest']) + ''
                read_list.append(open_url)
                #browser_obj.open_new_tab(open_url)
    
    if modified == True:
        with open(col_file, 'w') as f:
            f.write(json.dumps(comics, indent=4))
        modified = False
    print('END')
