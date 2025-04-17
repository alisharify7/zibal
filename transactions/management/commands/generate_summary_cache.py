from django.core.management.base import BaseCommand
from common_library.mongo import get_mongo_db, get_mongo_client
from pymongo.collation import Collation
from transactions.utils import set_transaction_summary_cache, process_transaction


class Command(BaseCommand):
    help = "Generate and cache all transaction summaries for all merchants and modes"

    def handle(self, *args, **options):
        db = get_mongo_db()
        transactions_collection = db.get_collection("transaction")

        modes = ["daily", "weekly", "monthly"]
        types = ["count", "amount"]
        merchant_ids = transactions_collection.distinct("merchantId")

        for merchant_id in merchant_ids:
            for mode in modes:
                for ttype in types:
                    data = process_transaction(
                        trans_type=ttype, trans_mode=mode, trans_merchant_id=merchant_id
                    )
                    set_transaction_summary_cache(
                        data=data,
                        trans_type=ttype,
                        trans_mode=mode,
                        merchant_id=merchant_id,
                    )

        for mode in modes:
            for ttype in types:
                data = process_transaction(
                    trans_type=ttype, trans_mode=mode, trans_merchant_id=None
                )
                set_transaction_summary_cache(
                    data=data, trans_type=ttype, trans_mode=mode, merchant_id=None
                )

        self.stdout.write(self.style.SUCCESS("✅ All caches generated successfully!"))
