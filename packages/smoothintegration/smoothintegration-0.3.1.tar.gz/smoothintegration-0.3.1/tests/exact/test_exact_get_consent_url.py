import uuid

import pytest
import responses

from smoothintegration.exceptions import SIError


class TestExactGetConsentUrl:

    def test_can_get_consent_url_for_uk(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/exact/connect?company_id=d56b018d-42a3-4f47-b141-44d9d4d81878&version=uk",
            json={
                "message": "Created Consent Url",
                "result": {
                    "consentUrl": "the-consent-url",
                },
            },
            status=200,
        )

        assert (
            test_client.exact.get_consent_url(
                uuid.UUID("d56b018d-42a3-4f47-b141-44d9d4d81878"), "uk"
            )
            == "the-consent-url"
        )

    def test_can_get_consent_url_for_nl(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/exact/connect?company_id=d56b018d-42a3-4f47-b141-44d9d4d81878&version=nl",
            json={
                "message": "Created Consent Url",
                "result": {
                    "consentUrl": "the-consent-url",
                },
            },
            status=200,
        )

        assert (
            test_client.exact.get_consent_url(
                uuid.UUID("d56b018d-42a3-4f47-b141-44d9d4d81878"), "nl"
            )
            == "the-consent-url"
        )

    def test_raises_error_on_bad_request(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/exact/connect?company_id=d56b018d-42a3-4f47-b141-44d9d4d81878&version=uk",
            json={"message": "Exact is not configured for this organisation"},
            status=400,
        )

        with pytest.raises(SIError) as excinfo:
            test_client.exact.get_consent_url(
                uuid.UUID("d56b018d-42a3-4f47-b141-44d9d4d81878"), "uk"
            )
        assert (
            str(excinfo.value)
            == "Bad Request: Exact is not configured for this organisation"
        )

    def test_raises_error_on_unauthorized(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/exact/connect?company_id=invalid-company-id&version=uk",
            json={"message": "Invalid 'X-Organisation' header"},
            status=401,
        )

        with pytest.raises(SIError) as excinfo:
            test_client.exact.get_consent_url("invalid-company-id", "uk")
        assert str(excinfo.value) == "Unauthorized: Invalid 'X-Organisation' header"

    def test_raises_error_on_internal_server_error(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/exact/connect?company_id=d56b018d-42a3-4f47-b141-44d9d4d81878&version=uk",
            json={"message": "Internal Server Error"},
            status=500,
        )

        with pytest.raises(SIError) as excinfo:
            test_client.exact.get_consent_url(
                uuid.UUID("d56b018d-42a3-4f47-b141-44d9d4d81878"), "uk"
            )
        assert str(excinfo.value) == "Internal Server Error"
