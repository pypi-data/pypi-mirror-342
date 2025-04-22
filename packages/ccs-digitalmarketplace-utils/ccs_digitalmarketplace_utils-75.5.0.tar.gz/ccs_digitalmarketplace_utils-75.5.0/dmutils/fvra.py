from dmapiclient.errors import APIError

from dmapiclient import SpotlightFvraAPIClient
from logging import Logger
from typing import List
from dmutils.timing import logged_duration_for_external_request as log_external_request


def _get_financials_from_duns_number(spotlight_fvra_api_client: SpotlightFvraAPIClient, duns_number: str):
    with log_external_request(service="Spotlight FVRA"):
        return spotlight_fvra_api_client.get_financials_from_duns_number(duns_number)["organisationMetrics"]


def supplier_financial_viablitity_risk_assessments(
    spotlight_fvra_api_client: SpotlightFvraAPIClient,
    duns_numbers: List[str],
    logger: Logger
):
    """
    Function to collect the metrics results for a list of suppliers.
    If an exception is raised then the error is logged and an empty array is returned
    """
    try:
        return [
            _get_financials_from_duns_number(spotlight_fvra_api_client, duns_number)
            for duns_number in duns_numbers
        ]
    except APIError as e:
        logger.error(
            "Failed to get metrics for all suppliers",
            extra={
                "error": str(e),
            },
        )
        return []
