import sys
import os

def get_source():
    if not sys.argv[1] or sys.argv[1] not in ('training', 'validation'):
        raise Exception('Needed to specify what data to get')
    else:
        if sys.argv[1]=='training':
            return 'training'
        else:
            return os.environ['VAL_SOURCE']