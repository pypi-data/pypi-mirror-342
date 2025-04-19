import pytest

from wattmaven_solarnetwork_tools.core.solarnetwork_client import (
    HTTPMethod,
    SolarNetworkClient,
    SolarNetworkCredentials,
)


@pytest.mark.integration
class TestSolarNetworkClient:
    def test_get_nodes_with_valid_credentials(self, host, credentials):
        with SolarNetworkClient(
            host=host,
            credentials=credentials,
        ) as client:
            response = client.request("GET", "/solarquery/api/v1/sec/nodes")
            assert response.status_code == 200
            assert response.json()["success"] is True

    def test_get_nodes_with_invalid_credentials(self, host, credentials):
        invalid_credentials = SolarNetworkCredentials(
            token="invalid-token", secret="invalid-secret"
        )

        with SolarNetworkClient(
            host=host,
            credentials=invalid_credentials,
        ) as client:
            response = client.request("GET", "/solarquery/api/v1/sec/nodes")
            assert response.status_code == 403
            assert response.json()["success"] is False

    def test_get_nodes_without_token_and_secret(self, host, credentials):
        # Nodes is a secure endpoint, so it should return 401 if no credentials are provided.

        with SolarNetworkClient(
            host=host,
        ) as client:
            response = client.request("GET", "/solarquery/api/v1/sec/nodes")
            assert response.status_code == 401
            assert response.json()["success"] is False

    def test_lookup_locations_without_credentials(self, host, credentials):
        # Looking up locations is a public endpoint, so it should return 200 even if no credentials are provided.

        with SolarNetworkClient(
            host=host,
        ) as client:
            response = client.request(
                "GET",
                "/solarquery/api/v1/pub/location",
                {
                    "location.timeZoneId": "Pacific/Auckland",
                },
            )
            assert response.status_code == 200
            assert response.json()["success"] is True

    def test_get_nodes_with_valid_credentials_using_method_enum(
        self, host, credentials
    ):
        with SolarNetworkClient(
            host=host,
            credentials=credentials,
        ) as client:
            response = client.request(HTTPMethod.GET, "/solarquery/api/v1/sec/nodes")
            assert response.status_code == 200
            assert response.json()["success"] is True

    def test_get_datum_list_with_random_order_of_parameters(
        self, host, credentials, test_node_id
    ):
        with SolarNetworkClient(
            host=host,
            credentials=credentials,
        ) as client:
            response = client.request(
                "GET",
                "/solarquery/api/v1/sec/datum/list",
                # Should be able to handle parameters that _aren't_ in alphabetical order.
                params={
                    "nodeId": test_node_id,
                    "startDate": "2025-01-07",
                    "endDate": "2025-01-01",
                    "aggregation": "Day",
                },
            )
            assert response.status_code == 200
            assert response.json()["success"] is True

    def test_get_datum_list_with_source_id(self, host, credentials, test_node_id):
        with SolarNetworkClient(
            host=host,
            credentials=credentials,
        ) as client:
            response = client.request(
                "GET",
                "/solarquery/api/v1/sec/datum/list",
                params={
                    "nodeId": test_node_id,
                    # Source IDs are good to test because they must be correctly encoded.
                    "sourceId": "*/**",
                    "startDate": "2025-01-07",
                    "endDate": "2025-01-01",
                    "aggregation": "Day",
                },
            )
            assert response.status_code == 200
            assert response.json()["success"] is True

    def test_get_datum_list_with_accept_header(self, host, credentials, test_node_id):
        with SolarNetworkClient(
            host=host,
            credentials=credentials,
        ) as client:
            response = client.request(
                "GET",
                "/solarquery/api/v1/sec/datum/list",
                params={
                    "nodeId": test_node_id,
                    "startDate": "2025-01-07",
                    "endDate": "2025-01-01",
                    "aggregation": "Day",
                },
                accept="text/csv",
            )
            assert response.status_code == 200
            assert response.headers["Content-Type"].startswith("text/csv")
