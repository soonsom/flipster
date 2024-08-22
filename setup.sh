echo "parameter total count: $#"
PLATFORM=$1
DEVICE=$2
ID=$3
PASSWORD=$4
BALANCE=$5
TOTAL_VALUE=$6


function run() {
  mkdir -p logs/${PLATFORM}
  head -n 1 testinfo.env > testinfo-run.env
  tail -n +2 testinfo.env > testinfo-${DEVICE}.env
  sed -i '' s/testdevice/${DEVICE}/g testinfo-"${DEVICE}".env
  sed -i '' s/testplatform/${PLATFORM}/g testinfo-run.env
  sed -i '' s/testid/${ID}/g testinfo-"${DEVICE}".env
  sed -i '' s/testpassword/${PASSWORD}/g testinfo-"${DEVICE}".env
  sed -i '' s/testbalance/${BALANCE}/g testinfo-"${DEVICE}".env
  sed -i '' s/testtotalvalue/${TOTAL_VALUE}/g testinfo-"${DEVICE}".env
}


function guidance() {
  echo "--- Missing parameters, please enter parameters as below. ---"
  echo "$0 PLATFORM, DEVICE, ID, PASSWORD, BALANCE, TOTAL_VALUE"
}


if [ $# -eq 6 ]
  then
    run
  else
    guidance
    exit 1
fi