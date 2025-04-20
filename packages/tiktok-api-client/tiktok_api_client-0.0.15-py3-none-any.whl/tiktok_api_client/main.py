import requests, urllib.parse, base64, hashlib, secrets

try:
    from .utils import (
        TimeoutError, HTTPError, get_file, handle_response
    )
except ImportError:
    from utils import (
        TimeoutError, HTTPError, get_file, handle_response
    )



SCOPES = [
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats",
]


class TikTok:
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
    TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
    TOKEN_REVOKE_URL = "https://open.tiktokapis.com/v2/oauth/revoke/"
    AUTH_SCOPE = ["video.publish"]
    VIDEO_POST_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    PHOTO_POST_URL = "https://open.tiktokapis.com/v2/post/publish/content/init/"

    def __init__(self, client_key: str, client_secret: str, redirect_uri: str, state = "", scopes: list = None, timeout: int = 500):
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code_verifier = self._generate_code_verifier()
        self.state = state
        self.timeout = timeout
        if scopes:
            self.scopes = self.scopes
        

    def _generate_code_verifier(self) -> str:
        return secrets.token_urlsafe(64)

    def _generate_code_challenge(self, verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip("=")

    def get_authorization_url(self) -> str:
        code_challenge = self._generate_code_challenge(self.code_verifier)
        params = {
            "client_key": self.client_key,
            "response_type": "code",
            "scope": " ".join(self.AUTH_SCOPE),
            "redirect_uri": self.redirect_uri,
            "code_challenge": code_challenge,
            "state": self.state,
            "code_challenge_method": "S256"
        }
        return f"{self.AUTH_URL}?{urllib.parse.urlencode(params)}"

    def exchange_code_for_token(self, code: str, timeout: int = 10) -> dict:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier,
        }

        try:
            response = requests.post(self.TOKEN_URL, headers=headers, data=data, timeout=timeout)
            response.raise_for_status()
            self.token_data = response.json()
            return self.token_data
        except requests.exceptions.Timeout:
            raise TimeoutError("TikTok OAuth request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"OAuth error: {e}")

    def refresh_access_token(self, refresh_token: str = None):
        if not refresh_token and not self.token_data.get("refresh_token"):
            raise Exception("No refresh token available")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token if refresh_token else self.token_data.get("refresh_token"),
        }

        try:
            response = requests.post(self.TOKEN_URL, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            self.token_data = response.json()
            return self.token_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Token refresh failed: {e}")

    def revoke_access_token(self, access_token: str = None):
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No refresh token available")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "token": access_token if access_token else self.token_data.get("access_token")
        }

        try:
            response = requests.post(self.TOKEN_REVOKE_URL, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Token refresh failed: {e}")


    def get_creator_info(self, access_token: str = None):
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No refresh token available")
        url = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
        headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get('access_token')}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        try:
            response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"Request failed: {req_err}")


    def create_video(
            self,
            source: str,
            upload_type: str,
            title: str,
            privacy_level: str,
            disable_duet: bool = False,
            disable_comment: bool = False,
            disable_stitch: bool = False,
            video_cover_timestamp_ms: int = 1000,
            access_token: str = None,
            video_path: str = None,
            video_url: str = None
            ):
        """
        upload_type: str = post_video_file, post_video_url, upload_video_file, upload_video_url
        """
        if not upload_type in ["POST_VIDEO_FILE", "POST_VIDEO_URL", "UPLOAD_VIDEO_FILE", "UPLOAD_VIDEO_URL"]:
            raise ValueError("upload_type must be one of ['POST_VIDEO_FILE', 'POST_VIDEO_URL', 'UPLOAD_VIDEO_FILE', 'UPLOAD_VIDEO_URL']")
        if not source in ["FILE_UPLOAD", "PULL_FROM_URL"]:
            raise ValueError("source must be one of ['FILE_UPLOAD', 'PULL_FROM_URL']")

        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No refresh token available")


        # fetc lates user info
        self.get_creator_info()

        self.headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get('access_token')}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        post_info = {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": disable_duet,
            "disable_comment": disable_comment,
            "disable_stitch": disable_stitch,
            "video_cover_timestamp_ms": video_cover_timestamp_ms
        }

        if source == "FILE_UPLOAD":
            if not video_path:
                raise ValueError("video_path must be provided when source is FILE_UPLOAD")
            elif upload_type not in ["POST_VIDEO_FILE", "UPLOAD_VIDEO_FILE"]:
                raise ValueError("upload_type must be one of ['POST_VIDEO_FILE', 'UPLOAD_VIDEO_FILE']")

            file_info = get_file(video_path)

            source_info = {
                "source": "FILE_UPLOAD",
                "video_size": file_info['file_size'],
                "chunk_size": file_info['chunk_size'],
                "total_chunk_count": file_info['total_chunks']
            }
            payload = {
                "post_info": post_info,
                "source_info": source_info,
                "file_data": file_info['file_data']
            }
            if upload_type == "POST_VIDEO_FILE":
                return self.post_video_file(payload)
            elif upload_type == "UPLOAD_VIDEO_FILE":
                return self.upload_video_file(payload)

        elif source == "PULL_FROM_URL":
            if not video_url:
                raise ValueError("video_url must be provided when source is PULL_FROM_URL")
            elif upload_type not in ["POST_VIDEO_URL", "UPLOAD_VIDEO_URL"]:
                raise ValueError("upload_type must be one of ['POST_VIDEO_URL', 'UPLOAD_VIDEO_URL']")

            source_info = {
                "source": "PULL_FROM_URL",
                "video_url": video_url,
            }

            payload = {
                "source_info": source_info
            }

            if upload_type == "POST_VIDEO_URL":
                payload.update({
                    "post_info": post_info,
                })

            return self.post_video_url(payload)


    def post_video_file(self, payload: dict):
        try:
            # initial posting
            video_data = payload.pop("file_data")
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload, timeout=10))
            initial_data = response

            # proceed to uplaod the video file
            for chunk in video_data:
                response = requests.put(
                    initial_data['data']['upload_url'],
                    headers={
                        "Content-Range": chunk['content_range'],
                        "Content-Type": "video/mp4"
                    },
                    data=chunk['chunk_data'],
                    timeout=self.timeout
                )

            # Handle response
            response.raise_for_status()
            final_data = response.json()
            
            self.post_video_file_response = {
                "initial_response": initial_data,
                "final_response": final_data
            }
            return self.post_video_file_response

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")


    def post_video_url(self, payload: dict):
        try:
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload, timeout=10))
            self.post_video_url_response = response
            return response
        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def upload_video_file(self, payload: dict):

        try:
            # initial posting
            video_data = payload.pop("file_data")
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload['source_info'], timeout=10))
            initial_data = response

            # proceed to uplaod the video file
            for chunk in video_data:
                response = requests.put(
                    initial_data['data']['upload_url'],
                    headers={
                        "Content-Range": chunk['content_range'],
                        "Content-Type": "video/mp4"
                    },
                    data=chunk['chunk_data'],
                    timeout=300
                )
            # Handle response
            response.raise_for_status()
            final_data = response.json()
            self.upload_video_file_response = {
                "initial_response": initial_data,
                "final_response": final_data
            }
            return {
                "initial_data": initial_data,
                "final_data": final_data
            }

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def create_photo(
            self,
            post_mode: str,
            title: str,
            privacy_level: str,
            description: str = "",
            disable_comment: bool = False,
            auto_add_music: bool = False,
            photo_cover_index: int = 1,
            photo_images: list = None,
            access_token: str = None,
            ):

        if not post_mode in ["DIRECT_POST", "MEDIA_UPLOAD"]:
            raise ValueError("post_mode must be one of ['DIRECT_POST', 'MEDIA_UPLOAD']")

        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No refresh token available")

        if not len(photo_images):
            raise ValueError("photo_images must be provided in list [url1, url2, ...]")

        if (photo_cover_index < 1 or photo_cover_index > len(photo_images)):
            raise ValueError("photo_cover_index must be between 1 and the number of images provided")

        # fetch lates user info
        self.get_creator_info()

        self.headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get('access_token')}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        post_info = {
            "title": title,
            "description": description,
        }
        source_info = {
            "source": "PULL_FROM_URL",
            "photo_cover_index": photo_cover_index,
            "photo_images": photo_images
        }

        if post_mode == "DIRECT_POST":
            post_info.update({
                "disable_comment": disable_comment,
                "privacy_level": privacy_level,
                "auto_add_music": auto_add_music
            })

        payload = {
            "post_info": post_info,
            "source_info": source_info,
            "media_type": "PHOTO",
            "post_mode": post_mode
        }

        self.headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get('access_token')}",
            "Content-Type": "application/json"
        }

        try:
            # initial posting
            response = handle_response(requests.post(self.PHOTO_POST_URL, headers=self.headers, json=payload, timeout=10))

            # Handle response
            self.photo_upload_response = response
            return {
                "photo_upload_response": self.photo_upload_response
            }

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")


    def check_upload_status(self, publish_id: str, access_token: str = None):
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No refresh token available")
        if not publish_id:
            raise ValueError("publish_id must be provided to check upload status")

        url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

        headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get('access_token')}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        data = {
            "publish_id": publish_id if publish_id else self.initial_video_upload_data['data'].get("publish_id"),
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check upload status: {e}")