#!/bin/sh
  
set -e

echo "Testing python3 package $1"
for py in $(py3versions -r 2>/dev/null) ; do
    cd "$AUTOPKGTEST_TMP" ;
    echo "Testing with $py:" ;
    $py -c "import $2; print($2)" ;
done
