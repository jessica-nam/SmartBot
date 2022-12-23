from bs4 import BeautifulSoup # For webscraping
from pprint import pprint     # For readability while testing
import requests               # For accessing URL
import csv                    # For writing data
import re                     # For extracting postID 
import json                   # CSV to JSON

# These are the base URLs I will use
URL1 = "https://stackoverflow.com/questions/tagged/"
URL2 = "https://stackoverflow.com/questions/" # For getting answer URL

# This is a fully configured example URL for votes and newest
# URL = "https://stackoverflow.com/questions/tagged/python?tab=votes&page=1"
# URL = "https://stackoverflow.com/questions/tagged/recursion?tab=newest&page=1"

# Users should be able to filter what kind of StackOverflow Questions page the chatbot will extract data from
# Choices (default is no tag and newest tab)
TAG = "python"  # can be "python", "recursion". etc.
TAB = "votes"  # can be "newest", "votes", "Frequent (Questions with most links)"

# Pre set page amount
PAGE_LIMIT = 2 # if 3 it actually grabs 10 pages idky

def build_url(base_url=URL1, tag = TAG, tab=TAB, page=PAGE_LIMIT):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page """
    # print(f"{base_url}{tag}?tab={tab}&page={page}")
    return f"{base_url}{tag}?tab={tab}&page={page}"

def build_answer_url(base_url=URL2, postID=""):
    """ Builds StackOverflow answer URL format which takes in two parameters: postID and question """    
        
    return f"{base_url}{postID}"

def scrape_one_question_page(page):
    """ Retrives newest question, postID, votes, answer, view count from StackOverflow by scraping one page 
        NOTE TO SELF: "answers" derived from this function only indicates answer count """

    response = requests.get(build_url(page=page), timeout=5)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")

    ##### Questions found in h3 tags with class='s-post-summary--content-title'
    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")

    ##### Find question answer link (we can grab postID from this)
    answers_link_list = soup.find_all("a", class_="s-link")
    answers_link_list = answers_link_list[2:]   # Remove the first two links which are javascript:void(0)
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
        question, postID, vote, answers, view = [str(e) for e in i]

        answer = "none"

        if int(answers) > 0:
            response = requests.get(f"https://stackoverflow.com/questions/{postID}", timeout=5)
            soup = BeautifulSoup(response.text, features="html.parser")
            answer = soup.find("div", class_=["answer", "js-answer", "accepted_answer"])
            if not answer: 
                answer = soup.find("div", class_=["answer", "js-answer"])

            if answer is None:
                answer = ""
            else:
            
                answer = "".join(map(lambda x: x.text.strip(), answer.find("div", {"class": ["s-prose", "js-post-body"]})("p")))

        # print(answer)

        QuestionPage.append({
            "question": question,
            "postID": postID,
            "votes": vote,
            "answers": answers,
            "views": view,
            "url": f"https://stackoverflow.com/questions/{postID}",
            "answer": answer
        })
    return QuestionPage


def scrape_question_pages(page_limit):
    """ This function can scrape multiple pages up tp page_limit """
    questions = []
    for i in range(1, page_limit + 1):
        page_question = scrape_one_question_page(i)
        questions.extend(page_question) # Use extend to add multiple items
    return questions

# def scrape_one_answer_page(postID):
#     """ Retrives the answer from the question page by the postID """

#     response = requests.get(build_answer_url(URL, postID))
#     soup = BeautifulSoup(response.text, features="html.parser")

#     answers_list = soup.find_all(
#         "div", class_="s-prose js-post-body")

#     for x in answers_list:
#         print(x.find('p').text)

def export_data(pages):
    """ Export dictionary data into questions.csv file """

    

    ### Data from multiple pages ###
    data = scrape_question_pages(pages)
    
    with open("testing.csv", "w", encoding="utf-8") as f:
        fieldnames = ["postID", "question", "views", "votes", "answers", "answer", "url"] # Rows for CSV
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        print("Done writing to CSV")

def to_JSON(file):
    """ Convert CSV file to JSON Dictionary format file """

    with open(file, "r",encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        data = {"query": []}
        for row in reader:
            #print(row)
            if row == []:
                print("empty")
            else:
                data["query"].append({
                    "postID": row[0], 
                    "question": row[1], 
                    "views": row[2],
                    "votes": row[3],
                    "answers": row[4], # Number of answers
                    "answer": row[5],  # Top answer
                    "url": row[6], 
                    })
    
                print(data)
    


if __name__ == "__main__":
    pages = 1

    #### Uncommenting this will cause refresh
    # export_data(pages)

    file = "testing.csv"
    to_JSON(file)
