import requests
from lxml import html
from lxml import etree
import json

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

    saved_cookies = {}

    # Constructor will log the user in by default
    def __init__( self, username, password ):

        r = requests.post( self.baseurl + 'login', data={ 'urlname': username, 'pwd': password, 'format': 'json' } )

        if(r.status_code == 200): # The request was successfully sent
            self.login_information = r.json()
            
            for cookie in r.cookies:
                self.saved_cookies[cookie.name] = cookie.value


    # Logs a users in and returns the json response
    def login(self, username, password ):

        r = requests.post( self.baseurl + 'login', data={ 'urlname': username, 'pwd': password, 'format': 'json' } )

        if(r.status_code == 200): # The request was successfully sent
            self.saved_cookies = r.cookies
            return r.json()

    # Returns your own, currently logged in account, user id
    def get_my_id(self):
        return self.user_id

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

    # Gets the nonce and the updates the cookies
    def get_nonce(self):

        # Request to get the playtv home page with the cookies so that it knows we are logged in
        r = requests.get( 'https://plays.tv/home', cookies=self.saved_cookies )

        # Update any cookies that have changed
        for cookie in r.cookies:
            self.saved_cookies[cookie.name] = cookie.value

        # In the html element there is an attribute called data-conf and it contains a json structure which holds the updated nonce

        page = html.fromstring( r.content )

        json_attribute = page.xpath("/html/@data-conf")

        json_unk =  json.loads( json_attribute[0] )

        return json_unk['login_user']['nonce']

    # Gets information of a users profile
    def get_profile_information(self, userid):

        r = requests.get( self.baseurl + 'orbital/profile/' + userid )

        # Make sure the get request was successful
        if(r.status_code == 200):
            return r.json()
        else:
            return None

    # Get all of the a users videos, currently only the logged in user, which are public
    def get_public_videos(self, userid):
        
        r = requests.get( self.baseurl + 'orbital/videos?user_id=' + userid + '&itemsPerPage=99999&videoType=regVideos' )

        # Make sure the get request was successful
        if (r.status_code == 200 ):
            return r.json()
        else:
            return None

    # Get all of the a users videos, currently only the logged in user, which are public
    def get_private_videos(self, userid):
        
        r = requests.get( self.baseurl + 'orbital/videos?user_id=' + userid + '&itemsPerPage=99999&videoType=hiddenVideos' )

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

    # All user API calls

    # Gets the user id from an inputted username
    def get_user_id( self, username ):

        # Get the search page for people with the username entered
        r = requests.get( 'https://plays.tv/explore/people?search=' + username )

        page = html.fromstring( r.content )

        # Find the list element that contains all the found accounts
        result = []
        for user in page.xpath("//li[@class='user-item ']"):
            result = result + user.xpath('@data-user-id')

        found_user_id = None

        # Loop through all the found list elements looking for the correct user
        for user in result:
            # Get the information of the user from their profile then compare the name to the one entered
            if(self.get_profile_information( user )['data']['user']['name'] == username):
                found_user_id = user # If both names match then set the found user id to the current itteration and exit the loop
                break

        return found_user_id # Return the found ID

        #r = requests.post( self.baseurl + 'user/' + username ) The correct/better method of getting the user ID but there are unknown arguments

    # Sends a request to follow a user from their ID
    def follow_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/follow', data={ 'obj_type': 'user', 'obj_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ): 
            return True
        else:
            return False

    # Sends a request to unfollow a user from their ID
    def unfollow_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/unfollow', data={ 'obj_type': 'user', 'obj_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to block a user from their ID
    def block_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/block', data={ 'user_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to unblock a user from their ID
    def unblock_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/unblock', data={ 'user_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to mute a user from their ID
    def mute_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/mute', data={ 'user_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to unmute a user from their ID
    def unmute_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/unmute', data={ 'user_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to friend a user from their ID
    def friend_request_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/friend_request', data={ 'obj_type': 'user', 'obj_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False

    # Sends a request to cancle friend request to a user from their ID
    def cancle_friend_request_user(self, user_id):

        # Send a post request with an updated nonce and corresponding cookies
        r = requests.post( self.baseurl + 'user/friend_cancel_request', data={ 'obj_type': 'user', 'obj_id': user_id, "nonce": self.get_nonce() }, cookies=self.saved_cookies )

        # Check if it was successfully executed
        if( r.status_code == 200 ):
            return True
        else:
            return False