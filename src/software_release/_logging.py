"""Set up Application Logs

This module defines how the emitted application logs are handled and where
they are written/streamed.
The application logs are written in full details (ie with timestamps) to a file
and also streamed to the console in a more concise format.

Console:
    Stream Logs of INFO (and above) Level on Console's stderr
    The rendered Log format is: <logger name>: <log level> <log message>

Disk File:
    Write Logs of ALL Levels on a Disk File (see SOFTWARE_RELEASE_LOGS_FILE variable below)
    The rendered Log format is: <timestamp> <logger name>: <log level> <log message>

Log Levels:
- CRITICAL
- ERROR
- WARNING
- INFO
- DEBUG

Usage:
    Do a 'from . import _logging' in the root __init__.py of your package and
    all submodules 'inherit' the logging configuration at runtime.
    So, then on any module a 'import logging' is sufficient!
"""
import logging

SOFTWARE_RELEASE_LOGS_FILE = 'soft-rel.log'

#### FILE LOGGING
# set up logging to file for DEBUG Level and above so that no LOG is missed from
# the file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename=SOFTWARE_RELEASE_LOGS_FILE,
    filemode='w',
)

#### CONSOLE LOGGING
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()

# console.setLevel(logging.INFO)
console.setLevel(logging.INFO)

# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


# Now, we can log to the root logger, or any other logger. First the root...
# logging.info('Blah blah')

# Now, define a couple of other loggers which might represent areas in your
# application:

# logger1 = logging.getLogger('myapp.area1')
# logger2 = logging.getLogger('myapp.area2')
# logger3 = logging.getLogger(__name__)

# logger1.debug('balh blah')
# logger1.info('balh blah')
# logger2.warning('balh blah')
# logger3.error('balh blah')
