#!/usr/bin/python3
"""
Tool to automatically check the membership of a given username
in popular websites.
"""

import requests
import pandas as pd
import sys
import random
from termcolor import colored
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from pyfiglet import figlet_format
import json
import time
import urllib.request

def instruction():
    print()
    print()
    print("INSTRUCTION")
    print("Give a correct command line arguments")
    print("For search a single username give single argument like: single,one,1")
    print("for example 'python3 main.py single'")
    print("For search usernames from dataset give argument like multiple,dataset,more ")
    print("Also give a number; how many usernames want to search")
    print("For example 'python3 main.py dataset 3   '")
    print("If you fail to do so please try again with the above instructions")

def main():
    def banner(text, ch='=', length=78):
        spaced_text = ' %s ' % text
        banner = spaced_text.center(length, ch)
        print(banner)

    ascii_banner = figlet_format('Presence of Social Media Handle')
    print(ascii_banner)


    banner_text = "A platform Where A User can Find the Online Presence of Social Media Handle on Internet"
    banner(banner_text)
    most_count=0
    most_popular= ""
    if len(sys.argv)>1:
        if(sys.argv[1]=="single" or sys.argv[1]=="Single" or sys.argv[1]=="one" or sys.argv[1]=="1"):
            username= input("Enter username: ")
            FindPresence(username)
        elif(sys.argv[1]=="multiple" or sys.argv[1]=="dataset" or sys.argv[1]=="more"):
            data= pd.read_csv('username_dataset.csv')
            df = pd.DataFrame(columns = ['username_from_data'])
            # df= df.sample()
            df['username_from_data']= data['user_name_data']
            # print(data)
            row=int(sys.argv[2])
            for i in range(row):
                # print(df['username_from_data'][i])
                temp= FindPresence(df['username_from_data'][i])
                if(temp>most_count):
                    most_count=temp;
                    most_popular = df['username_from_data'][i]
            banner('completed')
            print("Overall Summary of all usernames")
            print("Most Popular username:: ",most_popular)
            print('User {} has membership in {}/{} websites'.format(most_popular,most_count, 40))
        else:
            instruction()

    else:
        instruction()
    banner('completed')

def FindPresence(user_taken):
    start_time = time.time()
    

    wiki_link = 'https://en.wikipedia.org/wiki/List_of_HTTP_status_codes'
    uname = user_taken
    width = 20  # to pretty print
    global counter
    counter = 0  # to count no of success
    page = requests.get(wiki_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    user_agent = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
                  ' Mobile Safari/537.36')
    headers = {'user-agent': user_agent}

    def get_website_membership(site):

        def print_fail():
            print(site.rjust(width), ':', colored(state.ljust(width//2), 'red'), '(Status:', msg, ')')

        def print_success():

            print(site.rjust(width), ':', colored(state.ljust(width//2), 'green'), '(Status:', msg, ')')

        url = websites[site]
        global counter
        state = "FAIL"
        msg = '--exception--'

        if not url[:1] == 'h':
            link = 'https://'+uname+url
        else:
            link = url+uname

        try:
            if site == 'Youtube' or 'Twitter':
                response = requests.get(link)
            else:
                response = requests.get(link, headers=headers)
            tag = soup.find(id=response.status_code)
            msg = tag.find_parent('dt').text
            response.raise_for_status()

        except Exception:
            print_fail()

        else:
            res_soup = BeautifulSoup(response.content, 'html.parser')
            if site == 'Pastebin':
                if len(res_soup.find_all('h1')) == 0:
                    msg = 'broken URL'
                    print_fail()

                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))
            if site == 'LinkedIn':
                if len(res_soup.find_all('h1')) == 0:
                    msg = 'broken URL'
                    print_fail()

                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))
            elif site == 'Wordpress':
                if 'doesn’t exist' or 'blocked' in res_soup:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))

            # elif site == 'Imgur':
            #     ToDo

            elif site == 'GitLab':
                if 'Sign in' in res_soup.title.text:
                    msg = 'broken URL'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))
            elif site == 'HackerNews':
                if 'No such user.' in res_soup:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))
            elif site == 'ProductHunt':
                if 'Page Not Found' in res_soup.text:
                    msg = 'No Such User!'
                    print_fail()
                else:
                    state = 'SUCCESS'
                    counter += 1
                    print_success()
                    print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))
            else:
                state = 'SUCCESS'
                counter += 1
                print_success()
                print(colored("\t\tLink to profile {}".format(link),'red','on_cyan',attrs=['bold','dark','underline']))

    websites = {
        'LinkedIn' : 'https://www.linkedin.com/in/',   
        'Facebook': 'https://www.facebook.com/',
        'Twitter': 'https://twitter.com/',
        'Instagram': 'https://www.instagram.com/',
        'Youtube': 'https://www.youtube.com/user/',
        'Reddit': 'https://www.reddit.com/user/', 
        'ProductHunt': 'https://www.producthunt.com/@',
        'PInterest': 'https://www.pinterest.com/',
        'Flickr': 'https://www.flickr.com/people/',
        'Vimeo': 'https://vimeo.com/',
        'Soundcloud': 'https://soundcloud.com/',
        'Disqus': 'https://disqus.com/',
        'Medium': 'https://medium.com/@',
        'AboutMe': 'https://about.me/',
        'Imgur': 'https://imgur.com/user/', 
        # returns a landing page. to do
        'Flipboard': 'https://flipboard.com/',
        'Slideshare': 'https://slideshare.net/',
        'Spotify': 'https://open.spotify.com/user/',
        'Scribd': 'https://www.scribd.com/',
        'Patreon': 'https://www.patreon.com/',
        'BitBucket': 'https://bitbucket.org/',
        'GitLab': 'https://gitlab.com/',
        'Github': 'https://www.github.com/',
        'GoodReads': 'https://www.goodreads.com/',
        'Instructable': 'https://www.instructables.com/member/',
        'CodeAcademy': 'https://www.codecademy.com/',
        'Gravatar': 'https://en.gravatar.com/',
        'Pastebin': 'https://pastebin.com/u/',
        'FourSquare': 'https://foursquare.com/',
        'TripAdvisor': 'https://tripadvisor.com/members/',
        'Wikipedia': 'https://www.wikipedia.org/wiki/User:',
        'HackerNews': 'https://news.ycombinator.com/user?id=',
        'CodeMentor': 'https://www.codementor.io/',
        'Trip': 'https://www.trip.skyscanner.com/user/',
        'Blogger': '.blogspot.com',
        'Wordpress': '.wordpress.com',
        'Tumbler': '.tumblr.com',
        'Deviantart': '.deviantart.com"',
        # ^ This website is either blocking/delaying the script
        'LiveJournel': '.livejournal.com',
        'Slack': '.slack.com',
    }

    p = ThreadPool(10)
    p.map(get_website_membership, list(websites.keys()))
    n_websites = len(list(websites.keys()))
    print('Summary: User {} has membership in {}/{} websites'
          .format(uname, counter, n_websites))
    print(f"Completed {len(websites)} queries in {time.time() - start_time:.2f}s")
   
    return counter

if __name__ == '__main__':
    main()
