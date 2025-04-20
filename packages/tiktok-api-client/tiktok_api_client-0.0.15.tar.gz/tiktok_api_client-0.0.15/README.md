
# TikTok Open API Client

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-3819/)

This Python library provides a convenient way to interact with the TikTok Open API for authorization and publishing video and photo content. It handles the OAuth 2.0 authorization flow with PKCE and offers methods for posting videos (from file or URL) and photos.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Basic Usage](#basic-usage)
  - [Posting a Video from a URL](#posting-a-video-from-a-url)
  - [Posting a Photo](#posting-a-photo)
- [Class Overview](#class-overview)
  - [`TikTok(client_key, client_secret, redirect_uri, state="", scopes=None)`](#tiktokclient_key-client_secret-redirect_uri-state-scopesnone)
  - [Methods](#methods)
- [Available Scopes](#available-scopes)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- **OAuth 2.0 Authorization:** Implements PKCE (Proof Key for Code Exchange) flow for secure authentication
- **Token Management:** Handles authorization code exchange, token refresh, and revocation
- **Content Publishing:** Supports both video and photo posts
- **Creator Information:** Retrieves details about the authenticated TikTok creator
- **Upload Status:** Tracks video upload progress
- **Error Handling:** Includes custom exceptions for various error scenarios

## TikTok Documentation
- [TikTok Developers](https://developers.tiktok.com)
- [TikTok Content Posting API - Get Started](https://developers.tiktok.com/doc/content-posting-api-get-started?enter_method=left_navigation)


## Installation

```bash
pip install tiktok-api-client
```

## Getting Started

### Prerequisites
You'll need these credentials from your TikTok developer portal:
- Client Key
- Client Secret 
- Redirect URI (must be registered in your developer portal)

### Basic Usage

## Available Scopes

```python
SCOPES = [
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats",
]
```

Pass a subset of these scopes to the `scopes` parameter when initializing the client.

Initialize the client and get authorization URL:

```python
from tiktok_api_client import TikTok

# Initialize client
tik = TikTok(
    client_key="your_client_key",
    client_secret="your_client_secret",
    redirect_uri="https://your-app.com/callback", use ngrok for testing
    state={"user_id": "user1"},  # Optional tracking state
    scopes=["video.publish", "user.info.basic"]
)

# Get authorization URL
auth_url = tik.get_authorization_url()
print(f"Authorize URL: {auth_url}")

https://www.tiktok.com/v2/auth/authorize/?client_key=sbaw0y8rutbd9qx3i1&response_type=code&scope=video.publish&redirect_uri=https%3A%2F%2Fyour-app-url.comp%2Fcallback&code_challenge=zzq1--trJ8aXxqsddsdsdsdrWCaatTBx4&state=%7B%27user_id%27%3A+%mami%27%2C+%name%27%3A+%27hello%27%7D&code_challenge_method=S256
# visit the endpoint to authentiicate Tiktok on the browser
```

### Authorization Flow Notes

1. The authorization process generates a `code_verifier` stored in `tik.code_verifier`
2. You must store this code verifier along with your state parameters for later verification
3. After user authorization, TikTok redirects to your callback URL with an authorization code

Example callback response:
```json
{
  "code": "9xmQgPZMUTvILmosta-4eC-PXLGFRgjdzXspg2ybTc2AKGDt...",
  "scopes": "user.info.basic,video.publish",
  "state": "{'user_id': user1'}
}
```



### Exchanging Authorization Code for Tokens

```python
# Exchange code for tokens
# You can track your save info from the state returned earlier then, retrive code_verifier
# reinitialize tiktok in session or continue with previous instance if testing on terminal
tik = TikTok(
    client_key="your_client_key",
    client_secret="your_client_secret",
    redirect_uri="https://your-app.com/callback",
)
tik.code_verifier = code_verifier #saved earlier
token_data = tik.exchange_code_for_token(code=code)
print("Access Token:", token_data["access_token"])
print("Refresh Token:", token_data["refresh_token"])

```

Example token response:
```json
{
  "access_token": "act.UD0znPSOyqFgRJVvF9Tr2Xc5bJYjOnRiGPpsvNxb1TX...",
  "expires_in": 86400,
  "open_id": "-000bMhnTFeW4SZCPZkPWZppArDnsFgvOa_f",
  "refresh_expires_in": 31536000,
  "refresh_token": "rft.BDkTqoVTZZm9kLAtll3Rf2JQq5vwlvy9XR3KvbQEIM...",
  "scope": "user.info.basic,video.publish",
  "token_type": "Bearer"
}
```

### Token Management

- Store both access and refresh tokens securely
- Refresh tokens hourly using a cron job:
  ```python
  tik.refresh_access_token()  # Uses stored refresh token
  # Or specify manually:
  tik.refresh_access_token(refresh_token="your_refresh_token")
  ```

- Revoke tokens when needed:
  ```python
  tik.revoke_access_token()
  ```

### Getting Creator Information

```python
creator_info = tik.get_creator_info()
```

Example response:
```json
{
  "data": {
    "duet_disabled": true,
    "max_video_post_duration_sec": 3600,
    "privacy_level_options": [
      "FOLLOWER_OF_CREATOR",
      "MUTUAL_FOLLOW_FRIENDS",
      "SELF_ONLY"
    ],
    "stitch_disabled": true,
    "comment_disabled": false,
    "creator_avatar_url": "https://p16-pu-sign-no.tiktokcdn-eu.com/...",
    "creator_nickname": "username",
    "creator_username": "userhandle"
  },
  "error": {
    "code": "ok",
    "message": "",
    "log_id": "2025041606EF40DB44655DE1236366E029"
  }
}
```

## Content Publishing

### Video Upload Options

There are two upload methods:
1. **Direct Post**: Publishes immediately to public view
2. **Upload**: Saves to draft folder

Required parameters:
- `title`
- `source` (either `FILE_UPLOAD`, `PULL_FROM_URL`)
- `upload_type` (e.g., `POST_VIDEO_FILE`, `UPLOAD_VIDEO_FILE`, `POST_VIDEO_URL` or `UPLOAD_VIDEO_URL`)

### Posting a Video

```python
# From local file, FOR DIRECT UPLOAD
response = tik.create_video(
    title="Hello World",
    source="FILE_UPLOAD", 
    upload_type="POST_VIDEO_FILE",
    privacy_level="SELF_ONLY",
    video_path="/path/to/video.mp4", #FROM LOCAL FILE SYSTEM
    # OPTIONAL PARAMETERS
    disable_comment=False,
    disable_duet=False,
    disable_comment=False,
    disable_stitch=False,
    video_cover_timestamp_ms=1000
)
```

Example response:
```json
{"initial_response": {"data": {"publish_id": "v_pub_file~v2-1.7493784938978805793",
   "upload_url": "https://open-upload-i18n.tiktokapis.com/upload?upload_id=7497888937493822177&upload_token=4534354-c51c-b4ef-0d67-svsdvsdvs"},
  "error": {"code": "ok",
   "message": "",
   "log_id": "20250415DB4C60556301E49832D8623D21"}},
 "final_response": None}
```

```python
# From URL
response = tik.create_video(
    title="Remote Video",
    source="PULL_FROM_URL",
    upload_type="POST_VIDEO_URL",
    privacy_level="SELF_ONLY",
    video_url="https://your-url.com/video.mp4"
)
```

Example response:
```json
{
  "data": {
    "publish_id": "v_pub_url~v2-1.7493775763519964616"
  },
  "error": {
    "code": "ok",
    "message": "",
    "log_id": "20228DFF6051832504CD7615187FE36718"
  }
}
```

These methoss requires your app verified by tiktok before use:

```python
tik.create_video(title='hello', source='PULL_FROM_URL', upload_type="UPLOAD_VIDEO_URL", privacy_level="SELF_ONLY", video_url='https://your-url.com/files/video.mp4')
tik.create_video(title='hello', source='FILE_UPLOAD', upload_type="UPLOAD_VIDEO_FILE", privacy_level="SELF_ONLY", video_path='/path/to/video.mp4')

# "unaudited_client_can_only_post_to_private_accounts","message":"Please review our integration guidelines at https://developers.tiktok.com/doc/content-sharing-guidelines/
```


### Photo Upload

```python
# Direct post
response = tik.create_photo(
    title="My Photos",
    post_mode="DIRECT_POST",
    privacy_level="SELF_ONLY",
    photo_images=[
        "https://example.com/photo1.png",
        "https://example.com/photo2.png"
    ]
)
```

Example response:
```json
{"photo_upload_response": {"data": {"publish_id": "p_pub_url~v2.43534534563534534"},
"error": {"code": "ok",
 "message": "",
 "log_id": "7CTFGVO483OOOOOOOOOOOO4"}}}
```

```python
# Save to draft
response = tik.create_photo(
    title="Draft Photos",
    post_mode="MEDIA_UPLOAD",
    privacy_level="SELF_ONLY",
    photo_images=[
        "https://example.com/photo1.png"
    ]
)
# "unaudited_client_can_only_post_to_private_accounts","message":"Please review our integration guidelines at https://developers.tiktok.com/doc/content-sharing-guidelines/
```


### Checking Upload Status

```python
status = tik.check_upload_status(publish_id="your_publish_id")
```

## Class Reference

### `TikTok(client_key, client_secret, redirect_uri, state="", scopes=None)`

Constructor parameters:
- `client_key`: Your application's client key
- `client_secret`: Your application's client secret  
- `redirect_uri`: Registered callback URI
- `state`: Optional CSRF protection string/dict
- `scopes`: List of requested API scopes

### Methods

- `get_authorization_url() -> str`
- `exchange_code_for_token(code: str) -> dict`
- `refresh_access_token(refresh_token: str = None) -> dict`
- `revoke_access_token(access_token: str = None) -> dict`
- `get_creator_info() -> dict`
- `create_video() -> dict`
- `create_photo() -> dict`
- `check_upload_status() -> dict`

## Available Scopes

```python
[
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats"
]
```

## Error Handling

The library throws these exceptions:
- `TimeoutError` for request timeouts
- `HTTPError` for HTTP-related issues
- General `Exception` for OAuth errors

Always use try-catch blocks for reliability.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## License

MIT License. See [MIT License](https://en.wikipedia.org/wiki/MIT_License) for details.
