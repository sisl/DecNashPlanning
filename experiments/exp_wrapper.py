# experiment.py

import os
if __name__ == '__main__':
    loc = 0
    frames = 1000
    for exp in ['decnash','idm','cnash']:
        for track in range(5):
            # run
            command = 'python experiments/experiment.py --loc %i --track %i --exp %s --frames %i' %(loc, track, exp, frames)
            os.system(command)
            
        
        
        