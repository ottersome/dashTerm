#!/usr/bin/env python3
#import libraries
import sys
import curses
from gmail.gmail_credentials import * 
from scraping.scraper import Scraper
from curses import wrapper
from apiclient.discovery import build
from gmail.gmail_mails import GmailMessages
from oauth2client.client import GoogleCredentials
import httplib2
from spotify.spotify_credentials import *
from spotify.spotify_transactions import *
import logging
import threading
import os
import webbrowser
import unicodedata

#main class
class MainScreen:
    #Since we use curse and 4 windows we need to keep these variable accessible to all funcitons
    win1=None
    win2=None
    win3=None
    win4=None
    stdscr=None

    #functions hold directory to where the log file and this file are
    LOG_FILE = None
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    DISPLAYON = True

    #used to later check wether we are logged in to google account and spotify 
    googlecredencialos = None
    spotifyToken = 0

    #classes constructor, we just set a few variables up 
    def __init__(self):
        LOG_FILE = 'log.log'
        logging.basicConfig(filename=LOG_FILE,filemode='w',level=logging.DEBUG)
        FILE_DIR = os.path.dirname(os.path.abspath(__file__))
        logging.debug("THIS IS THE PATH : "+FILE_DIR)
        self.authorizeUser()
    #in this function we try to make sure that the user is authenticated before proceeding into the application
    #all of this uses spotipi api and googleapi for python 
    def authorizeUser(self):
        if self.googlecredencialos  == None:
            self.googlecredencialos = get_stored_credentials(1)
            if self.googlecredencialos == 0:
                email = input("Please input your Gmail address : \n")
                url = get_authorization_url(email,'')
                webbrowser.open(url)
                authorization = input("Please give me back the code they gave you in the browser : ")
                try:
                    self.googlecredencialos = get_credentials(authorization,"holis").to_json()
                except Exception as e:
                    logging.error("authorizeUser google cred exception : "+ str(e))
                    print("My apologies there was an error with the given code please try again")
                    quito()
        
        if self.spotifyToken == 0:
            spoti = SpotifyCredentials()
            self.spotifyToken = spoti.getToken('abuklao','user-read-private user-read-email user-library-read user-top-read')
    
        #making sure everything is in order
        if self.googlecredencialos != None and self.googlecredencialos != 0 and self.spotifyToken != None:
            try:
                #avoid any unwated outputs
                sys.stdout=open(os.devnull, 'w')
                #wrapper is used in order to make sure that the curses library is run smoothly at the beggining and when terminating
                curses.wrapper(self.firstSetup)
            except Exception as e:
                import traceback
                logging.error("Hi there : "+traceback.format_exc())
                logging.error("AT WRAPPER : "+str(e))
        else:
            print("Sorry you dont meet the requirements to enter the application please try again\nExiting....")
            quito()
    #
    def firstSetup(self,stdscr):
        #initializing curses with our preferences these functions start colors(in case we want to use colors) and make that if we type it wont me displayed in the terminal 
        curses.noecho()
        #curses.start_color()
        curses.use_default_colors()
        
        #after this is pretty much Initializing windows with their respective sizes, borders and titles
        logging.info("Initializing Screens...")
        self.stdscr = stdscr
        three_col_w = int(curses.COLS/3)
        self.win1= curses.newwin(curses.LINES,three_col_w,0,0)
        self.win2 = curses.newwin(curses.LINES,three_col_w,0,three_col_w)
        self.win3 = curses.newwin(int(curses.LINES/2),three_col_w,0,three_col_w*2)
        self.win4 = curses.newwin(int(curses.LINES/2),three_col_w,int(curses.LINES/2),three_col_w*2)

        self.stdscr.clear()
        self.win1.border(0)
        self.win2.border(0)
        self.win3.border(0)
        self.win4.border(0)

        self.win2.addnstr(0,1,"Welcome to DashTerm",self.win2.getmaxyx()[1]-2)
        self.win1.addnstr(0,1,"Gmail Inbox",self.win1.getmaxyx()[1] - 2)
        self.win3.addnstr(0,1,"Song Recommendations",self.win3.getmaxyx()[1]-2)
        self.win4.addnstr(0,1,"Tweets",self.win4.getmaxyx()[1]-2)

        self.stdscr.refresh()
        self.win1.refresh()
        self.win2.refresh()
        self.win3.refresh()
        self.win4.refresh()

        #here we start threads to look for information online. There should be at most 2 threads running at the same time on this app 
        try:
            t1=threading.Thread(target=self.checkSpotify)
            t2=threading.Thread(target=self.checkgoogle)
            t1.start()
            t2.start()
        except Exception as e:
            logging.error("firstSetup Error : "+str(e))
        
        #the "stdscr.getch()" function hangs the program while it waits for input. We use this to manipulate the gui and go url according to our desires
        while True:
            x = stdscr.getch()
            logging.info("BUTTON PRESSED "+chr(x))
            if x == ord('q'):
                self.quito()
            
            window = None
            index = -1 
            if x == ord('a'):
                window = self.win1
                index = 1
            elif x == ord('s'):
                window = self.win2
                index = 2
            elif x == ord('w'):
                window = self.win3
                index = 3
            elif x == ord('d'):
                window = self.win4
                index = 4
            if index >=1:
                #toggle makes the seleted window blink 
                self.toggleBlink(window,1)
                x = stdscr.getch()
                if x == ord('q'):
                    quito()
                '''elif x == ord('^['):
                    logging.info("ESCAPE PRESSED")'''
                #TODO add escape to go back 


                self.toggleBlink(window,0)
                #we load the link of the container we wanted into a browser
                self.loadLink(window,index,x)
    def quito(self):
        #sys.stdout.close()
        #sys.stderr.close()
        self.DISPLAYON = False
        self.win1 = None
        self.win2 = None
        self.win3 = None
        self.win4 = None

        curses.endwin()


        quit()

    #makes selected window blink 
    def toggleBlink(self,window,onoff):
        if onoff == 1:
            window.attrset(curses.A_BLINK)
            window.border(0)
            window.refresh()
            window.attrset(curses.A_NORMAL)
        else:
            window.attrset(curses.A_NORMAL)
            window.border(0)
            window.refresh()

    #link is loaded by loading a json file that contains all links previously stored at querying time
    def loadLink(self,window,part,x):
        
        #we load the file and check for the respective url
        logging.info("Loading link")
        data = self.JsonFileToDict("cache.json")
        if data != None:
            #This functions are volatile to lack of file existance of mis-interpretation therefore we surround with thy, however continuing wont harm the program 
            try:
                #as per the cache structure we use part and index to open information about each window and entry respectively to finally get the url 
                index = int(chr(x))-1
                url = data[str(part)][index]['url']
                logging.info("OPENING IN BROWSER : "+url)

                #when information is sucessfully retrieved we then open the browser
                webbrowser.open(url)
                #reload emails
                self.checkgoogle()
            except Exception as e:
                logging.error("loadLink exception : "+str(e))
                return
        else:
            return None
    #check spotify recommendations and top artists
    def checkSpotify(self):
        logging.debug("We are here niggas")
        #Get top artists
        try:
            spotra = SpotifyTransactions()
            infolist = ('name','uri')
            uri_list = []
            top_artists = spotra.getTopArtists(self.spotifyToken,infolist)
        except Exception as e:
            logging.error("CHECKSPOTIFY ERROR : \n" +e)
        #Get recommendations
        for item in top_artists:
            uri_list.append(item['uri'])
        #we use the list of top artists' URIs as a seed for the recommendations that will be provided by spotify 
        reco = spotra.recommendations(self.spotifyToken,uri_list,5)
    
        #display recomendations
        #with i and entries we make sure we dont exceed the amount of entries we print to the window
        i = 0
        #For thread safety 
        if self.DISPLAYON == False:
            return()
        entries = int(self.win3.getmaxyx()[0] / 3)
        stringoList = []
        for itemo in reco:
            #if it exceeds we break
            if i > entries:
                break
            #stringo is a strng that will be formatted to be later printed and cached 
            stringo = ''
            stringo = "Artist: "+itemo['artist']+"\nSong: "+itemo['song']
            maxes = self.win3.getmaxyx()
            #the position that we will take every step of i 
            inipos = (i*3+2,3)

            #Saving in cache as we previously mentioned of stringo, we also save the url in order to later open the browser to it 
            stringoList.append({'url':itemo['url'],'stringo':stringo})
    
            logging.debug("ADDING MESSAGE")
            #we add this entry to the window
            self.addMessage(self.win3,stringo,(maxes[0]+2,maxes[1]-2),inipos,i)
            #self.win3.addstr(ypos,2,'Artist : '+itemo['artist'])
            #self.win3.addstr(ypos+1,2,'Song : '+itemo['song'])
            #ypos = ypos + 3

            i = i+1
        #we save stringo list in cache
        self.saveInCache(3,stringoList)

        #refresh to show new values
        self.win3.refresh()
        
        #we now look for news and tweets about users top artists
        try:
            t3 = threading.Thread(target=self.checkTweets)
            t3.start()
        except Exception as e:
            logging.error(str(e))

        self.getNews()

    def getNews(self):
        #For this we use scraping/scraper.py and beautiful soup with urllib which gives us a touple of the information we previously needed
        #The outputing algorith is pretty similar to that of spotify so the explanation is the same
        logging.info("Retrieving news about artists...")
        try:
            data = json.load(open('spotify/top_artists.json'))

            stringoList = []
            i = 0
            for datum in data:
                entries = self.win2.getmaxyx()[0] / 6
                if i >= entries:
                    return
                tuplo = Scraper.scrapeNews(datum['name'])
                stringo = "Artist : "+tuplo[0]+"\nNews : \n"+tuplo[1]
                maxes = self.win2.getmaxyx()

                stringoList.append({"url":tuplo[2],"stringo":stringo})
                self.saveInCache(2,stringoList)
                currpos = (i*6+2,3)
                logging.debug("NEWSO : \n"+stringo)

                self.addMessage(self.win2,stringo,(currpos[0] +5,maxes[1] -2),currpos,i)
                i = i+1
        except Exception as e:
            logging.error(str(e))

    def checkTweets(self):
        #check tweets is also in scraping/scraper.py  and follow the same algorithm as news but now in twitter
        logging.info("Retrieving tweets about artists...")
        try:
            data = json.load(open('spotify/top_artists.json'))

            stringoList = []
            i = 0
            for datum in data:
                logging.info("Checking Tweets for : "+datum['name'])
                entries = int(self.win4.getmaxyx()[0] / 4)
                if i >= entries:
                    break

                logging.info("Tweet entries : "+str(i)+"/"+str(entries))
                tuplo = Scraper.scrapeTweets(datum['name'])
                logging.info("Tuplo retrieved : ")
                stringo = "Artist: "+tuplo[0]+"\n@"+tuplo[1]+" said:\n"+tuplo[2]
    
                stringoList.append({"url":tuplo[3],"stringo":stringo})

                currpos = (i*4+2,3)
                maxes = self.win4.getmaxyx()
                self.addMessage(self.win4,stringo,(currpos[0]+3,maxes[1]-2),currpos,i)
                self.saveInCache(4,stringoList)

                i = i + 1
        except Exception as e:
            logging.error(str(e))

    #Checks for emails
    def checkgoogle(self):
        if self.googlecredencialos !=0:
            #kinda redundant but just in case
            self.win1.clear()
            self.win1.border(0)
            #we get the credentials thet were previously stored in gmail/credentials.json
            filedir = os.path.join(self.FILE_DIR,'gmail/client_credentials.json')
            clientstuff = json.load(open(filedir))
            dicto = json.loads(self.googlecredencialos)

            #change the title to suit the email address
            self.win1.addnstr(0,1,"[Gmail Inbox _ "+dicto['id_token']['email']+']',self.win1.getmaxyx()[1]-2)
            #we get credenetials according to google
            credentialos = GoogleCredentials(dicto['access_token'],dicto['client_id'],dicto['client_secret'],dicto['refresh_token'],dicto['token_expiry'],dicto['token_uri'],dicto['user_agent'],dicto['revoke_uri'])
            #we retrieve the emails using httplib2 and google apis, but this only gives us a list of api and misc information, not the content itself therefore on the following for loop we get every email for every id 
            http = httplib2.Http()
            http = credentialos.authorize(http)
            service = build('gmail','v1',http=http)
            mails = GmailMessages.ListMessages(service,dicto['id_token']['email'],'in:inbox is:unread -category:(promotions OR social)')
            
            #i and stringoList work as always
            i=0
            stringoList = []
            
            #this simply tests if there are no emails or there is some issue with the mail dictoinary 
            '''try:
                logging.log("Mail Snippet : "+mails[0]['snipppet'])
            except Exception as e:
                self.win1.addstr(2,2,"No new Mails were found")
                self.win1.refresh()
                return'''

            for item in mails:
                stringo = ''
                #get individual email
                indmessage = GmailMessages.getIndividualMessage(service,dicto['id_token']['email'],item['id'])

                #this whole bunch is just getting the headers and appending them to stringo 
                headerswanted = ('From','Subject','Date')
                headersdicto = indmessage['payload']['headers']
                for header in headersdicto:
                    for wanted_header in headerswanted:
                       if wanted_header == header['name']:
                            if stringo == '':
                                stringo = header['name']+' : '+header['value']
                            else:
                                stringo = stringo +'\n'+header['name']+' : '+header['value']
                
                #we finally append the email snippper(summary) to stringo 
                stringo = stringo + '\n'+indmessage['snippet']
                stringoList.append({"url":"https://mail.google.com/mail/u/0/#inbox/"+item['id'],"stringo":stringo})
                #print message
                #for thread safety
                if self.DISPLAYON == False:
                    return()
                maxes = self.win1.getmaxyx()
                amount_of_entries = int(maxes[0] / 6)
                inipos = (i*6+2,3)
                
                #save Stringo In Cache
                self.saveInCache(1,stringoList)
                if i > amount_of_entries:
                    return
                self.addMessage(self.win1,stringo,(inipos[0]+5,maxes[1]-2),inipos,i)
                i = i+1
    '''This function makes sure that the item we give it will be printed within the bounds that we set it, specially made for them to not cause trouble for the windows '''
    def addMessage(self,window,message,maxes,inipos,index):
        if self.DISPLAYON == False:
            return
        #we add some sort of index for every entry, this way it is easy to click the number to open the url 
        try:
            if index >= 0 and window.getyx()[0] < window.getmaxyx()[0]:
                logging.debug("NUM YO : "+str(index))
                window.addstr(inipos[0],inipos[1]-2,str(index+1)+')')
        except Exception as e:
            logging.error("ADD MESSAGE ERROR : "+str(e))
        #counter used to count the amount of characters of the string printed
        counter = 0

        #we go row by row column by column printing characters until otherwise not required
        for y in range(inipos[0],maxes[0]):
            #we use a while loop here because we want to skip twice in case of a wide or full width character(such as chinese)
            x = inipos[1]
            while x < maxes[1]:
                #check that everything is in order, otherwise abort this function or loop
                currpos = window.getyx()
                if x >= maxes[1] or counter >= len(message) or y >= maxes[0]:
                    return
                if message[counter] == '\n':
                    counter = counter + 1
                    break
                elif message[counter] == '\0' or window.getyx()[0] >= window.getmaxyx()[0] -1:
                    return
                #when past all requirements we try to print
                try:
                    #status means if the character we are about to print is full width, wide or medium. This is used to check how much space a romanized or chinese character takes in the screen
                    status = unicodedata.east_asian_width(message[counter])
                    window.addch(y,x,message[counter])
                except Exception as e:
                    logging.debug("Exception : "+str(y)+"/"+str(window.getmaxyx()[0])+"__"+str(x)+"/"+str(window.getmaxyx()[1])+"__"+str(counter)+"/"+str(len(message)))
                    logging.error("ADDME\n"+str(e))
                #Again, if the character is big we add twice to x
                if status == 'W' or status == 'F':
                   x = x+1
                x = x+1
                counter = counter + 1

        window.refresh()
    
    '''After we get an a dictionary or list of information we take such information and dump it into a 
    json file for caching . In the event of a resize of terminal or such we shall pull from this file instead of the internet to re-render our information into the UI'''
    #TODO The recovering process is still not implemented and therefore not working
    def saveInCache(self,pos,dicto):
        try:
            logging.info("Saving in cache with pos : "+str(pos))
            
            #we open the file twice, once to read, another time to overwrite
            '''If there existed json string in the file then we make into a list/dictionary and then overwrite it with whats new to the save it in the same file '''
            data = self.JsonFileToDict("cache.json")
            with open("cache.json","w") as outfile:
                if data == None:
                    logging.info("Data is empty")
                    data = {}
                data[int(pos)] = dicto
                json.dump(data,outfile)
        except Exception as e:
            logging.error("SavingInCache Exception : "+str(e))

    #We make sure the file is json compatible or exists otherwise return None
    def JsonFileToDict(self,filostring):
        try:
            dicto = json.load(open(filostring))
            return dicto
        except ValueError as e:
            logging.error("JsonFileToDict JSON ERROR : "+str(e))
            return None
        except IOError as e:
            logging.error("JsonFileToDict File Not Found : "+str(e))
            return None
    

#run the program 
screeno = MainScreen()
