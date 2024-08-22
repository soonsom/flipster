DEVICE=$1

lsof -PiTCP -sTCP:LISTEN
kill -9 $(ps -ef | grep ${DEVICE}.json | grep -v grep | awk '{print $2}')
lsof -PiTCP -sTCP:LISTEN

echo "cleaning up... ${DEVICE}"
python3 cleanup.py --device ${DEVICE}
echo "cleaned up with ${DEVICE}"
