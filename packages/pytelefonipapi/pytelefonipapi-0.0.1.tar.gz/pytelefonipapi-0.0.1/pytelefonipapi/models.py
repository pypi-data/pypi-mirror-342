from typing import Optional, Union
from pydantic import BaseModel


class GetCodeDataModel(BaseModel):
    phone: str
    code: str
    id: int

    def __str__(self):
        return f"{self.phone} - {self.code}"


class GetTGCodeDataModel(BaseModel):
    phone: str
    code: str
    id: int
    operator_name: str
    channel: str
    status: bool
    status_info: str

    def __str__(self):
        return f"{self.phone} - {self.code}"


class BackCallsDataModel(BaseModel):
    auth_phone: str
    id: int
    url_image: str | None = None
    url_link: str | None = None

    def __str__(self):
        return f"{self.auth_phone} - {self.id}"


class ReverseAuthPhoneCheckDataModel(BaseModel):
    phone: str
    id: int

    def __str__(self):
        return f"{self.phone} - {self.id}"


class GetStatusDataModel(BaseModel):
    id: int
    created_at: str
    phone: str
    status: bool
    status_info: str
    price: float

    def __str__(self):
        return f"{self.id}"


class GetBalanceDataModel(BaseModel):
    balance: float
    price: float | None = None
    balance_limit: float | None = None

    def __str__(self):
        return f"{self.balance}"


class BillingDataModel(BaseModel):
    created_at: str
    code_auth: str
    status: bool
    status_info: str
    phone: str
    price: float

    def __str__(self):
        return f"{self.status_info}"


class BaseResponseModel(BaseModel):
    success: Optional[bool] = None
    error: Optional[str] = None
    data: Union[
        GetCodeDataModel, str,
        BackCallsDataModel,
        ReverseAuthPhoneCheckDataModel,
        GetTGCodeDataModel,
        GetStatusDataModel,
        GetBalanceDataModel,
        BillingDataModel,
    ] = None


class GetCodeModel(BaseResponseModel):
    data: GetCodeDataModel | None = None


class GetSMSCodeModel(BaseResponseModel):
    data: GetCodeDataModel | None = None


class ReverseAuthPhoneGetModel(BaseResponseModel):
    data: BackCallsDataModel | None = None


class ReverseAuthPhonePostModel(BaseResponseModel):
    data: BackCallsDataModel | None = None


class ReverseAuthPhoneCheckModel(BaseResponseModel):
    data: ReverseAuthPhoneCheckDataModel | None = None


class GetTGCodeModel(BaseResponseModel):
    data: GetTGCodeDataModel | None = None


class GetBillingModel(BaseResponseModel):
    data: list[BillingDataModel] | None = None


class PostBillingModel(BaseResponseModel):
    data: list[BillingDataModel] | None = None


class GetStatusModel(BaseResponseModel):
    data: GetStatusDataModel | None = None


class GetBalanceModel(BaseResponseModel):
    data: GetBalanceDataModel | None = None
