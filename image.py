from unsplash.api import Api
from unsplash.auth import Auth

client_id='84c984e533a3c128505b3f8869343ad73576a5628704a18448ac427ee1d86532'
client_secret='33288ae12c99a8847d6cdffe309a5516dfba568e8c21a6910ff5489469e7602d'
redirect_uri='urn:ietf:wg:oauth:2.0:oob'
code=''

auth=Auth(client_id, client_secret, redirect_uri, code=code)
api=Api(auth)

image = api.photo.random()
print(image[0])
