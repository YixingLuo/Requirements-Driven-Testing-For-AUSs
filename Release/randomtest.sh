#!/bin/sh

prefix="timeout `expr $2 + 10`"

if which wine64
then
	prefix="$prefix wine64"
fi

logdir=$(mktemp -d log/$(date '+%Y%m%d_%H%M')_XXX)

echo $logdir

git status > $logdir/git_status

echo rev=$(git rev-parse HEAD), timout=$2 > $logdir/info

for i in $(seq 1 $1); do
	out=$logdir/$i.out
	cfg=$logdir/config_$i.json
	exj_parser config_ex.json $cfg
	$prefix ./dynamic_cost.exe -i "$cfg" -c $2 > "$out"
done
