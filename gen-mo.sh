#! /bin/bash
pushd po
for i in *.po
do
po=$i
msgmerge "$po" "ojuba-virtual-cd.pot" > "$po.tmp" && \
mv "$po.tmp" "$po"
mkdir -p "../locale/${po/.po/}/LC_MESSAGES/"
msgfmt -o "../locale/${po/.po/}/LC_MESSAGES/ojuba-virtual-cd.mo" "$po"
done
popd

