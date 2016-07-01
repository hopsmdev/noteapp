#! /bin/bash
export MONGODB_USER='test'
export MONGODB_PASSWORD='test'
export MONGODB_PORT=27017
export MONGODB_NAME='testdb'

docker-compose -f $(dirname "${0}")/docker-compose.yml up --force-recreate -d

docker exec test_mongodb_1 mongo $MONGODB_NAME --eval "db.dropAllUsers();
    db.createUser({ user: '$MONGODB_USER', pwd: '$MONGODB_PASSWORD', \
    roles: [ { role: 'dbOwner', db: '$MONGODB_NAME' } ] });"