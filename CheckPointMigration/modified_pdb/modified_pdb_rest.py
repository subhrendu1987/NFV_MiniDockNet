#!/usr/bin/python3.7
from bottle import route, run, template
import time, subprocess, json, sys
import modified_pdb as mpdb
import os
#from bottledaemon import daemon_run
"""
PdbRest adds a REST API to Pdb.
"""
IP='localhost'
PORT="38081"
##########################################################################################
############################################################
@route('/start/')
@route('/start/<prog_name>')
def start(prog_name=''):
        ''' Start program in pdb mode
        http://127.0.0.1:38081/start/test.py'''
        if(len(prog_name)>0):
                if not os.path.exists(prog_name):
                        print('Error:', prog_name, 'does not exist')
                        sys.exit(1)
                #sys.stdin = open('input.txt')
                pdb = mpdb.Pdb(stdin=open('input.txt',"r"))
                while True:
                        pdb._runscript(prog_name)
                        if pdb._user_requested_quit:
                                break
                        else:
                                print("Execution continued")
                return({'Return':"%s Pdb session exited"%(prog_name)})
        else:
                return template('Goto <a>{{redir_url}}</a>. Missing prog_name', redir_url="http://127.0.0.1:38081/test.py")
############################################################
@route('/hello/')
def start():
	print("Hello")

##########################################################################################
run(host=IP, port=PORT, debug=True)
##########################################################################################
