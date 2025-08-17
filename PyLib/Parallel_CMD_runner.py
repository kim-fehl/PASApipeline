#!/usr/bin/env python3

import sys
import os
import subprocess
import time




def run_commands (cmd_list, max_simult_processes=10):

    procs = []
    failed_procs = []
    
    for cmd in cmd_list:

        while len(procs) >= max_simult_processes:

            time.sleep(10)
            
            # wait until one opens up
            not_done = []

            for p in procs:
                ret = p['proc'].poll()
                if ret != None:
                    if ret != 0:
                        # errored out
                        failed_procs.append(p)
                        print("process errored: CMD: " + p['cmd'], file=sys.stderr)
                    else:
                        # exited normally
                        print("process completed successfully", file=sys.stderr)
                else:
                    # process still running
                    not_done.append(p)
                    print("process still running", file=sys.stderr)

            procs = not_done
        
            
        # execute command
        print("CMD: " + cmd, file=sys.stderr)

        p = { 'proc':None, 'cmd':None }
        p['proc'] = subprocess.Popen(cmd, shell=True)
        p['cmd'] = cmd
        procs.append(p)


    # wait for remaining ones to complete
    for p in procs:
        ret = p['proc'].wait()
       
        if ret != 0:
            # errored out
            failed_procs.append(p)
            print("process errored: CMD: " + p['cmd'], file=sys.stderr)
        else:
            # exited normally
            print("process completed successfully", file=sys.stderr)



    print("There were " + str(len(failed_procs)) + " failed processes.", file=sys.stderr)
    
    return failed_procs


if __name__ == "__main__":

    test_cmds = [ 'sleep 1',
                  'sleep 2',
                  'sleep 3',
                  'sleep 4',
                  'sleep x',
                  'sleep 6',
                  'doh',
                  'sleep 2' ]
                      
    run_commands(test_cmds, 2)
    
    sys.exit(0)
