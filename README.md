# SmartBot

## Introduction
According to a report on the Chatbot Market by Global Forecast, the Chatbot market size will grow to $10.5 billion by 2026. Chatbots have been utilized by many different industries, ranging from e-commerce to travel, in an effort to increase customer engagement and efficiency. 

Chatbots function by performing routine tasks based on algorithms and triggers that simulate a human conversation. Typical chatbots retrieve their conversational skills from static data the programmer inputs. In this project, I will be creating my own version of a chatbot called the SmartBot but I will be expanding SmartBot’s capabilities by using the powers of Deep learning and Natural Language Processing. Instead of being restricted to a finite set of responses, the SmartBot will learn from the data based human dialogue and become more intelligent. I will be extracting this data from StackOverflow. I first tried to be lazy and download a torrent file already containing Stack Overflow data but could only find data from around 2010. I did not like how outdated this data was so I decided to web scrape StackOverflow, thus getting the newest information, using the public Stack Exchange API and the module BeautifulSoup.

## Purpose
Sometimes just talking through a coding problem will lead to the solution. There is a technique for programmers called Rubber Duck. My coach, Hudson, introduced this tip to me while I was studying NCLab Python. The Rubber Duck technique is when programmers talk to a rubber duck about their code. The idea is that talking through your code will give you a better understanding of your program. I chose StackOverflow for my database because I believe my SmartBot could mimic this rubber duck for programmers when coding. The SmartBot derives its intelligence from StackOverflow allowing the programmer to ask coding questions to SmartBot and in return, the SmartBot will try to answer the question from the knowledge it gained from the StackOverflow data extraction. 

## Process

### 1. Data Extraction
First, I needed to get my data for my SmartBot to work on. For this, I used the Python module BeautifulSoup, a Python package for parsing HTML and XML documents. I also used the requests library, which is a HTTP library for Python, to grab the Stack Overflow Questions page URL. Then, I created functions to scrape the webpages by using the BeautifulSoup module and identified the question, vote, answer, and view values for that page. All of these values were then exported into a questions.csv file. 
The format of this CSV file is question, votes, answers, views.

### 2. Machine Learning Model

### 3. Training
