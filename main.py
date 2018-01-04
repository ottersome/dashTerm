import sys
import curses
from gmail.gmail_credentials import * 
from curses import wrapper
from apiclient.discovery import build
from gmail.gmail_mails import GmailMessages
from oauth2client.client import GoogleCredentials
import httplib2
class MainScreen:

    win1=None
    win2=None
    win3=None
    stdscr=None

    def __init__(self):
        wrapper(self.firstSetup)
    
    def firstSetup(self,stdscr):
        self.stdscr = stdscr
        three_col_w = int(curses.COLS/3)
        self.win1= curses.newwin(curses.LINES,three_col_w,0,0)
        self.win2 = curses.newwin(curses.LINES,three_col_w,0,three_col_w)
        self.win3 = curses.newwin(curses.LINES,three_col_w,0,three_col_w*2)
        self.stdscr.clear()
        self.win1.border(0)
        self.win2.border(0)
        self.win3.border(0)
        self.win2.addstr(0,1,"Welcome to DashTerm")
        self.win1.addstr(0,1,"Gmail Inbox")

        self.stdscr.refresh()
        self.win1.refresh()
        self.win2.refresh()
        self.win3.refresh()
        self.checkgoogle()
        x = stdscr.getch()

    def checkgoogle(self):
        credencialos = get_stored_credentials(1)
        if credencialos !=0:
            clientstuff = json.load(open('./gmail/client_credentials.json'))
            dicto = json.loads(credencialos)
            self.win1.addstr(0,1,"[Gmail Inbox _ "+dicto['id_token']['email']+']')
            credentialos = GoogleCredentials(dicto['access_token'],dicto['client_id'],dicto['client_secret'],dicto['refresh_token'],dicto['token_expiry'],dicto['token_uri'],dicto['user_agent'],dicto['revoke_uri'])
            http = httplib2.Http()
            http = credentialos.authorize(http)
            service = build('gmail','v1',http=http)
            mails = GmailMessages.ListMessages(service,dicto['id_token']['email'],'in:inbox is:unread -category:(promotions OR social)')

            mailcounter = 0
            for item in mails:
                indmessage = GmailMessages.getIndividualMessage(service,dicto['id_token']['email'],item['id'])
                #print(json.dumps(indmessage, sort_keys=True, indent=4, separators=(',', ': ')))
                headerswanted = ('From','Subject','Date')
                headersdicto = indmessage['payload']['headers']
                localcounter = 0
                for incomehead in headersdicto:
                    for want in headerswanted:
                        if incomehead['name'] == want:
                            localcounter = localcounter + 1
                            ypos = localcounter + (mailcounter*4)
                            if ypos >= curses.LINES-3:
                                return
                            self.win1.addstr(2+ypos,2,want +':'+incomehead['value'])
                            self.win1.refresh()
                mailcounter = mailcounter + 1


            

screeno = MainScreen()
