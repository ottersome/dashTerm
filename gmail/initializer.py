from gmail_credentials import exchange_code, get_authorization_url,get_user_info,get_credentials,get_stored_credentials
from apiclient.discovery import build
from gmail_mails import GmailMessages
from oauth2client.client import GoogleCredentials
import webbrowser
import json
import httplib2
class GmailManger:

    news = input("You want a new boi ?\n")
    credencialos = get_stored_credentials(1)
    if credencialos == 0:
        email = input("Please input your email\n")
        url = get_authorization_url(email,"")
        webbrowser.open(url)
        authorization = input("Please input the authorization code given\n")
        credentials = get_credentials(authorization,"holis")
        #storage.put(Credentials)
        #credentials = storage.get()

        print("Credentials : \n"+credentials.to_json())
        userinfo = get_user_info(credentials)
        print("Printing info...")
        for infotas in userinfo:
            print(str(infotas)+' - '+str(userinfo[infotas]))

        webbrowser.open(userinfo['link'])
    else:
        #client stuff
        clientstuff = json.load(open('./client_credentials.json'))


        dicto = json.loads(credencialos)
        print(dicto['id_token']['email'])
        credentialos = GoogleCredentials(dicto['access_token'],dicto['client_id'],dicto['client_secret'],dicto['refresh_token'],dicto['token_expiry'],dicto['token_uri'],dicto['user_agent'],dicto['revoke_uri'])
        #credentialos = AccessTokenCredentials(dicto['access_token'],'my-user-agent/1.0')
        #http_auth = credentialos.authorize(Http())
        http = httplib2.Http()
        http = credentialos.authorize(http)
        service = build('gmail','v1',http=http)
        mails = GmailMessages.ListMessages(service,dicto['id_token']['email'],'in:inbox is:unread -category:(promotions OR social)')
        for item in mails:
            indmessage = GmailMessages.getIndividualMessage(service,dicto['id_token']['email'],item['id'])
            #print(json.dumps(indmessage, sort_keys=True, indent=4, separators=(',', ': ')))
            headerswanted = ('From','Subject','Date')
            headersdicto = indmessage['payload']['headers']
            for ito in headersdicto:
                for want in headerswanted:
                    if ito['name'] == want:
                        print(want +':'+ito['value'])
            print('\n')
