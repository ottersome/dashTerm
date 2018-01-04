from spotify_credentials import SpotifyCredentials

print("Hello There")
spoti = SpotifyCredentials()
token = spoti.getToken('abuklao','user-read-private user-read-email user-library-read')
spoti.Testo(token)
