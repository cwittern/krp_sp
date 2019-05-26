#!/bin/bash
# concate the lei files for bu and krp corpus files

script="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root=`dirname $script`
corpusdir="$root/data"
modeldir="$root/model"

cd $corpusdir
for b in {1..6}
do
    #ls KR$b[a-z].txt
    cat KR$b[a-z].txt > KR$b.txt
done
echo "cat KR* > krp.txt"
