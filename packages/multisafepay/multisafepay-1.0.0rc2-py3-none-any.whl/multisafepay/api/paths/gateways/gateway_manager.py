# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.gateways.response.gateway import Gateway
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg

ALLOWED_OPTIONS = {
    "country": "",
    "currency": "",
    "amount": "",
    "include": "",
}


class GatewayManager(AbstractManager):
    """
    Manages gateway-related operations.
    """

    def get_gateways(self, include_coupons: bool = True) -> CustomApiResponse:
        """
        Retrieve a list of gateways.

        Parameters
        ----------
        include_coupons (bool): Whether to include coupons in the response (default is True).

        Returns
        -------
        CustomApiResponse: The response containing the list of gateways.

        """
        options = {}
        if include_coupons:
            options["include"] = "coupons"

        response = self.client.create_get_request("json/gateways", options)
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if isinstance(response.get_body_data(), list):
            try:
                args["data"] = [
                    Gateway.from_dict(gateway)
                    for gateway in response.get_body_data().copy()
                ]
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Listing gateway"))
                    .get_messages()
                )

        return CustomApiResponse(**args)

    def get_by_code(
        self,
        gateway_code: str,
        options: dict = None,
    ) -> CustomApiResponse:
        """
        Retrieve a gateway by its code.

        Parameters
        ----------
        gateway_code (str): The code of the gateway to retrieve.
        options (dict): Additional options for the request (default is None).

        Returns
        -------
        CustomApiResponse: The response containing the gateway data.

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}

        response = self.client.create_get_request(
            f"json/gateways/{gateway_code}",
            options,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }

        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Gateway(**response.get_body_data().copy())
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Gateway"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
