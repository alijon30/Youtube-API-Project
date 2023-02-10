from googleapiclient.discovery import  build
import csv
my_key = "AIzaSyCZEEc95w_ivN38nviyvQyfWZAtjg-eNEs"


youtube = build('youtube', 'v3', developerKey = my_key)


request = youtube.search().list(
    part = 'snippet',
    type = 'video',
    q = 'Education Technology',
    maxResults = 100
)

response = request.execute()

i = 1
with open('abc.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Description', 'Author', 'ViewCount'])

print(response)

for video in response['items']:
    title = str(i) + " " + video['snippet']['title']
    description =  video['snippet']['description']
    author =  video['snippet']['channelTitle']
    i += 1

    #scraping viewcount info from youtube API using different method
    videoID = video["id"]['videoId']
    req = youtube.videos().list(
        part='snippet,statistics',
        id=videoID
    )
    response2 = req.execute()
    viewCount = response2['items'][0]["statistics"]["viewCount"]

    print(f"{title} {description} {author} {viewCount}")
    with open('abc.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, description, author, viewCount])


nextPageToken = response.get('nextPageToken')

if nextPageToken:
    request = youtube.search().list(
        part='snippet',
        maxResults=50,
        pageToken= nextPageToken,
        q='Education Technology'
    )

    response = request.execute()

i = 51

with open('abc.csv', 'a', newline='') as f:
    writer = csv.writer(f)

for video in response['items']:
    title = str(i) + " " + video['snippet']['title']
    description =  video['snippet']['description']
    author =  video['snippet']['channelTitle']
    i += 1

    #scraping viewcount info from youtube API using different method
    videoID = video.get('id', {}).get('videoId', '')
    req = youtube.videos().list(
        part='snippet,statistics',
        id=videoID
    )
    response2 = req.execute()
    if response2['items']:
        viewCount = response2['items'][0]["statistics"]["viewCount"]
    else:
        viewCount = None

    print(f"{title} {description} {author} {viewCount}")
    with open('abc.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, description, author, viewCount])
