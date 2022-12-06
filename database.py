from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

# Page we want to scrape (Questions page from stackoverflow)
URL = "https://stackoverflow.com/questions"
PAGE_LIMIT = 1


def build_url(base_url=URL, tab="newest", page=1):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page
        Example: https://stackoverflow.com/questions?tab=newest&page=1"""
    return f"{base_url}?tab={tab}&page={page}"


def scrape_page(page=1):
    """ Retrives newest question and answers from StackOverflow by scraping one page """

    response = requests.get(build_url(page=page))
    page_questions = []

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")

    # Questions found in h3 tags with class='s-post-summary--content-title'
    questions_list = soup.find_all(
        "h3", class_="s-post-summary--content-title")

    # The question descriptions
    description_list = soup.find_all(
        "h3", class_="s-post-summary--content-excerpt")
    
    # (Vote/Answer/View) HTTP code
    vote_answer_view_HTTP_list = soup.find_all(
        "span", class_="s-post-summary--stats-item-number")

    # (Vote/Answer/View) values
    vote_answer_view_list = []
    for v in vote_answer_view_HTTP_list:
        vote_answer_view_list.append(v.text)

    

    vote_count_list = []
    answer_count_list = []
    view_count_list = []

    # List values (Vote/Answer/View) split into triplets for each question
    triplet_vote_answer_view_list = [
        vote_answer_view_list[i:i + 3] for i in range(0, len(vote_answer_view_list), 3)]

    print(triplet_vote_answer_view_list)

    OnePageOutput = []
    i = 0

    for x in questions_list:
        OnePageOutput.append(x.text)
        for j in range(3):
            OnePageOutput.append(vote_answer_view_list[i+j])
        i += j+1
        
    print(OnePageOutput)

    return triplet_vote_answer_view_list

if __name__ == "__main__":
    
    voteanswerview = scrape_page()



    
