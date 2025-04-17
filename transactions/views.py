"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins.transactions import TransactionQueryMixin
from .serializers import TransactionResponseSerializer
from .utils import (
    process_transaction,
    get_transaction_summary_cache,
    set_transaction_summary_cache,
)


class TransactionView(TransactionQueryMixin, APIView):
    """
    API endpoint for retrieving transaction reports from either the main database or cache.

    This view handles:
    1. Fetching transaction data from the primary database if not available in cache
    2. Storing results in cache for future requests

    Query Parameters:
    - type: Report type ('count' for transaction count or 'amount' for transaction amounts)
    - mode: Time period ('daily', 'weekly', or 'monthly')
    - merchantId: Optional merchant ID to filter transactions

    Response:
    - Returns serialized transaction data grouped by the specified time period
    - Automatically caches results for subsequent requests
    - Returns 200 OK with cached data if available
    - Returns 200 OK with fresh data if not in cache
    """

    def get(self, request, *args, **kwargs):
        trans_type, trans_mode, trans_merchant_id = self.get_transaction_params(request)

        cache_result = get_transaction_summary_cache(
            trans_type=trans_type, trans_mode=trans_mode, merchant_id=trans_merchant_id
        )
        if cache_result:
            return Response(cache_result)

        data = process_transaction(
            trans_type=trans_type,
            trans_mode=trans_mode,
            trans_merchant_id=trans_merchant_id,
        )

        set_transaction_summary_cache(
            data=data,
            trans_mode=trans_mode,
            trans_type=trans_type,
            merchant_id=trans_merchant_id,
        )

        serialized_data = TransactionResponseSerializer(data=data, many=True)
        serialized_data.is_valid(raise_exception=True)
        return Response(serialized_data.data)


class TransactionCachedView(TransactionQueryMixin, APIView):
    """
    API endpoint exclusively for retrieving cached transaction reports.

    This view:
    - Only returns data if it exists in cache
    - Does not query the primary database
    - Useful for optimized performance when fresh data isn't required

    Query Parameters:
    - type: Report type ('count' or 'amount')
    - mode: Time period ('daily', 'weekly', or 'monthly')
    - merchantId: Optional merchant ID filter

    Response:
    - Returns 200 OK with cached data if available
    - Returns 404 Not Found if data isn't in cache
    """

    def get(self, request, *args, **kwargs):
        trans_type, trans_mode, trans_merchant_id = self.get_transaction_params(request)

        cache_result = get_transaction_summary_cache(
            trans_type=trans_type, trans_mode=trans_mode, merchant_id=trans_merchant_id
        )
        if cache_result:
            return Response(cache_result)
        else:
            return Response(
                {
                    "message": "query was not found in cache db. for retrieving data use main api endpoint."
                },
                status=status.HTTP_204_NO_CONTENT,
            )
