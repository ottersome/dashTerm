import json, requests, urllib
import spotipy
import spotipy.util as util
import os

class SpotifyTransactions:
    ARTIST_LIMIT = 5
    OFFSET = 0
    TIME_RANGE = 'short_term'
    RECOMM_URL = 'https://api.spotify.com/v1/recommendations'
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))


    def getTopArtists(self,token,infolist):
        if token:
            returnList = []
            sp = spotipy.client.Spotify(auth=token)
            results = sp.current_user_top_artists(limit=self.ARTIST_LIMIT,offset=self.OFFSET,time_range=self.TIME_RANGE)
            for item in results['items']:
                tempdict = {}
                for item2 in item:
                    if type(item2) is str:
                        if item2 in infolist:
                            tempdict[item2] = item[item2]

                returnList.append(tempdict)
            
            with open(os.path.join(self.FILE_DIR,'top_artists.json'),'w') as outfile:
                json.dump(returnList,outfile)
            return returnList
        return None
    def recommendations(self,token,artisturi_list,limit):
        #check if format correction is needed
        if (artisturi_list[0].find(':')) > 0:
            for item in artisturi_list:
                artisturi_list[artisturi_list.index(item)] = item.split(':')[2]

        returnList = []
        final_url = self.RECOMM_URL+'?seed_artists='+','.join(artisturi_list)+'&limit=10'
        response = requests.get(final_url, headers={'Authorization':'Bearer '+token})
        recomends = response.json()
        for item in recomends['tracks']:
            returnList.append({'artist':item['artists'][0]['name'],'song':item['name'],'url':item['external_urls']['spotify']})
        return returnList




