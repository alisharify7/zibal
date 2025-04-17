"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

from pymongo import MongoClient
from pymongo.database import Database
from django.conf import settings


def get_mongo_client() -> MongoClient:
    """
    Creates and returns a MongoDB client connection based on Django settings.

    Constructs the connection URI using MONGODB_HOST, MONGODB_PORT, and optionally
    MONGODB_USERNAME and MONGODB_PASSWORD from Django settings. If no username is provided,
    creates an unauthenticated connection.

    Returns:
        MongoClient: An instance of PyMongo's MongoClient connected to the MongoDB server.

    Raises:
        ConnectionError: If the connection to MongoDB fails.
    """
    uri = f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/"
    if not settings.MONGODB_USERNAME:
        uri = f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/"
    return MongoClient(uri)


def get_mongo_db(db_name: str = "zibal_db") -> Database:
    """
    Returns a MongoDB database instance for the Zibal application.

    Uses get_mongo_client() to establish a connection and returns the 'zibal_db' database.
    This is the main database access point for the Zibal transaction system.

    Returns:
        Database: A MongoDB database instance configured for Zibal operations.

    Example:
        db = get_mongo_db()
        transactions = db.transactions.find()
    """
    client = get_mongo_client()
    return client.get_database()
