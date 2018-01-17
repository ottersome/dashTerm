from spotify_credentials import SpotifyCredentials
from spotify_transactions import SpotifyTransactions
import json
from spotipy.oauth2 import SpotifyClientCredentials
print("Hello There")
spoti = SpotifyCredentials()
#scc = SpotifyClientCredentials(client_id=spoti.client_id,client_secret=spoti.client_secret)
#token =  scc.get_access_token()
name = input("Please input your username : ")
token = spoti.getToken(name,'user-read-private user-read-email user-library-read user-top-read')
spotra = SpotifyTransactions()
infolist = ('name','uri')
uri_list = []
top_artists = spotra.getTopArtists(token,infolist)
for item in top_artists:
    uri_list.append(item['uri'])
reco = spotra.recommendations(token,uri_list,5)
for itemo in reco:
    print("Artist : "+itemo['artist']+"  Song: "+itemo['song'])
