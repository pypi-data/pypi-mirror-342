# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.client.client import Client


class AbstractManager:
    """
    A class to represent an abstract manager.

    Attributes
    ----------
    client (Client): An instance of the Client class to be used by the manager.

    """

    def __init__(self, client: Client):
        """
        Initialize the AbstractManager with a Client instance.

        Parameters
        ----------
        client (Client): An instance of the Client class to be used by the manager.

        """
        self.client = client
