from gmail.gmail_credentials import get_stored_credentials
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
import webbrowser
import json
import httplib2

credencialos = get_stored_credentials(1)
dicto = json.loads(credencialos)
credencialos = GoogleCredentials(dicto['access_token'],dicto['client_id'],dicto['client_secret'],dicto['refresh_token'],dicto['token_expiry'],dicto['token_uri'],dicto['user_agent'],dicto['revoke_uri'])
http = credencialos.authorize(httplib2.Http())
service = build('people','v1',http=http, discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
#results = service.people().connections().list(resourceName='people/me',pageSize=10,personFields='names,emailAddresses,interests').execute()
results = service.people().get(resourceName='people/me',personFields='ageRanges,interests').execute()
connections = results.get('connections', [])
with open('data.txt','w') as outfile:
    json.dump(results,outfile)
print(connections)
for person in connections:
    names = person.get('names', [])
    if len(names) > 0:
        name = names[0].get('displayName')
        print(name)
        
