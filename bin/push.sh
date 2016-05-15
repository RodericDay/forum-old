set -e
cd ..
git add *.html
git commit -m 'HTML changes - rebase!'
git push
ssh roderic@projects.roderic.ca "cd forum && git reset --hard HEAD"
