"""
unofficial API BeMyAI from Android app
"""
from .langs import LANGS, LOCALES
from .schema import (
    LoginResponseModel,
    AppConfigUserModel,
    ChatModel,
    ChatConfigModel,
    ChatUploadImageConfigModel,
    ChatMessagesModel,
)
import os
import asyncio
import tempfile
from functools import partial
import json
import shutil
from uuid import uuid4
from datetime import datetime, timezone, timedelta
import os.path
from math import floor
from typing import AsyncIterator, Optional
import aiohttp
import aiofiles  # type: ignore
import aiofiles.os  # type: ignore
from loguru import logger  # type: ignore
from PIL import Image

my_debug = os.environ.get("my_debug", None) is not None
if my_debug:
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:8888"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8888"


def get_image_info(filename: str) -> tuple[Optional[str], tuple[int, int], str]:
    with Image.open(filename) as im:
        return (im.format, im.size, im.mode)


def compute_image_size(width: int, height: int, max_dimension=2000) -> tuple[int, int]:
    width_changed, height_changed = (0, 0)
    if (width <= max_dimension and height <= max_dimension) or (width == height):
        return (width, height)
    max_number: int = max(width, height)
    divided_number: int = max_number / max_dimension
    min_number: int = min(width, height)
    min_side: int = floor(min_number / divided_number)
    if width > height:
        width_changed = max_dimension
        height_changed = min_side
    else:
        width_changed = min_side
        height_changed = max_dimension
    return (width_changed, height_changed)


def process_image(
    path_to_image: str,
    path_to_processed_image: str,
    max_dimension: int = 2000,
    format: str = "JPEG",
    optimize: bool = True,
    jpeg_compress: int = 80,
) -> tuple[int, int]:
    """
    Process the image for API requirements.
    processed image will be saved in `path_to_processed_image`
    as new file in the specified format (default JPEG) with compression 80% by default.
    Returns the resolution of the image.
    """
    logger.debug("start image process")
    with open(path_to_image, "rb") as fp:
        im = Image.open(fp)
        width, height = im.size
        if im.mode != "RGB":
            logger.info(f"converting from {im.mode} to  RGB mode")
            im = im.convert("RGB")
        if width > max_dimension or height > max_dimension:
            logger.info("resizing image")
            im.thumbnail(
                compute_image_size(
                    width=width, height=height, max_dimension=max_dimension
                )
            )
        im.save(
            path_to_processed_image,
            format.upper(),
            optimize=optimize,
            quality=jpeg_compress,
        )
        width, height = im.size
        logger.info("image processed: %s, %dx%d" % (format, width, height))
        im.close()
    assert os.path.isfile(path_to_processed_image), "The processed file not found"
    return (width, height)


dl_folder = os.path.join(tempfile.gettempdir(), "downloads")


class BeMyAIError(Exception):
    msg = None
    response = None

    def __init__(self, msg, response=None):
        self.response = response
        super().__init__(msg)


class EmailVerificationRequired(BeMyAIError):
    msg = None
    response = None

    def __init__(self, msg="email verification required", response=None):
        self.response = response
        super().__init__(msg, response)


class PasswordChangeRequired(BeMyAIError):
    msg = None
    response = None

    def __init__(self, msg="password change required", response=None):
        self.response = response
        super().__init__(msg, response)


