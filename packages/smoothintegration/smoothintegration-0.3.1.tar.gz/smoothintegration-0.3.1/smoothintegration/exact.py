import uuid
from typing import Literal, TypedDict, cast

from smoothintegration import _http

ExactVersion = Literal["nl", "be", "de", "uk", "us", "es", "fr"]


class GetConsentUrlResponseResult(TypedDict):
    consentUrl: str


class GetConsentUrlResponse(TypedDict):
    message: str
    result: GetConsentUrlResponseResult


def get_consent_url(
    company_id: uuid.UUID,
    version: str,
) -> str:
    """
    Get the URL to redirect the user to in order to get consent to connect to an Exact company.

    :param company_id: The ID of the SmoothIntegration company to add this new Connection to.
    :param version: Version of Exact to connect to. One of "nl", "be", "de", "uk", "us", "es", "fr".

    :returns: The URL to redirect the user to in order to get consent.
    :raises SIError: if the consent url could not be retrieved for any reason.
    """
    request_params = {
        "company_id": company_id,
        "version": version,
    }

    response = cast(
        GetConsentUrlResponse,
        _http.request("/v1/exact/connect", params=request_params),
    )

    return response["result"]["consentUrl"]
