from datetime import datetime
from typing import Dict, List, Optional, Any

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    PositiveInt,
    HttpUrl,
)

__all__ = [
    "UserModel",
    "LoginResponseModel",
    "AppConfigUserModel",
    "WaitingListModel",
    "ChatConfigModel",
    "ChatModel",
    "ChatUploadImageConfigModel",
    "ChatMessagesModel",
]


class UserModel(BaseModel):
    id: int
    uid: str
    created_at: datetime
    first_name: str
    last_name: str
    email: str
    user_type: str
    timezone: str
    primary_language: str
    secondary_languages: List
    country: str
    auth_type: str
    has_usable_password: StrictBool
    has_accepted_latest_terms: StrictBool
    has_accepted_marketing: Optional[StrictBool]
    is_pending_deletion: StrictBool
    has_hidden_email: StrictBool
    extra: Dict[str, Any]


class LoginResponseModel(BaseModel):
    user: UserModel
    token: str
    email_verification_required: StrictBool
    password_change_required: StrictBool


class ChatUploadImageConfigModelFields(BaseModel):
    Content_Type: str = Field(alias="Content-Type")
    key: str
    x_amz_algorithm: str = Field(alias="x-amz-algorithm")
    x_amz_credential: str = Field(alias="x-amz-credential")
    x_amz_date: str = Field(alias="x-amz-date")
    policy: str
    x_amz_signature: str = Field(alias="x-amz-signature")


class ChatUploadImageConfigModel(BaseModel):
    url: HttpUrl
    fields: ChatUploadImageConfigModelFields
    chat_image_id: int


class ChatModel(BaseModel):
    id: int
    created_at: datetime
    context: str
    organization: Optional[str]
    user: int
    language: str
    rating: Optional[int]
    call_button_title: str


class ChatConfigModel(BaseModel):
    sid: str
    upgrades: List[str]
    pingInterval: PositiveInt
    pingTimeout: PositiveInt
    maxPayload: PositiveInt


class AppConfigUserModel(BaseModel):
    # groups_enabled: StrictBool
    photos_enabled: StrictBool
    # ios_use_community_portal: StrictBool
    # organization_calls_enabled: StrictBool
    # ios_learning_center_enabled: StrictBool
    # android_use_community_portal: StrictBool
    # volunteer_label_call_enabled: StrictBool
    chat_enabled: StrictBool
    # sh_scan_qr_code_enabled: StrictBool
    chat_image_jpeg_compression: int
    chat_image_max_dimension: int
    chat_image_type: str
    # bmai_speech_output_available: StrictBool
    # ios_shortcuts_settings_enabled: StrictBool
    # wearable_rbm_blocked: StrictBool
    # wearable_rbm_enabled: StrictBool
    # wearable_rbm_debug_actions_enabled: StrictBool
    # wearable_rbm_promo_enabled: StrictBool


class WaitingListModel(BaseModel):
    id: int
    created_at: datetime
    modified_at: datetime
    device_type: str


class Image(BaseModel):
    id: int
    created_at: datetime
    upload_finished: StrictBool
    url: HttpUrl


class ChatMessagesModel(BaseModel):
    id: int
    version: PositiveInt
    created_at: datetime
    role: str
    user: Optional[int]
    session: int
    type: str
    error_code: Optional[int]
    data: Optional[str]
    images: List[Image]


"""example
m = ChatMessagesModel.model_validate_json(message)
"""
