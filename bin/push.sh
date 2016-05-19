set -e
git add -u
git commit --amend --no-edit
git push -f
ssh roderic@projects.roderic.ca "cd forum && git reset --hard HEAD"
ssh roderic@projects.roderic.ca ".venvs/django/bin/python forum/manage.py migrate"
ssh roderic@projects.roderic.ca "supervisorctl restart forum"
