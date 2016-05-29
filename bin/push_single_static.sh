set -e
git add $1
git commit --amend --no-edit
git push -f
ssh roderic@projects.roderic.ca "cd forum && git reset --hard HEAD"
