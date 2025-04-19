# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["CreateTokenResponse"]


class CreateTokenResponse(BaseModel):
    token: str
    """The authentication token to use for API requests"""
