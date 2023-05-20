#!/bin/bash
CONFIGFS=/sys/kernel/config

# FIND ALL LUN
luns=$(ls -d $CONFIGFS/target/iscsi/*/tpgt_*/lun/lun_*/)

badtargets=""

for lun in $luns
do
        # Extract target name from lun path
        target=$(basename $(realpath "$lun"/../../..))

        # Extract portal from lun path
        portal=$(ls "$lun"/../../np/)

        # find soft link from lun path
        sl=$(find "$lun" -maxdepth 1 -type l | wc -l)

        # if there is no softlink we can assume there is no link to backend device
        if [ "$sl" -eq 0 ]
        then
                result="BAD"
                badtargets=$(echo -e "$badtargets\n$target $portal")
        else
                result="OK"
        fi

        echo "$target $portal $result"
done

echo
echo "BAD TARGET: "
echo "$badtargets" | grep -v "^$" | sort | uniq 
