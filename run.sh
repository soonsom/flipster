PLATFORM=$1
DEVICE=$2
DEBUG_MODE=$3
KEYWORD_TC=$4

echo ${KEYWORD_TC}
echo "DEBUG_MODE: ${DEBUG_MODE}"

if [ ${DEBUG_MODE} == 0 ]; then
  pytest -vv -s --device ${DEVICE} -k "${KEYWORD_TC}" --capture=sys --html=results/${PLATFORM}/report-${DEVICE}.html --self-contained-html --css=utils/html_report/report.css

else
  pytest -vv -s --device ${DEVICE} -k "${KEYWORD_TC}"
fi