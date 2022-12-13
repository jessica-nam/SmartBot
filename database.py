from bs4 import BeautifulSoup # For webscraping
from pprint import pprint     # For readability while testing
import requests               # For accessing URL
import csv                    # For writing data
import re                     # For extracting postID 

# These are the base URLs I will use
URL1 = "https://stackoverflow.com/questions/tagged/"
URL2 = "https://stackoverflow.com/questions/" # For getting answer URL

# This is a fully configured example URL for votes and newest
# URL = "https://stackoverflow.com/questions/tagged/python?tab=votes&page=1"
# URL = "https://stackoverflow.com/questions/tagged/recursion?tab=newest&page=1"

# Users should be able to filter what kind of StackOverflow Questions page the chatbot will extract data from
# Choices (default is no tag and newest tab)
TAG = ""  # can be "python", "recursion". etc.
TAB = "votes"  # can be "newest", "votes", "Frequent (Questions with most links)"

# Pre set page amount
PAGE_LIMIT = 3 # if 3 it actually grabs 10 pages idky


def build_url(base_url=URL1, tag = TAG, tab=TAB, page=PAGE_LIMIT):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page """

    return f"{base_url}{tag}?tab={tab}&page={page}"

def build_answer_url(base_url=URL2, postID=""):
    """ Builds StackOverflow answer URL format which takes in two parameters: postID and question """    
        
    return f"{base_url}{postID}"

def scrape_one_question_page(page=1):
    """ Retrives newest question, postID, votes, answer, view count from StackOverflow by scraping one page 
        NOTE TO SELF: "answers" derived from this function only indicates answer count """

    response = requests.get(build_url(page=page))

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")

    ##### Questions found in h3 tags with class='s-post-summary--content-title'
    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")

    ##### Find question answer link (we can grab postID from this)
    answers_link_list = soup.find_all("a", class_="s-link")
    answers_link_list = answers_link_list[3:]   # Remove the first three links which are javascript:void(0)
    answers_link_list = answers_link_list[:-1]  # Remove last link which is https://stackexchange.com/questions?tab=hot

    ##### Vote/Answer/View descriptions found in span tags with class='s-post-summary--stats-item-number'
    vote_answer_view_HTML_list = soup.find_all( 
        "span", class_="s-post-summary--stats-item-number") # THIS IS HTML NOT TEXT
    vote_answer_view_list = []
    for v in vote_answer_view_HTML_list:
        vote_answer_view_list.append(v.text) # THIS IS TEXT

    ##### CURRENTLY UNUSED ######
    # Question descriptions found in h3 tags with class='s-post-summary--content-excerpt'
    description_list = soup.find_all(
        "h3", class_="s-post-summary--content-excerpt")



    # [Question, Post_ID, Vote, Answer, View]
    OnePageOutput = []

    i = 0
    for (x, y) in zip(questions_list, answers_link_list):
        OnePageOutput.append(x.text.strip())

        ### Grab question summary 
        question = x.text.strip()

        ### Grab postID
        link = y['href']
        post_ID = link[10:20]                           # format: "/503093/"
        post_ID = str(re.findall('/([^"]*)/', post_ID)) # format: "['503093']"
        post_ID = post_ID[1:-1]                         # format: "'503093'"
        post_ID = post_ID.replace("'", "")              # format: "503093"
        OnePageOutput.append(post_ID)                   # Add as second element after its question summary

    
        ### Grab [Vote, Answer, View] values for the question 
        for j in range(3):
            OnePageOutput.append(vote_answer_view_list[i+j])

        i += j+1
    i = 0

    # data values ([Question,PostID,Vote,Answer,View]) split for each question
    data = [
    OnePageOutput[i:i + 5] for i in range(0, len(OnePageOutput), 5)]

    # Dictionary format for CSV
    QuestionPage = []

    # Unpack data into dictionary format
    for i in data:
        question, postID, vote, answer, view = [str(e) for e in i]

        QuestionPage.append({
            "question": question,
            "postID": postID,
            "votes": vote,
            "answers": answer,
            "views": view
        })
    return QuestionPage


def scrape_question_pages(page_limit):
    """ This function can scrape multiple pages up tp page_limit """
    questions = []
    for i in range(1, page_limit + 1):
        page_question = scrape_one_question_page(i)
        questions.extend(page_question) # Use extend to add multiple items
    return questions


def export_data():
    """ Export dictionary data into questions.csv file """

    ### If you only want data from one page ###
    # data = scrape_one_question_page(PAGE_LIMIT)

    ### If you want data from multiple pages ###
    data = scrape_question_pages(PAGE_LIMIT)

    with open("questions.csv", "w") as f:
        fieldnames = ["question", "postID", "votes", "answers", "views"] # Rows for CSV
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        print("Done writing")

def scrape_one_answer_page(postID):
    """ Retrives the answer from the question page by the postID """

    response = requests.get(build_answer_url(URL, postID))
    soup = BeautifulSoup(response.text, features="html.parser")

    answers_list = soup.find_all(
        "div", class_="s-prose js-post-body")

    for x in answers_list:
        print(x.find('p').text)

    
    

if __name__ == "__main__":

    L = scrape_one_question_page(2)
    print(L)
    print(L[0]["postID"])
    print(L[0]["question"])

    print(build_answer_url(URL1, L[0]["postID"]))
    # scrape_one_answer_page(L[1]["postID"])
    #scrape_one_answer_page(36730372, "extract-the-text-from-p-within-div-with-beautifulsoup")
    export_data()

