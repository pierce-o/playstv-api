
# playstv-api

An unofficial API designed and built in python and aims to interact with the plays.tv service with multiple aspects of the website. 
# Usage
The usage is very simple and will start with importing the library and then creating an new object with the `PlaysTV` class

```python
from playstvapi import *
```
Then to create a new instance of the playstv object you will need to have this. The constructor takes 2 arguments, the username and the password of the account you are trying to login to. 
```python
playstv = PlaysTV( 'username', 'password' )
```
This will log the user in but wont extract the data from the returned JSON object, so the next thing to do is to get the information out of the JSON object and is done like so.
```python
playstv.get_data_from_login_response()
```
That's all that needs to be done to setup the base for your project and the functions can then be accessed from the playstv object.

# Documentation
## Misc Functions
### login
This function will take a username and password and attempt to log the user in to the website. The function will return the JSON object from logging in which holds information like user_id, display name, and other useful values.
### get_my_id
This function will return the user_id that was saved after `get_data_from_login_response` was called. 
### get_data_from_login_response
This function will take all the useful data from the login response and save it to individual variables within the PlaysTV object. This will return true if the login information retcode was 0, which means that the user has logged in successfully.
### get_nonce
This will return the unique nonce that is created when a user logs into the website. This nonce is tied to certain cookies linking it to only be used on your account in that session. This information is stored as an attribute in any page on the website under the `<html>` element in a JSON format.
### get_profile_information
This will send a request to get information from a users profile, by user_id not username, and will return a JSON object that contains information about the user, user_id and more, as well as the recently, top 12, videos uploaded by the user.
### get_public_videos
This function will return a JSON object that contains all the relevant data about all the videos video. This can have a high number of videos as by default it will get ALL public videos however, if you only want to get a certain amount of videos there is a second argument that defaults at 99999.
### get_private_videos
This function is the same as `get_public_videos` but will get the private videos instead.
### phrase_video_json
This function will go through all the found videos from the get_x_videos JSON object and extract all the relevant information needed to find a video. This will return an array of `VideoData` objects.
## User Functions
### get_user_id
This function will return a user_id, a unique identification id for a user, and this will take a username as an argument.
### follow_user and unfollow_user
This function will send a request to follow/unfollow a user from their user_id which is taken as an argument and will return true if it has successfully executed.
### block_user and unblock_user
This function will send a request to block/unblock a user from their user_id which is taken as an argument and will return true if it has successfully executed.
### mute_user and unmute_user
This function will send a request to mute/unmute a user from their user_id which is taken as an argument and will return true if it has successfully executed.
### friend_request_user
This function will send a request to friend a user from their user_id which is taken as an argument and will return true if it has successfully executed.
### cancel_friend_request_user
This function will send a request to cancel a friend request for a user from their user_id which is taken as an argument and will return true if it has successfully executed.
### friend_request_accept_user
This function will accept friend request from a user using their user_id which is taken as an argument and will return true if it has successfully executed.
### unfriend_user
This function will unfriend a user from your account using their user_id which is taken as an argument and will return true if it has successfully executed.
## Comment Functions
### create_comment
This function will create a comment on a video by taking it's feedid and the message you want to send. This will return true if it has successfully executed.
### delete_comment
This function will delete a comment on a video by taking it's comment id and will return true if it has successfully executed.
### like_comment
This function will like a comment on a video by taking it's comment id and feedid which will return true if it has successfully executed.
### report_comment
This function will report a comment on a video by taking it's comment id and will return true if it has successfully executed.
### get_comment
This function will get the comment text from a comment by taking it's comment id and will return true if it has successfully executed.
## Account Functions
### account_update
This is the main function for account details and shouldn't be called directly if only one specific things needs to be changed as there are functions for that. 
### account_update_email
This will update the users email from the old one to which ever email is passed to the function.
### account_update_password
This function takes two arguments old password and the new password then send a request to update it.
### account_update_quote
This will take one argument which is the new quote which is also know as the bio on the users profile.
### account_reset_password_email
This function will send a request to send a password reset email.
### account_validate_username and account_validate_email
These functions will check if a username or email is already assigned to an account.
## Video Functions
### repost_video
This function will take the feed id of a video then repost the video onto your feed for other users who follow you to see.
### react_to_video
This will create a reaction to a video which takes two arguments one for the feed id of the video and the second is the emoji. An example of what the second argument is, `:heart:` will be ❤️.
### set_privacy_video
This will change the privacy of a video and takes two arguments one is the feed id of the video and the second is the privacy sate. 0 is for public and 1 is for private.
### edit_video_description
This will change the title of an uploaded video and takes two arguments, the feed id and the new description.
### get_video_meta
This will return information about an uploaded video such as length, time uploaded, the file url, feed id, and description. This takes on argument which is the feed id of a video.
### get_who_liked_video
This function will return a JSON object of who has liked a video and takes one argument which is the feed id.
### delete_video
This function will send a request to delete a video and takes one argument which is the feed id of the video that wants to be deleted.
