#! /bin/bash
xgettext -o "po/ojuba-virtual-cd.pot" -L python ojuba-virtual-cd
pushd po
for i in *.po
do
po=$i
msgmerge "$po" "ojuba-virtual-cd.pot" > "$po.tmp" && \
mv "$po.tmp" "$po"
done
popd
