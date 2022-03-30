import codecs
import os
import shutil
import urllib.request
import tweepy
import time

from pathlib import Path
from instagram_private_api import Client
from collections import namedtuple
from xml.dom.minidom import parseString

INSTA_USERNAME = 'jkt48.zee'
INSTA_ID       = '9144760144'

def absPath(path):
    return str(Path(__file__).resolve().parent.joinpath(path))

def fetchStory():
    with open(absPath('config/instaAPI.txt')) as instaData:
        kuki = codecs.decode(instaData.read().encode(), 'base64')
    instaAPI = Client(INSTA_USERNAME,'', cookie=kuki)
    return instaAPI.user_story_feed(INSTA_ID)

def parseStory(userInfo):
    if userInfo['reel'] is None: return[0]
    Data = namedtuple('Story', ['type','taken_at','media_url','audio_url'])
    mediaURL = []
    for media in userInfo['reel']['items']:
        takenTS = int(media.get('taken_at'))
        if 'video_version' in media:
            videoManifest = parseString(media['video_dash_manifest'])
            videoPeriod   = videoManifest.documentElement.getElementsByTagName('Period')
            Representation= videoPeriod[0].getElementsByTagName('Representation')
            videoURL      = Representation[0].getElementsByTagName('BaseURL')[0].childNodes[0].nodeValue
            audioElement  = Representation.pop()
            if audioElement.getAttribute("mimeType") == "audio/mp4":
                audioURL  = audioElement.getElementsByTagName('Base URL')[0].childNodes[0].nodeValue
                mediaURL.append(Data('video', takenTS, videoURL, audioURL))
            else:
                mediaURL.append(Data('video', takenTS, videoURL, None))
        else:
            mediaURL.append(Data('picture', takenTS, media['image_versions2']['candidates'][-1]['url'], None))
    return mediaURL

def getTwitAPI():
    with open(absPath('config/twitterAPIAzizi.txt')) as twitData:
        ckey, csecret, tkey, tsecret = twitData.read().split('\n')
    twitAuth = tweepy.OAuthHandler(ckey, csecret)
    twitAuth.set_access_token(tkey, tsecret)
    return tweepy.API(twitAuth)

def twitMedia(filePath):
    TwitAPI = getTwitAPI()
    with open(absPath('config/instaAPI.txt')) as instaData:
        kuki = codecs.decode(instaData.read().encode(), 'base64')
    dataGET = Client(INSTA_USERNAME,'', cookie=kuki)
    try:
        Twit = TwitAPI.media_upload(filePath)
        TwitAPI.update_status(status='story baru dari ayang @A_ZeeJKT48 😘', media_ids=[Twit.media_id_string])
        if hasattr(Twit, 'processing_info') and Twit.processing_info['state'] == 'pending':
            print('Pending...')
            time.sleep(15)
        print('UPLOADING '+storyID)
        print(format(filePath))
        print('TWEETING!')
        print('SUCCESS!')
    except tweepy.errors.BadRequest as err:
        print('ERROR:', err)
        print('ERROR!')

def ReadLastTweet():
    if not os.path.exists(absPath('tempAzizi.txt')):
        return 0
    with open(absPath('tempAzizi.txt')) as file:
        read = file.read()
        timestamp = str(read)
    return timestamp

def deleteStory():
    shutil.rmtree(absPath('assetsAzizi/'))
    os.makedirs(absPath('assetsAzizi/'))
    with open('assetsAzizi/story','w') as file:
        file.write('')

while True:
    if __name__ == '__main__':
        with open(absPath('config/instaAPI.txt')) as instaData:
            kuki = codecs.decode(instaData.read().encode(), 'base64')
        dataGET = Client(INSTA_USERNAME,'', cookie=kuki)
        storyData = dataGET.user_reel_media(INSTA_ID)
        if storyData['items'] is not None:
            for i in storyData['items']:
                storyID = i['id']
                lastStory = ReadLastTweet()
                if lastStory >= str(storyID):
                    print('TWEET FOR STORY {} ALREADY SENT'.format(storyID))
                    continue
                storyGET = absPath('assetsAzizi/'+storyID+'.mp4')
                if i["media_type"] == 1:
                    time.sleep(30)
                    url = i['image_versions2']['candidates'][0]['url']
                    urllib.request.urlretrieve(url, storyGET)
                    twitMedia(storyGET)
                    with open('tempAzizi.txt','w') as file:
                        write = str(storyID)+'\n'
                        file.write(write)
                elif i["media_type"] == 2:
                    time.sleep(30)
                    url = i['video_versions'][0]['url']
                    urllib.request.urlretrieve(url, storyGET)
                    twitMedia(storyGET)
                    with open('tempAzizi.txt','w') as file:
                        write = str(storyID)+'\n'
                        file.write(write)
        else:
            print('NOT STORIES FOUND')
        deleteStory()
    time.sleep(100)