from http import HTTPStatus

STAT_OPERATORS = ['count', 'mean', 'std', 'min', 'max', 'med']

PROC_STAGE = ['config', 'extract', 'transform', 'load']

MAX_RETRIES = 3
TIMEOUT = 12
SSL_VERIFY = False
PAGE_NUMBER = 1
PAGE_SIZE = 100

OK = HTTPStatus.OK
GET = 'GET'

'''
Scope: defines the scope of data processing
 - proposal: the processing spans on all runs and files,
             and the summary is aggregated at the specified proposal
 - run: the processing spans on all files for the specified run,
        and the summary is generated per run
 - file: The processing is done per file,
         and a summary is also generated for each individual file
'''


class Scope:
    # Constants representing different data processing scopes
    PROPOSAL = 'proposal'
    FILE = 'file'
    RUN = 'run'

    @staticmethod
    def get_scopes():
        """
        Return a list of all available data processing scopes.

        Returns:
        - A list containing strings representing different data processing scopes.
        """
        return [Scope.PROPOSAL, Scope.FILE, Scope.RUN]
