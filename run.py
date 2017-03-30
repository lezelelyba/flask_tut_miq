#!flask/bin/python

from app import main

main.run(host='0.0.0.0', debug=True, use_debugger=True)
