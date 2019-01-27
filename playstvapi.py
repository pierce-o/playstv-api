import requests

# A class to store the minimum information we need about a video to be able to identify it
class VideoData:

    feedid = None
    videoid = None
    description = None
    server = None

    # Constructor
    def __init__( self, feedid, videoid, description, server ):
        self.feedid = feedid
        self.videoid = videoid
        self.description = description
        self.server = server

# Main class for the api
class PlaysTV:

    baseurl = 'https://plays.tv/ws/' # All api calls go to this address

    # Stores all the json information returned from the login response
    login_information = None

    # All the relevent information that we can get from the login_information
    user_id = None
    display_name = None
    email = None
    json_web_token = None

    # Constructor will log the user in by default
    def __init__( self, username, password ):

        r = requests.post( self.baseurl + 'login', data={ 'urlname': username, 'pwd': password, 'format': 'json' } )

        if(r.status_code == 200): # The request was successfully sent
            self.login_information = r.json()

    # Logs a users in and returns the json response
    def login(self, username, password ):

        r = requests.post( self.baseurl + 'login', data={ 'urlname': username, 'pwd': password, 'format': 'json' } )

        if(r.status_code == 200): # The request was successfully sent
            return r.json()

    # Takes the revelent data from the login and stores it in the variables
    def get_data_from_login_response(self):
        if( self.login_information['retcode'] == 0 ): # Login was successful
            data = self.login_information['data']

            self.user_id = data['userId']
            self.display_name = data['displayName']
            self.email = data['email']
            self.json_web_token = data['jwt']

            # Successfully set all of the revelent information so return true
            return True
        else:
            # There was an error when logging in most likely wrong password so return false
            return False

    # Gets information of a users profile
    def get_profile_information(self):

        r = requests.get( self.baseurl + 'orbital/profile/' + self.user_id )

        # Make sure the get request was successful
        if(r.status_code == 200):
            return r.json()
        else:
            return None

    # Get all of the a users videos, currently only the logged in user, which are public
    def get_public_videos(self):
        
        r = requests.get( self.baseurl + 'orbital/videos?user_id=' + self.user_id + '&itemsPerPage=99999&videoType=regVideos' )

        # Make sure the get request was successful
        if (r.status_code == 200 ):
            return r.json()
        else:
            return None

    # Get all of the a users videos, currently only the logged in user, which are public
    def get_private_videos(self):
        
        r = requests.get( self.baseurl + 'orbital/videos?user_id=' + self.user_id + '&itemsPerPage=99999&videoType=hiddenVideos' )

        # Make sure the get request was successful
        if (r.status_code == 200 ):
            return r.json()
        else:
            return None

    # Create an array of VideoData object which only store the relevent data that we need for the video
    def phrase_video_json(self, json):

        videos = json['data']

        # Create a empty array
        saved_videos = []

        for video in videos:
            videoId = video['videoUrl'][36:47] # Take the video ID which the server uses to save all the information about it e.g. video, thumbnails 
            saved_videos.append( VideoData( video['feedId'], videoId, video['description'], video['videoUrl'][2:29] ) ) # Append a new object to the end of the array

        # Return the array populated or not
        return saved_videos
