import requests
import re
import json
import isodate
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC


def find_course_page(a_list,course_name):
    # loop through the a elements
    for a in a_list:
        # check if the course name matches the user input
        if a.text.strip() == course_name:
            # extract the href attribute value of the a element
            course_link = a['href']
            print('Link to', course_name, ':', course_link)
            break
    try:
        return course_link
    except: #if course name is not found
        return None

def create_soup(link = 'https://ugcmoocs.inflibnet.ac.in/index.php/courses/moocs'):
    
    req = requests.get(link)

    soup = BeautifulSoup(req.content,'html.parser')

    return soup

def collect_links(link):
    # create a new browser instance
    browser = webdriver.Firefox()

    browser.get(link)

    # find the select element and create a Select object
    select_element = browser.find_element(by=By.CSS_SELECTOR,value='select')
    select = Select(select_element) #checks that the tag is indeed a select tag

    # loop through the options and scrape their contents
    # The first option is default and does not have any videos
    for option in select.options[1:]:
        
        select.select_by_visible_text(option.text)

        # Wait for the element to be clickable
        try:
            #Find the self learning element
            li_element = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="video_2"]')))
            
            #click on it to get dynamic content
            li_element.click()
            
            # switch to the iframe
            iframe = browser.find_element(By.XPATH,'//*[@id="youtube_player"]')
            
            #extract the link to the video
            src_link = iframe.get_attribute('src')
            
            #store the links in a text file
            filename = "links.txt"
            with open(filename, "a") as f:
                f.write(src_link+ '\n')
            f.close()
        except:
            #some modules do not have any videos which raises an exception which is handled by skipping over that module
            continue
    # close the browser window
    browser.quit()

    return

def get_video_duration(video_id):
    """
    Returns the duration of a YouTube video given its video ID.
    """

    #Youtube Data API
    api_key = 'AIzaSyDwwnyJr7tboh0Ofo9rl8v_uRqeizc5OtM'

    #link to video
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=contentDetails'
    response = requests.get(url)

    #parse the information as a json file
    data = json.loads(response.text)
    duration = data['items'][0]['contentDetails']['duration']
    duration_str = duration

    #since the duration is in iso date format, convert it to minutes and seconds
    duration = isodate.parse_duration(duration_str)
    total_seconds = duration.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)


    return minutes, seconds

def calculate_course_duration():
    '''
    Calculates the total duration of the course
    '''
    total_minutes = 0
    total_seconds = 0
    #the links are stores in a txt file 
    with open('links.txt','r') as f:
        for line in f:
            # Extract the video ID from the URL
            video_id = re.findall(r'embed/([\w-]+)', line)[0]

            # Get the duration of the video
            try:
                minutes, seconds = get_video_duration(video_id)

                total_minutes+=minutes
                total_seconds+=seconds
            except:
                continue
    f.close()

    #deletes the txt file as we no longer require it
    os.remove('links.txt')


    minutes = total_seconds // 60
    total_seconds = total_seconds % 60

    total_minutes += minutes

    hours = total_minutes // 60

    total_minutes = total_minutes % 60

    print(f'The total duration of this course is {hours} hours, {total_minutes} minutes, and {total_seconds} seconds.')



if __name__ =='__main__':

    link = 'https://ugcmoocs.inflibnet.ac.in/index.php/courses/moocs'
    soup = create_soup()

    # find the div element that contains the course names and links
    div = soup.find('div', {'id': 'pgcourses'})

    # get user input for the course name
    course_name = input('Enter the course name: ')

    # find all the a elements in the div element
    a_list = div.find_all('a')

    link = find_course_page(a_list, course_name)


    #if the course is not present in pg courses, search ug courses
    if (link==None):

        div = soup.find('div',{'id':'ugcourses'})

        a_list = div.find_all('a')

    link = find_course_page(a_list,course_name)

    try:
        if link is not None:
            collect_links(link)
        else:
            raise Exception('The given course is not found. Please enter the exact course name.\nExiting...') 
    except Exception as e:
        print(e)
        sys.exit()

    #print('test')
    
    calculate_course_duration()

    sys.exit(0)



