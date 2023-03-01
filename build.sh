#!/bin/bash

REPOSITORY=7j3k22hp.gra7.container-registry.ovh.net/tool/services/paa
BASE_PATH=.
DATE=`date +%Y-%m-%d-%H-%M-%S`

# Parse arguments
while [ $# -gt 0 ]; do
   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
        echo "Argument $1 $2"
   fi
  shift
done

VERSION=$version

if [ -z "$release" ]; then
    release=$VERSION
fi

FULL_IMAGE=$REPOSITORY:$release

echo "Build $FULL_IMAGE on $DATE"

docker build \
-f $BASE_PATH/Dockerfile \
-t $FULL_IMAGE \
.

docker push $FULL_IMAGE