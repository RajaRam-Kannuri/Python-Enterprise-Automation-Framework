from pydantic import Field

from core.models.lms.lms_base import LMSModelBase


class LoginForm(LMSModelBase):
    return_url: str = Field(alias="Input.ReturnUrl")
    email: str = Field(alias="Input.Email")
    password: str = Field(alias="Input.Password")
    remember_login: str = Field(alias="Input.RememberLogin")
    button: str
    request_verification_token: str = Field(alias="__RequestVerificationToken")
