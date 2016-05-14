set -e
../manage.py test ..
git add -u
git commit --amend --no-edit > /dev/null
git push -f
ssh roderic@projects.roderic.ca "cd forum && git reset --hard HEAD"
ssh roderic@projects.roderic.ca ".venvs/notes/bin/python forum/manage.py migrate"
ssh roderic@projects.roderic.ca "supervisorctl restart forum"
