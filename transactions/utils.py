"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

import datetime

from bson import ObjectId
from persiantools.jdatetime import JalaliDate
from common_library.mongo import get_mongo_db


def set_transaction_summary_cache(
    data: list, trans_type: str, trans_mode: str, merchant_id
):
    db = get_mongo_db()
    summary_collection = db["transaction_summary"]
    query = {
        "type": trans_type,
        "mode": trans_mode,
        "merchantId": ObjectId(merchant_id) if merchant_id else None,
    }

    doc = {
        "answer": data,
        "type": trans_type,
        "mode": trans_mode,
        "merchantId": query["merchantId"],
        "createdAt": datetime.utcnow().isoformat(),
    }

    summary_collection.delete_one(query)
    summary_collection.insert_one(doc)


def get_transaction_summary_cache(trans_type: str, trans_mode: str, merchant_id):
    db = get_mongo_db()
    summary_collection = db["transaction_summary"]
    query = {
        "type": trans_type,
        "mode": trans_mode,
        "merchantId": ObjectId(merchant_id) if merchant_id else None,
    }

    doc = summary_collection.find_one(query, {"_id": 0, "answer": 1})
    if doc:
        return doc["answer"]
    return None


def process_transaction(trans_type, trans_mode, trans_merchant_id):
    db = get_mongo_db()
    transaction_collection = db.get_collection("transaction")

    aggregate_pipline = []

    if trans_merchant_id:
        trans_merchant_id = ObjectId(trans_merchant_id)
        aggregate_pipline.append({"$match": {"merchantId": trans_merchant_id}})

    aggregate_pipline.append({"$sort": {"createdAt": 1}})

    group_args = {"$sum": 1} if trans_type == "count" else {"$sum": "$amount"}

    if trans_mode == "daily":
        group_id = {
            "year": {"$year": "$createdAt"},
            "month": {"$month": "$createdAt"},
            "day": {"$dayOfMonth": "$createdAt"},
        }
    elif trans_mode == "weekly":
        group_id = {
            "year": {"$isoWeekYear": "$createdAt"},
            "week": {"$isoWeek": "$createdAt"},
        }
    elif trans_mode == "monthly":
        group_id = {"year": {"$year": "$createdAt"}, "month": {"$month": "$createdAt"}}

    aggregate_pipline.append({"$group": {"_id": group_id, "value": group_args}})

    aggregate_pipline.append({"$sort": {"_id": 1}})

    aggregated_result = transaction_collection.aggregate(aggregate_pipline).to_list()
    data = []

    for document in aggregated_result:

        if trans_mode == "daily":
            key = JalaliDate.to_jalali(**document["_id"]).strftime("%Y/%m/%d")
            data.append({"value": document["value"], "key": key})
        elif trans_mode == "weekly":
            date = datetime.date.fromisocalendar(**document["_id"], day=1)
            key = JalaliDate.to_jalali(date.year, date.month, date.day)
            data.append(
                {
                    "value": document["value"],
                    "key": f"هفته {key.week_of_year()} سال {key.year}",
                }
            )
        else:  # $ monthly
            date = datetime.date(**document["_id"], day=1)
            key = JalaliDate.to_jalali(date.year, date.month, date.day)
            data.append(
                {
                    "value": document["value"],
                    "key": f"{key.strftime('%B', locale='fa')} {key.year}",
                }
            )

    return data
