# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from pathlib import Path


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)

    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory (object):
    def __init__ (self, guid, title, description, link, pubdate=None):
        '''
        Initializes a NewsStory object
                
        guid (string): the global unique identifier
        title (string): The title of the article
        description (string): a paragraph or so description of the article
        link (string): links to the additional content surrounding the article
        pubdate (datetime): the publication date of the article, defaults to none if no date

        A NewsStory object has five attributes:
            self.guid (string, determined by input guid)
            self.title (string, determined by input title)
            self.description (string, determined by input description)
            self.link (string, determined by input link)
            self.pubdate(datetime, determined by input pubdate)
        '''

        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class
        
        Returns: self.guid
        '''
        
        return self.guid
    
    def get_title(self):
        '''
        Used to safely access self.title outside of the class
        
        Returns: self.title
        '''
        
        return self.title
    
    def get_description(self):
        '''
        Used to safely access self.description outside of the class
        
        Returns: self.description
        '''
        
        return self.description
    
    def get_link(self):
        '''
        Used to safely access self.link outside of the class
        
        Returns: self.link
        '''
        
        return self.link
    
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class
        
        Returns: self.pubdate
        '''
        
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger (Trigger):
    def __init__(self, phrase):
        """
        Initializes a PhaseTrigger object

        phrase (string): The phrase to use for the trigger

        A PhraseTrigger has one attribute:
            self.phrase (string, determined by input text)
        """

        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        """
        Checks whether self.phrase is in the inputted text

        text (string): The text to find the phrase in

        Returns: True or False
        """

        tempString = text.lower()

        for puncs in string.punctuation:
            # each punctuation is replaced with a space
            # note: strings are immutable, this is inefficient
            tempString = tempString.replace(puncs, " ")
            
        # splits tempString into list of words
        strippedWords = tempString.split(" ")
        # splits the phrase into a list of words
        splitPhrase = self.phrase.split(" ")

        # while there are empty list elements remove them
        while '' in strippedWords:
            strippedWords.remove('')

        # if any of the phrase words aren't in the list, there's no match
        if splitPhrase[0] not in strippedWords:
            return False
        # otherwise there could be a match
        else:
            # for each word in the given text
            for textWords in strippedWords:
                # if any word is the first word of our phrase
                if textWords == splitPhrase[0]:
                    # get this words index and begin checking the rest of the phrase
                    index = strippedWords.index(textWords)
                    # start a loop count at 1, so as to check the 2nd element of splitPhrase first
                    for i in range(1, len(splitPhrase)):
                        if index < len(strippedWords)-1:
                            index += 1
                        if splitPhrase[i] == strippedWords[index]:
                            # if the last word of the phrase string has been reached
                            # the full phrase is in the text
                            if (i+1) == len(splitPhrase):
                                return True
            
            # if this point is reached there was no matches
            return False




            

