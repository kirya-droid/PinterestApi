# PinterestApi

This is a wrapper for automating your pinterest account using the Pinterest API.
## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Video Guide](#video-guide)
## Introduction

This project implements the functions of obtaining an access token, obtaining board IDs, downloading pins, downloading video pins.
## Installation
``` Ruby
git clone https://github.com/kirya-droid/PinterestApi.git
```
``` Ruby
pip install requests
```
## Usage
### Getting the Pinterest API
You need to get the Pinterest API from https://developers.pinterest.com/apps/

### Inserting Data into Your Config and Authorizing Your Application
``` python
config = {
    'client_id': 'your_client_id',
    'redirect_url': 'http://localhost:8085',
    'client_secret': 'your_client_secret'
}
pinterest_oauth = PinterestOAuth(config)
pinterest_oauth.open_auth_url()
access_token = pinterest_oauth.get_access_token()
``` 
### After Receiving the Token, You Can Publish Your Pins
``` python
token = "Your_token"
creator = PinterestPinCreator(token)
``` 
### Creating a Pin
``` python

creator.create_pin(
         board_id="your board's ID",
         description="Description of your pin",
         title="The name of your pin",
         img_url="image url",
         link="the link that your pin leads to" 
     )
``` 
### Creating a Video Pin
``` python
creator.create_video_pin(
        board_id="your board's ID",
        description="Description of your pin,
        title="The name of your pin",
        link="the link that your pin leads to",
        filepath="videoname.mp4",
        cover_image="cover video.png"
    )
```
### Getting Board ID

``` python
creator.get_boards()
```
## Video Guide

coming soon