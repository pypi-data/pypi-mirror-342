# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.api.base.listings.listing import Listing
from multisafepay.api.base.listings.pager import Pager


class ListingPager(Listing):
    """
    A class to represent a listing with pagination.

    Attributes
    ----------
    pager (Pager): The pager object for pagination.

    """

    pager: Pager = None

    def __init__(self, data: list, pager: Pager, class_type: type):
        """
        Initialize the ListingPager with data, pager, and class type.

        Parameters
        ----------
        data (list): A list of data to be converted into items of type T.
        pager (Pager): The pager object for pagination.
        class_type (type): The class type to convert the data into.

        """
        super().__init__(data=data, class_type=class_type)
        self.pager = pager

    def get_pager(self) -> Pager:
        """
        Get the pager object.

        Returns
        -------
        Pager: The pager object for pagination.

        """
        return self.pager
