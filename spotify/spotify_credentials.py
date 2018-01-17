import json, requests, webbrowser, urllib
import spotipy
import sys
import spotipy.util as util
class SpotifyCredentials:
    client_id = '71c7ec8e05c94d49ba93e635866ec7a7'
    client_secret = 'f3aea0f317fb44209be782fd9c92f5df'
    redirect_uri = "http://localhost:8888/callback"

    authorize_url = 'https://accounts.spotify.com/authorize'
    
    def getToken(self,username,scope):
        token = util.prompt_for_user_token(username,scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri)
        return token

