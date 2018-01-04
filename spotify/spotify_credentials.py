import json, requests, webbrowser, urllib
import spotipy
import sys
import spotipy.util as util
class SpotifyCredentials:
    client_id = '71c7ec8e05c94d49ba93e635866ec7a7'
    client_secret = 'f3aea0f317fb44209be782fd9c92f5df'
    redirect_uri = "http://localhost:8888/callback"

    authorize_url = 'https://accounts.spotify.com/authorize'

    def __init__ (self):
        print("Puto el que lo lea")

    def authorize(self,client_id,response_type,redirect_uri,state):
        Vauthorize_url = 'https://accounts.spotify.com/authorize/?'
        client_id = '71c7ec8e05c94d49ba93e635866ec7a7'
        #client_id = self.client_id
        payload = {'client_id':client_id,'response_type':response_type,'redirect_uri':redirect_uri}
        #webbrowser.open_new_tab(authorize_url,
        encoded = urllib.parse.urlencode(payload)
        webbrowser.open_new_tab(authorize_url+encoded)

    def getToken(self,username,scope):
        token = util.prompt_for_user_token(username,scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri)
        return token
    def Testo(self,token):
        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks()
            for item in results['items']:
                track = item['track']
                print(track['name']+ ' - '+track['artists'][0]['name'])
