#!/bin/bash

MONGO_USER=${MONGODB_USERNAME:-username}
MONGO_PASS=${MONGODB_PASSWORD:-admin}


# wait for mongoDB
sleep 5 # we can remove this if we can add depends_on: service_healthy to mongoDB but just for now

until mongo --host mongo -u "$MONGO_USER" -p "$MONGO_PASS" --eval "print(\"waited for connection\")"
do
    sleep 1
    echo "connecting to MongoDB ..."
done

mongorestore --host mongo \
             -u "$MONGO_USER" \
             -p "$MONGO_PASS" \
             --gzip \
             --archive=/mongo-init/transaction.agz

echo "Restore completed successfully!"