# Problem 3
class TitleTrigger (PhraseTrigger):
    def evaluate(self, news):
        """
        Checks whether self.phrase is in the title

        news (object): The news article object to find the title in

        Returns: True or False
        """

        return self.is_phrase_in(news.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, news):
        """
        Checks whether self.phrase is in the description

        news (object): The news article object to find the title in

        Returns: True or False
        """

        return self.is_phrase_in(news.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger (Trigger):
    def __init__ (self, time):
        """
        Initializes a TimeTrigger object

        time (string): The time in EST as a string in the following format: '3 Oct 2016 17:00:10'

        A TimeTrigger has one attribute:
            self.time (datetime, determined by input time)
        """

        # converts string to datetime
        pubtime = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        # changes timezone
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        # sets self
        self.pubtime = pubtime

# Problem 6
class BeforeTrigger (TimeTrigger):
    def evaluate(self, news):
        """
        Checks whether story is published before trigger's time

        news (object): The news article object to find the pubdate in

        Returns: True or False
        """

        return news.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.pubtime


class AfterTrigger (TimeTrigger):
    def evaluate(self, news):
        """
        Checks whether story is published after trigger's time

        news (object): The news article object to find the pubdate in

        Returns: True or False
        """

        return news.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.pubtime


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger (Trigger):
    def __init__(self, other):
        """
        Initializes a NotTrigger object

        other (object): The object that is being 'notted'

        A NotTrigger has one attribute:
            self.trigger (object, determined by input other)
        """ 

        self.trigger = other
    
    def evaluate (self, news):
        """
        Sends the opposite trigger to the one sent in for self.trigger

        news (object): The news article object

        Returns: True or False
        """

        # this variable holds True or False depending on self.trigger
        original = self.trigger.evaluate(news)

        # If original trigger is true return false, vice versa
        return not original


# Problem 8
class AndTrigger (Trigger):
    def __init__(self, obj1, obj2):
        """
        Initializes an AndTrigger object

        obj1 (object): The first object that is part of the 'and'
        obj2 (object): The second object that is part of the 'and'

        An AndTrigger has two attribute:
            self.trigger1 (object, determined by input obj1)
            self.trigger2 (object, determined by input obj2)
        """ 

        self.trigger1 = obj1
        self.trigger2 = obj2
    
    def evaluate (self, news):
        """
        Sends the trigger dpeending on two other triggers

        news (object): The news article object

        Returns: True or False
        """

        # Hold true or false depending on their respective triggers
        result1 = self.trigger1.evaluate(news)
        result2 = self.trigger2.evaluate(news)

        # if both are true then true, otherwise false
        return result1 and result2


# Problem 9
class OrTrigger (Trigger):
    def __init__(self, obj1, obj2):
        """
        Initializes an OrTrigger object

        obj1 (object): The first object that is part of the 'or'
        obj2 (object): The second object that is part of the 'or'

        An AndTrigger has two attribute:
            self.trigger1 (object, determined by input obj1)
            self.trigger2 (object, determined by input obj2)
        """ 

        self.trigger1 = obj1
        self.trigger2 = obj2
    
    def evaluate (self, news):
        """
        Sends the trigger dpeending on two other triggers

        news (object): The news article object

        Returns: True or False
        """

        # Hold true or false depending on their respective triggers
        result1 = self.trigger1.evaluate(news)
        result2 = self.trigger2.evaluate(news)

        # if either are true then true, otherwise false
        return result1 or result2

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of News instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    
    filteredList = []
    
    # loops through each article
    for articles in stories:
        # loops through each trigger per article
        for triggers in triggerlist:
            # if any trigger hits add the article to the filtered list
            # and break out the trigger loop
            if triggers.evaluate(articles):
                filteredList.append(articles)
                break
    
    # return the filtered list
    return filteredList



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []

    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    
    # initialize trigger dictionary and list
    trigDict = {}
    trigList = []

    # for each input line
    for inputs in lines:
        # split into temporary list at each comma
        tempList = inputs.split(",")
        # if first input in line was ADD then add to list
        if tempList[0].upper() == "ADD":
            # adds each listed trigger to the trigger list
            for i in range(1, len(tempList)):
                trigList.append(trigDict[tempList[i]])
        # otherwise it adds the corresponding trigger object to the dictionary
        elif tempList[1] == "TITLE":
            trigDict[tempList[0]] = TitleTrigger(tempList[2])
        elif tempList[1] == "DESCRIPTION":
            trigDict[tempList[0]] = DescriptionTrigger(tempList[2])
        elif tempList[1] == "BEFORE":
            trigDict[tempList[0]] = BeforeTrigger(tempList[2])
        elif tempList[1] == "AFTER":
            trigDict[tempList[0]] = AfterTrigger(tempList[2])
        elif tempList[1] == "NOT":
            trigDict[tempList[0]] = NotTrigger(trigDict[tempList[2]])
        elif tempList[1] == "AND":
            trigDict[tempList[0]] = AndTrigger(trigDict[tempList[2]], trigDict[tempList[3]])
        elif tempList[1] == "OR":
            trigDict[tempList[0]] = OrTrigger(trigDict[tempList[2]], trigDict[tempList[3]])

    # returns the list of triggers
    return trigList



SLEEPTIME = 5 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("trump")
        # t3 = DescriptionTrigger("clinton")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config(Path(__file__).with_name('triggers.txt'))
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

