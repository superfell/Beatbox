#!/bin/bash
# expects that "tox" has been run
SF_SANDBOX=on .tox/py34/bin/coverage run --source beatbox demo.py $SF_USER $PASSWORD >/dev/null
for x in py27 py34; do
    .tox/${x}/bin/coverage run -a --source beatbox setup.py test >/dev/null
done
coverage html
coverage report
