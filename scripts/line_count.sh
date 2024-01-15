lines=`cat *.py */*.py */*/*.py *.sh | grep -v ^$ | grep -v -E "^[\s]*#" | grep -E "^[^\S\r\n]*\S.*$" | wc -l`

echo the project currently contains $lines lines