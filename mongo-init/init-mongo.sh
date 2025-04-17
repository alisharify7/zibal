#"""
#* Zibal Payment Test Task
#* Provisioning MongoDB
#* Developer: Ali Sharifi
#* Email: alisharifyofficial@gmail.com
#* Website: ali-sharify.ir
#* GitHub: github.com/alisharify7/zibal
#* Repository: https://github.com/alisharify7/zibal
#"""

#!/bin/bash
set -e

MONGO_USER=${MONGO_INITDB_ROOT_USERNAME:-root}
MONGO_PASS=${MONGO_INITDB_ROOT_PASSWORD:-example}

until mongosh --host mongo --username $MONGO_USER --password $MONGO_PASS --eval "print(\"waited for connection\")"
do
    sleep 1
done

mongorestore --host mongo \
             --port 27017 \
             --username $MONGO_USER \
             --password $MONGO_PASS \
             --gzip \
             --archive=/mongo-init/dump/transaction.agz

echo "Restore completed successfully!"