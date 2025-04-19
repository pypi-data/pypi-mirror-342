# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["CreateMagicLinkResponse"]


class CreateMagicLinkResponse(BaseModel):
    magic_link_url: str
    """The Connect magic link url to share with the user."""
