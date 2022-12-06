from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import csv

# Page we want to scrape (Questions page from stackoverflow)
URL = "https://stackoverflow.com/questions"
PAGE_LIMIT = 1


def build_url(base_url=URL, tab="newest", page=1):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page
        Example: https://stackoverflow.com/questions?tab=newest&page=1"""

    return f"{base_url}?tab={tab}&page={page}"


def scrape_page(page):
    """ Retrives newest question and answers from StackOverflow by scraping one page 
        *** NOTE TO SELF: "answers" derived from this function only indicates answer count """

    response = requests.get(build_url(page=page))
    page_questions = []

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

    # (Question,Vote,Answer,View)
    OnePageOutput = []

    i = 0
    for x in questions_list:
        OnePageOutput.append(x.text)
        question = x.text
    
        for j in range(3):
            OnePageOutput.append(vote_answer_view_list[i+j])

        i += j+1
    i = 0

    # List values ([Question,Vote,Answer,View]) split for each question
    triplet_vote_answer_view_list = [
    OnePageOutput[i:i + 4] for i in range(0, len(OnePageOutput), 4)]

    # Dictionary format for CSV
    QuestionPage = []

    for i in triplet_vote_answer_view_list:
        # Unpack values
        question, vote, answer, view = [str(e) for e in i]

        QuestionPage.append({
            "question": question,
            "votes": vote,
            "answers": answer,
            "views": view
        })
    return QuestionPage


def scrape(page_limit):
    """ This function can scrape multiple pages limited to page_limit """
    questions = []
    for i in range(1, page_limit + 1):
        page_question = scrape_page(i)
        questions.extend(page_question) # Use extend to add multiple items
    return questions


def export_data():
    data = scrape(2)
    with open("questions.csv", "w") as f:
        fieldnames = ["question", "votes", "answers", "views"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
        print("Done writing")


if __name__ == "__main__":

    from pprint import pprint # For readability

    export_data()
