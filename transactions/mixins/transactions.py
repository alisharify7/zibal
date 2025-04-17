from transactions.serializers import TransactionQueryParamsSerializer


class TransactionQueryMixin:
    """Mixin for handling common transaction query parameters"""

    def get_transaction_params(self, request):
        """Extracts and validates transaction query parameters"""
        query_params = TransactionQueryParamsSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        return (
            query_params.data.get("type"),
            query_params.data.get("mode"),
            query_params.data.get("merchantId", None),
        )
