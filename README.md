# Stacky

## Introduction
According to a report on the Chatbot Market by Global Forecast, the Chatbot market size will grow to $10.5 billion by 2026. Chatbots have been utilized by many different industries, ranging from e-commerce to education, in an effort to increase user engagement and efficiency. 

Chatbots function by performing routine tasks based on algorithms and triggers that simulate a human conversation. Typical chatbots retrieve their conversational skills from static data the programmer inputs. In this project, I created my own version of a chatbot called Stacky but I expanded Stacky’s capabilities by using the powers of Machine learning and Natural Language Processing. Instead of being restricted to a finite set of responses, Stacky is able to imitate human-like interactions by analyzing data the same way a human brain would. My chatbot does this by extracting data from Stack Overflow hence its name “Stacky”. Stacky derives its intelligence from StackOverflow allowing the programmer to ask coding questions to Stacky and in return, Stacky will try to answer the question from the knowledge it gained from the StackOverflow data extraction. The reason I chose this project is because of my recent discovery of ChatGPT. I became curious about how ChatGPT was so much more advanced than other chatbots. ChatGPT uses Natural Language Processing and Machine Learning so I wanted to work on a project that will help me become familiar with these topics while still being able to implement my ideas.

## Project Overview
There is a concept in computer science that says “garbage in equals garbage out”. The chatbot’s dataset needed to be clean and thorough. I exhausted several options for deciding what database to work off of. First I tried to look for a pre-made dataset on the internet that I could simply download. However, the only ones available were from 2011 and I wanted my chatbot to have more recent data. There were also other versions but they were only available in the torrent file format and as I have learned the hard way unless you are experienced at torrenting files, it is best to leave it alone. So in the end, I decided to use the power of web scraping to extract live data from https://stackoverflow.com/questions. For this, I used the Beautiful Soup module which is a free Python library for web scraping. I ran into these problems while learning how to web scrape:

 1. StackOverflow was bought by a company called Prosus in 2021 and it seems as a result, the Stack Overflow website’s HTML configurations changed as well meaning that many of the resources online about web scraping StackOverflow was outdated. Therefore, I got to teach myself a little HTML while web scraping my data.
 2. Although web scraping StackOverflow is legal, there is a limit to the number of requests one can send out during a period. If too many requests are detected from an IP address, StackOverflow will block you for around 10 to 15 minutes. Since there is no definitive time on how long I needed to wait between requests, I had to be careful not to overload StackOverflow’s server and extract my data ethically.

Using BeautifulSoup, questions from StackOverflow and their most upvoted answers were then extracted into an intents.json file which was then fed into the machine learning model, created using libraries such as Tensorflow, Keras, and NLTK. The machine learning model parses through the questions and answers in the dataset and tokenizes the words using the Natural Language Processing library, NLTK. To do this, I first created the training data, which was obtained by parsing through the database and categorizing each word. However, a machine learning model can only be trained off of numerical values so training data full of words would be of no use. To convert our data into numerical values that a neural network would be able to read, I used a popular technique called “bag of words” which vectorizes text and turns them into values compatible with my machine learning model. Once the data was converted into numerical values, I built the Neural Network model using the Sequential Tensorflow model. This was easier to implement than I thought because there was extensive documentation and resources available online. The dataset is trained in the model 3000 times and outputs its loss and accuracy rates for each piece of data. An example of such output looks like this:

Epoch 2992/3000
139/139 [==============================] - 0s 3ms/step - loss: 0.3731 - accuracy: 0.8853

After a process of trial and error, I found that 3000 epochs gave me a low enough loss rate with a fairly high accuracy to continue. This number had to be determined carefully as there was a risk of overtraining where instead of learning the data, the model memorizes it.

The bot uses this information to generate the best response. However, before outputting to the user, it is cleaned up using Natural Language Processing. At this point, the chatbot is fully functional from inside the terminal but I decided to extend the chatbot into a Flask web application for easier readability for the user. To run this app, one must clone the repository and enter this command into the terminal: python app.py Then click on the link... Running on http://XXX.XXX.X.XX:8888 (where the X’s are your IP address) Then you should see Stacky running on the web!

## Unit Tests
The main Python project files were unit tested using the module unittest. The file app.py is the only Python file that was not unit tested. Due to the Flask application aspect not being essential to Stacky's functionality, app.py does not have a unittest because of the complications that arise when testing functions that need an active HTTP request. However, database.py, processor.py, and chatbot.py were all successfully unit tested. Some of the unit tests take a very long time to finish. Below are screenshots of each of these files passing their unit tests.

### test_database.py
![Screenshot (315)](https://user-images.githubusercontent.com/98305390/210315972-d01fe31d-d8bc-4109-9ab5-bd4e14013926.png)


### test_processor.py
![Screenshot (316)](https://user-images.githubusercontent.com/98305390/210316107-0c041fa7-7cde-4fd9-93d0-7eb56a17796b.png)


### test_chatbot.py
![Screenshot (317)](https://user-images.githubusercontent.com/98305390/210316147-90e8eb6d-e69d-43a1-8355-945a603c9cfb.png)

