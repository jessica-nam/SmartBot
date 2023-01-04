# Stacky

## Background 
In this project, I created my own version of a chatbot called Stacky but I expanded Stacky’s capabilities by using the powers of Machine learning and Natural Language Processing. Instead of being restricted to a finite set of responses, Stacky is able to imitate human-like interactions by analyzing data the same way a human brain would. My chatbot does this by extracting data from Stack Overflow hence its name “Stacky”. Stacky derives its intelligence from StackOverflow allowing the programmer to ask coding questions to Stacky and in return, Stacky will try to answer the question from the knowledge it gained from the StackOverflow data extraction. The reason I chose this project is because of my recent discovery of ChatGPT. I became curious about how ChatGPT was so much more advanced than other chatbots. ChatGPT uses Natural Language Processing and Machine Learning so I wanted to work on a project that will help me become familiar with these topics while still being able to implement my ideas.

## How to use Stacky
### To extract data from StackOverflow, one must...
#### 1. Import the necessary modules
- pip install beautifulsoup4
- pip install requests
- pip install parrot
- pip install torch 
- pip install git+https://github.com/PrithivirajDamodaran/Parrot.git
#### 2. Change the TAG variable to whatever topic on stackOverflow to scrape (I recommend looking through https://stackoverflow.com/tags for ideas)
#### ![Screenshot (322)](https://user-images.githubusercontent.com/98305390/210464585-a5e9a199-7dd8-4600-bca6-2d0a579dbb50.png)
#### 3. Run the command ---> python database.py      into the terminal. The process of extracting can take up to 10 minutes but once the file finishes running, the user should be able to see the new data added on to the intents.json file.

### To train the Machine Learning model, one must...
#### 1. Import the necessary modules
- pip install nltk
- pip install numpy
- pip install tensorflow
#### 2. Run the command ---> python chatbot.py      into the terminal. This process is also slow as the model must be trained 3000 times. An output one can expect from running this file...
#### ![Screenshot (323)](https://user-images.githubusercontent.com/98305390/210466370-b2d70563-2aa2-4d0b-ac21-d93822452ce5.png)
#### 3. Once the model is trained, the classes.pkl, words.pkl, and model.h5 files are updated.

### To run Stacky web app...
#### 1. Import the necessary modules
- pip install Flask
#### 2. Run the command ---> python app.py      into the terminal. One should see this output below...
#### ![Screenshot (324)](https://user-images.githubusercontent.com/98305390/210473689-88e77d60-63cf-4f83-a3c6-c353c6c9c15b.png)
#### 3. Click on the link "Running on http://XXX.XXX.X.XX:8888" (where the X’s are your IP address) Then you should see Stacky running on the web!

## Unit Tests
### To run the unit tests, first CD into the unittest folder in the repository
### Next just enter the command ---> python test_chatbot.py (or other testing files)
The main Python project files were unit tested using the module unittest. The file app.py is the only Python file that was not unit tested. Due to the Flask application aspect not being essential to Stacky's functionality, app.py does not have a unittest because of the complications that arise when testing functions that need an active HTTP request. However, database.py, processor.py, and chatbot.py were all successfully unit tested. Some of the unit tests take a very long time to finish. Below are screenshots of each of these files passing their unit tests.

### test_database.py
![Screenshot (315)](https://user-images.githubusercontent.com/98305390/210315972-d01fe31d-d8bc-4109-9ab5-bd4e14013926.png)
### test_processor.py
![Screenshot (316)](https://user-images.githubusercontent.com/98305390/210316107-0c041fa7-7cde-4fd9-93d0-7eb56a17796b.png)


### test_chatbot.py
![Screenshot (317)](https://user-images.githubusercontent.com/98305390/210316147-90e8eb6d-e69d-43a1-8355-945a603c9cfb.png)

