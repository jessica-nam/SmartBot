from bs4 import BeautifulSoup
import requests
import csv

# Page we want to scrape (Questions page from stackoverflow)
URL = "https://stackoverflow.com/questions"
PAGE_LIMIT = 1


def build_url(base_url=URL, tab="newest", page=1):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page
        Example: https://stackoverflow.com/questions?tab=newest&page=1"""

    return f"{base_url}?tab={tab}&page={page}"

def scrape_one_question_page(page=1):
    """ Retrives newest question and answers from StackOverflow by scraping one page 
        *** NOTE TO SELF: "answers" derived from this function only indicates answer count """

    response = requests.get(build_url(page=page))
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")


    # Questions found in h3 tags with class='s-post-summary--content-title'
    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")


    # Question descriptions found in h3 tags with class='s-post-summary--content-excerpt'
    description_list = soup.find_all(
        "h3", class_="s-post-summary--content-excerpt")


    # Vote/Answer/View descriptions found in span tags with class='s-post-summary--stats-item-number'
    # (Vote,Answer,View) format
    vote_answer_view_HTML_list = soup.find_all(
        "span", class_="s-post-summary--stats-item-number") # THIS IS HTML NOT TEXT


    # (Vote,Answer,View) values
    vote_answer_view_list = []
    for v in vote_answer_view_HTML_list:
        vote_answer_view_list.append(v.text) # THIS IS TEXT

    # Find link
    answers_link_list = soup.find_all("a", class_="s-link")

    # Remove the first two links which are javascript:void(0)
    answers_link_list = answers_link_list[2:]

    #Remove last link which is https://stackexchange.com/questions?tab=hot
    answers_link_list = answers_link_list[:-1]

    # (Question,Vote,Answer,View)
    OnePageOutput = []

    i = 0
    for (x, y) in zip(questions_list, answers_link_list):
        OnePageOutput.append(x.text.strip())
        question = x.text.strip()


        link = y['href']
        post_ID = link[11:19]
        OnePageOutput.append(post_ID)

    
        for j in range(3):
            OnePageOutput.append(vote_answer_view_list[i+j])

        i += j+1
  
    i = 0
    # List values ([Question,Vote,Answer,View]) split for each question
    triplet_vote_answer_view_list = [
    OnePageOutput[i:i + 5] for i in range(0, len(OnePageOutput), 5)]

    print(triplet_vote_answer_view_list)

    # Dictionary format for CSV
    QuestionPage = []

    for i in triplet_vote_answer_view_list:
        # Unpack values

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
    """ This function can scrape multiple pages limited to page_limit """
    questions = []
    for i in range(1, page_limit + 1):
        page_question = scrape_one_question_page(i)
        questions.extend(page_question) # Use extend to add multiple items
    return questions

def scrape_answer_pages(page_limit):
    """ This function can scrape multiple pages limited to page_limit """
    questions = []
    for i in range(1, page_limit + 1):
        page_question = scrape_one_answer_page(i)
        questions.extend(page_question) # Use extend to add multiple items
    return questions


def export_data():
    data = scrape_one_question_page(2)
    with open("questions.csv", "w") as f:
        fieldnames = ["question", "postID", "votes", "answers", "views"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        print("Done writing")

def scrape_one_answer_page(page=1):
    """ Retrives the answer from the question page by the link """

    # Access the question page to grab the question ID
    response = requests.get(build_url(page=page))
    soup = BeautifulSoup(response.text, features="html.parser")

    
    # find link
    answers_link_list = soup.find_all("a", class_="s-link")

    # Remove the first two links which are javascript:void(0)
    answers_link_list = answers_link_list[2:]

    #Remove last link which is https://stackexchange.com/questions?tab=hot
    answers_link_list = answers_link_list[:-1]

    for i in answers_link_list:
        link = i['href']
        post_ID = link[11:19]

    

if __name__ == "__main__":

    from pprint import pprint # For readability
    pprint(scrape_one_question_page(1))
    export_data()
    scrape_answer_pages(2)
