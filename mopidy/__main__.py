import asyncore
import logging
import multiprocessing
import optparse
import os
import sys

sys.path.insert(0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from mopidy import settings, SettingsError
from mopidy.process import CoreProcess
from mopidy.utils import get_class

logger = logging.getLogger('mopidy.main')

def main():
    options, args = _parse_options()
    _setup_logging(options.verbosity_level)
    core_queue = multiprocessing.Queue()
    core = CoreProcess(core_queue)
    core.start()
    get_class(settings.SERVER)(core_queue)
    asyncore.loop()

def _parse_options():
    parser = optparse.OptionParser()
    parser.add_option('-q', '--quiet',
        action='store_const', const=0, dest='verbosity_level',
        help='less output (warning level)')
    parser.add_option('-v', '--verbose',
        action='store_const', const=2, dest='verbosity_level',
        help='more output (debug level)')
    return parser.parse_args()

def _setup_logging(verbosity_level):
    if verbosity_level == 0:
        level = logging.WARNING
    elif verbosity_level == 2:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(format=settings.CONSOLE_LOG_FORMAT, level=level)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')
    except SettingsError, e:
        sys.exit('%s' % e)
