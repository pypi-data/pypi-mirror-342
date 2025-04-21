import uuid
from typing import cast

from typing_extensions import TypedDict

from smoothintegration import _http


class GetConsentUrlResponseResult(TypedDict):
    consentUrl: str


class GetConsentUrlResponse(TypedDict):
    message: str
    result: GetConsentUrlResponseResult


def get_consent_url(
    company_id: uuid.UUID,
) -> str:
    """
    Get the URL to redirect the user to in order to get consent to connect to a QuickBooks company.

    :param company_id: The ID of the SmoothIntegration company to add this new Connection to.

    :returns: The URL to redirect the user to in order to get consent.
    :raises SIError: if the consent url could not be retrieved for any reason.
    """
    request_params = {"company_id": company_id}

    response = cast(
        GetConsentUrlResponse,
        _http.request("/v1/quickbooks/connect", params=request_params),
    )

    return response["result"]["consentUrl"]
