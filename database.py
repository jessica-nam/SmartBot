from bs4 import BeautifulSoup # For webscraping
import requests               # For accessing URL
import re                     # For extracting postID 
import json                   # For writing data

# These are the base URLs I will use
URL1 = "https://stackoverflow.com/questions/tagged/"
URL2 = "https://stackoverflow.com/questions/" # For getting answer URL

# Users should be able to filter what kind of StackOverflow Questions page the chatbot will extract data from
# Choices (default is no tag and newest tab)
TAG = "OOP"  # can be "python", "recursion". etc.
TAB = "votes"  # can be "newest", "votes", "Frequent (Questions with most links)"

# # Pre set page amount
# PAGE_LIMIT = 1

def build_url(page, base_url=URL1, tag = TAG, tab=TAB):
    """ Builds StackOverflow questions URL format which takes in two parameters: tab and page """
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

    ##### Question descriptions found in h3 tags with class='s-post-summary--content-excerpt' #####
    description_list = soup.find_all(
        "div", class_="s-post-summary--content-excerpt")

    ##### Find the first tag of each question (This is needed for ML model) #####
    tag_list = soup.find_all("ul", class_="ml0 list-ls-none js-post-tag-list-wrapper d-inline")
    tag_text_list = []
    for tag in tag_list:
        for li in tag.find('li'):
            tag_text_list.append(li.text)
    
    # [Question, Post_ID, Vote, Answer, View]
    OnePageOutput = []

    i = 0
    for (x, y, z, a) in zip(questions_list, description_list, answers_link_list, tag_text_list):
        OnePageOutput.append(x.text.strip())
        OnePageOutput.append(y.text.strip())

        ### Grab question 
        question = x.text.strip()

        ### Grab question summary
        questionSum = y.text.strip()

        ### Grab postID
        link = z['href']
        post_ID = link[10:20]                           # format: "/503093/"
        post_ID = str(re.findall('/([^"]*)/', post_ID)) # format: "['503093']"
        post_ID = post_ID[1:-1]                         # format: "'503093'"
        post_ID = post_ID.replace("'", "")              # format: "503093"
        OnePageOutput.append(post_ID)                   # Add as second element after its question summary

        OnePageOutput.append(a)

        ### Grab [Vote, Answer, View] values for the question 
        for j in range(3):
            OnePageOutput.append(vote_answer_view_list[i+j])

        i += j+1
    i = 0

    # data values ([Question,Description,PostID,Vote,Answer,View]) split for each question
    data = [
    OnePageOutput[i:i + 7] for i in range(0, len(OnePageOutput), 7)]

    # Dictionary format for JSON
    QuestionPage = []

    # Unpack data into dictionary format
    for i in data:
        question, questionSum, postID, tag, vote, answers, view = [str(e) for e in i]

        answer = "none"

        if int(answers) > 0:
            response = requests.get(f"https://stackoverflow.com/questions/{postID}", timeout=5)
            soup = BeautifulSoup(response.text, features="html.parser")

            #### Gets top answer ####
            answer = soup.find("div", class_=["answer", "js-answer", "accepted_answer"])

            if not answer: 
                answer = soup.find("div", class_=["answer", "js-answer"])

            if answer is None:
                answer = ""
            else:
            
                answer = "".join(map(lambda x: x.text.strip(), answer.find("div", {"class": ["s-prose", "js-post-body"]})("p")))

            #### Gets all answers in a list ####
            answerlist = soup.findAll("div", class_=["answer", "js-answer", "suggested_answer"])
            answerlistConfig = []
            for ans in answerlist:
                answerText = "".join(map(lambda x: x.text.strip(), ans.find("div", {"class": ["s-prose", "js-post-body"]})("p")))
                if len(answerText): answerlistConfig.append(answerText)


        QuestionPage.append({
            "tag": tag,
            "question": [question] + [questionSum],
            
            # "postID": postID,
            # "votes": vote,
            # "answers": answers,
            # "views": view,
            # "url": f"https://stackoverflow.com/questions/{postID}",
            "answer": answerlistConfig
        })
    return QuestionPage

def export_data(page, outfile):
    """ Export dictionary data into outfile JSON """

    ### Data from multiple pages ###
    # data = scrape_question_pages(pages)

    ### Data from a specific page ###
    base = {"intents": scrape_one_question_page(page)}

    f = None

    try:
        f = open(outfile, "r+")
    except:
        f = open(outfile, "w")
        json.dump(base, f, indent=4)
    else:
        data = json.loads(f.read())
        base["intents"].extend(data["intents"])
        f.seek(0)
        json.dump(base, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    page = 1

    ### Uncommenting this will cause refresh
    export_data(page, "intents.json")