from apiclient import errors
import json 
class GmailMessages:
    def ListMessages(service,user_id,query=''):
        labelIds = ['INBOX']
        try:
            response = service.users().messages().list(userId=user_id,q=query,maxResults=8).execute()
            messages =[]
            if 'messages' in response:
                messages.extend(response['messages'])
            '''while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                reponse = service.users().messages().list(userId=user_id,q=query,pageToken=page_token,labelIds = labelIds).execute()
                messages.extend(response['messages'])'''
            with open("gmails.txt","w") as outfile:
                json.dump(response,outfile)
            return messages
        except errors.HttpError as e:
            print("There was this exception : "+str(e))
    def getIndividualMessage(service, user_id,msg_id):
        try:
            message = service.users().messages().get(userId=user_id,id=msg_id,format="full").execute()
            return message
        except errorrs.HttpError as error:
            print("The following exceptiion occured : "+str(error))
        