class BeMyAI:
    def __init__(
        self, token: str = "", response_language="en-US", trust_env: bool = True
    ):
        if not os.path.isdir(dl_folder):
            os.mkdir(dl_folder)
            logger.info("created dl folder")
        else:
            logger.info("dl folder already exists")
        self.token = token
        if response_language in LANGS or response_language in LOCALES:
            self.response_language = response_language
        else:
            raise ValueError(
                "the language must be a two-letter code or  a country separated by a hyphen"
            )
        self.trust_env: bool = trust_env
        self.bemyeyes_app_secret = (
            "55519e815ff7b09ab971de5564baa282eca53af1eb528385fb98a34f2010e8c7"
        )
        self.User_Agent = "okhttp/3.14.9"
        self.gateway_url = "https://gateway.bemyeyes.com/api/v2/"
        self.lp_delimeter = chr(30)
        self.api_url = "https://api.bemyeyes.com/api/v2/"
        self.sid = ""
        self.extra = {
            "device_type": "android",
            "screen_reader_enabled": True,
            "content_size": "1.15",
            "accesibility_content_size_enabled": False,
        }
        self.app_config_user_cache: Optional[AppConfigUserModel] = None

    @staticmethod
    def get_error_messages(r):
        error_messages = []
        for m in r.items():
            k, v = m
            if isinstance(v, list):
                v = ", ".join(v)
            elif not isinstance(v, str):
                v = str(v)
            error_messages.append(": ".join([k, v]))
        if len(error_messages) == 0:
            return r
        return "\n".join(error_messages)

    @property
    def headers(self):
        h = {
            "User-Agent": self.User_Agent,
            "bemyeyes-app-secret": self.bemyeyes_app_secret,
            "Accept-Language": self.response_language,
        }
        if self.token and len(self.token) > 3:
            h.update(Authorization="Token " + self.token)
        return h

    @property
    def terms_accepted_at(self) -> str:
        "For signup"
        shanghai_offset = timedelta(hours=8)
        utc_now = datetime.now(timezone.utc)
        shanghai_now = utc_now.astimezone(timezone(shanghai_offset))
        logger.debug("date for signup: " + str(shanghai_now))
        return shanghai_now.isoformat()

    async def request(
        self, method, url, params=None, data=None, json=None, headers=None
    ):
        """
        Make a request to the API.
        In the response from the gateway server you Get the text,
        since the server returns data in different formats and with different headers,
        and from the api server get a dictionary,
        since all interaction is strictly in JSON format with the correct headers
        Thanks to Django REST framework on their side.
        """
        j = None
        if headers is None:
            headers = self.headers
        logger.debug(f"making {method} request to {url}...")
        async with aiohttp.ClientSession(
            trust_env=self.trust_env, raise_for_status=False, headers=headers
        ) as session:
            async with session.request(
                method=method, url=url, params=params, data=data, json=json
            ) as resp:
                if "json" not in resp.headers.get("Content-Type").lower():
                    if resp.ok:
                        return await resp.text()
                    else:
                        raise BeMyAIError(message=resp.text, response=resp)
                else:
                    if resp.ok:
                        return await resp.json()
                    else:
                        j = await resp.json()
                        if j.get("code", 0) != 1:
                            raise BeMyAIError(
                                msg=self.get_error_messages(j), response=resp
                            )
                        else:
                            logger.debug("There will be a new session next time")
                            await self.get_chat_config()
                            await self.authinticate(self.sid)
                            await self.enable_chat(self.sid)
                            return await self.request(
                                method=method,
                                url=url,
                                params=params,
                                data=data,
                                json=json,
                                headers=headers,
                            )

    async def refresh_token(self) -> LoginResponseModel:
        "Check the user (for example, to find out if the email address is verified)"
        resp = await self.request(
            "POST",
            self.api_url + "auth/refresh-token",
            json={"timezone": "Asia/Shanghai", "extra": self.extra},
        )
        result = LoginResponseModel.model_validate(resp)
        self.token = result.token
        return result

    async def resend_verify_email(self) -> None:
        "Send a confirmation email again (only after signup)"
        result = await self.refresh_token()
        if not result.email_verification_required:
            raise BeMyAIError("The email has already been verified")
        await self.request("POST", self.api_url + "auth/resend-verify-email")

    async def send_reset_password(self, email: str) -> None:
        "Recover a forgotten password. A link to the password change form will be sent to your email"
        self.token = ""
        await self.request(
            "POST", self.api_url + "auth/send-reset-password", json={"email": email}
        )

    async def signup(
        self, first_name: str, last_name: str, email: str, password: str
    ) -> LoginResponseModel:
        "Signup by mail and password (auth/signup-email) and get user object"
        self.token = ""
        resp = await self.request(
            "POST",
            self.api_url + "auth/signup-email",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "user_type": "bvi",
                "timezone": "Asia/Shanghai",
                "terms_accepted_at": self.terms_accepted_at,
                "extra": self.extra,
            },
        )
        result = LoginResponseModel.model_validate(resp)
        self.token = result.token
        return result

    async def login(self, email, password):
        "Login by mail and password (auth/login-email) and get token"
        self.token = ""
        resp = await self.request(
            "POST",
            self.api_url + "auth/login-email",
            json={"email": email, "password": password, "extra": self.extra},
        )
        result = LoginResponseModel.model_validate(resp)
        self.token = result.token
        if result.email_verification_required:
            raise EmailVerificationRequired(response=result)
        if result.password_change_required:
            raise PasswordChangeRequired(response=result)
        return result

    async def app_config_user(self) -> AppConfigUserModel:
        """
        Get the application configuration for the user.
        The results will be cached in the class instance.
        """
        if self.app_config_user_cache:
            logger.info("get app user config from cache")
            return self.app_config_user_cache
        resp = await self.request("GET", self.api_url + "app-config/user")
        self.app_config_user_cache = AppConfigUserModel.model_validate(resp)  # type: ignore
        logger.info("get app user config from internet")
        return self.app_config_user_cache  # type: ignore

    async def send_text_message(
        self, chat_id: int, text: str
    ) -> tuple[str, int, ChatMessagesModel]:
        "Send a text message to the chat"
        if not isinstance(chat_id, int):
            raise TabError("chat_id must be int")
        if not isinstance(text, str):
            raise TabError("text must be str")
        await self.get_chat_config()
        await self.authinticate(self.sid)
        await self.enable_chat(self.sid)
        resp = await self.request(
            "POST",
            f"{self.api_url}chats/{chat_id}/messages",
            json={"role": "user", "type": "text", "data": text},
        )
        result = ChatMessagesModel.model_validate(resp)
        return (self.sid, result.session, result)

    async def chats(self, context="chat") -> ChatModel:
        """
        Create new chat
        """
        logger.info("create new chat")
        resp = await self.request(
            "POST", self.api_url + "chats", json={"context": context}
        )
        return ChatModel.model_validate(resp)

    async def chat_messages(self, chat_id: int, image_id: int) -> ChatMessagesModel:
        resp = await self.request(
            "POST",
            f"{self.api_url}chats/{chat_id}/messages",
            json={"role": "user", "type": "text", "chat_image_id": image_id},
        )
        return ChatMessagesModel.model_validate(resp)

    async def chat_request_image_upload(
        self, chat_id: int, width: int, height: int, format: str = "jpeg"
    ) -> ChatUploadImageConfigModel:
        """
        Request parameters for upload image to the chat
        """
        logger.info("requested upload image config")
        cnf = await self.app_config_user()
        if width < 16 or height < 16:
            raise ValueError("The image is too small")
        if (
            width > cnf.chat_image_max_dimension
            or height > cnf.chat_image_max_dimension
        ):
            raise ValueError(
                f"width or height must be less than or equal to {cnf.chat_image_max_dimension}"
            )
        resp = await self.request(
            "POST",
            f"{self.api_url}chats/{chat_id}/request-image-upload",
            json={"format": format, "width": width, "height": height},
        )
        return ChatUploadImageConfigModel.model_validate(resp)

    async def take_photo(self, filename: str) -> tuple[str, int]:
        path_to_image = None
        if not isinstance(filename, str):
            path_to_image = os.path.join(dl_folder, f"image_{str(uuid4())}.tmp")
            with open(path_to_image, "wb") as newfp:
                shutil.copyfileobj(filename, newfp)
            filename = path_to_image  # type: ignore
        loop = asyncio.get_running_loop()
        cnf = await self.app_config_user()
        format, size, mode = await loop.run_in_executor(
            None, partial(get_image_info, filename=filename)
        )
        logger.info(
            "recognizing new photo: %s, %s, %s"
            % (format, str(size[0]) + "x" + str(size[1]), mode)
        )
        chat_config = await self.get_chat_config()
        await self.authinticate(chat_config.sid)
        await self.enable_chat(chat_config.sid)
        chat = await self.chats()
        path_to_processed_image = os.path.join(
            dl_folder, f"processed_image_{str(uuid4())}.{cnf.chat_image_type}"
        )
        width, height = await loop.run_in_executor(
            None,
            partial(
                process_image,
                path_to_image=filename,
                path_to_processed_image=path_to_processed_image,
                max_dimension=cnf.chat_image_max_dimension,
                format=cnf.chat_image_type,
                optimize=(cnf.chat_image_type.upper() == "JPEG"),
                jpeg_compress=cnf.chat_image_jpeg_compression,
            ),
        )
        upload_config = await self.chat_request_image_upload(
            chat_id=chat.id,
            width=width,
            height=height,
            format=cnf.chat_image_type,
        )
        logger.info("Starting upload image to Amazon")
        fd = aiohttp.FormData(quote_fields=False)
        fields = dict(
            {
                "Content-Type": upload_config.fields.Content_Type,
                "key": upload_config.fields.key,
                "x-amz-algorithm": upload_config.fields.x_amz_algorithm,
                "x-amz-credential": upload_config.fields.x_amz_credential,
                "x-amz-date": upload_config.fields.x_amz_date,
                "policy": upload_config.fields.policy,
                "x-amz-signature": upload_config.fields.x_amz_signature,
            }
        )
        for field in fields.items():
            fd.add_field(*field, content_type=None, content_transfer_encoding=None)
        with open(path_to_processed_image, "rb") as fp:
            fd.add_field(
                "file",
                fp,
                content_type=upload_config.fields.Content_Type,
                filename="file",
            )
            async with aiohttp.ClientSession(
                trust_env=self.trust_env,
                raise_for_status=True,
                headers={"User-Agent": self.User_Agent},
            ) as session:
                async with session.post(str(upload_config.url), data=fd) as resp:
                    if resp.status >= 100 <= 206:
                        logger.info("Uploaded successfully")
                    else:
                        logger.error("Upload faild")
                    _ = await resp.read()
        logger.info("removeing processed image")
        await aiofiles.os.remove(path_to_processed_image)
        if path_to_image:
            logger.info("removeing tmp image")
            await aiofiles.os.remove(path_to_image)
        upload_result = await self.chat_messages(
            chat_id=chat.id, image_id=upload_config.chat_image_id
        )
        if not upload_result.images[0].upload_finished:
            logger.error("The image has not been uploaded")
            raise BeMyAIError("The image could not be uploaded to Amazon")
        else:
            logger.info("upload image finished")
        return (chat_config.sid, chat.id)

    async def send_raw_events(self, sid: str, data: str) -> str:
        params = {"EIO": "4", "transport": "polling", "sid": sid}
        text = await self.request(
            "POST", self.gateway_url + "socket/", params=params, data=data
        )
        return text

    async def authinticate(self, sid: str = "") -> bool:
        if not sid:
            sid = self.sid
        text = await self.send_raw_events(sid, "40")
        if text != "ok":
            raise BeMyAIError(f"An unexpected response was received. {text}")
        text = await self.receive_raw_events(sid)
        if "AUTHENTICATED" not in text:
            raise BeMyAIError(f"An unexpected response was received. {text}")
        return True

    async def get_chat_config(self) -> ChatConfigModel:
        "Get sid and other settings"
        logger.debug("Getting chat config...")
        text = await self.receive_raw_events(get_new_sid=True)
        result = ChatConfigModel.model_validate_json(text[1::])
        if self.sid != result.sid:
            logger.debug("received new session id")
        self.sid = result.sid
        return result

    async def enable_chat(self, sid: str = "") -> str:
        logger.debug("enabling the chat")
        if not sid:
            sid = self.sid
        return await self.send_raw_events(sid, '42["ENABLE_CHAT","{}"]')

    async def receive_raw_events(self, sid: str = "", get_new_sid=False) -> str:
        params = {"EIO": "4", "transport": "polling"}
        if not sid:
            sid = self.sid
        if sid and not get_new_sid:
            params["sid"] = sid
        text = await self.request("GET", self.gateway_url + "socket/", params=params)
        return text

    async def receive_messages(self, sid: str = "") -> AsyncIterator[ChatMessagesModel]:
        logger.debug("Starting receive GPT messages")
        if not sid:
            sid = self.sid
        for i in range(3):
            text = await self.receive_raw_events(sid)
            if "42" not in text:
                logger.debug("unexpected response from polling: " + str(text))
                continue
            for response_part in text.split(self.lp_delimeter):
                if '"NEW_CHAT_MESSAGE"' in response_part:
                    message = ChatMessagesModel.model_validate(
                        json.loads(response_part[2:])[1]
                    )
                    logger.info("Got new message")
                    yield message
                    if not message.user:
                        break
                else:
                    logger.debug(response_part[2:-1])
        logger.debug("messages receiveing completed")
