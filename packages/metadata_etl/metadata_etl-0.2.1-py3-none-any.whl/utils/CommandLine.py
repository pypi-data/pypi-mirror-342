import argparse
from pathlib import Path
from .defines import Scope, PROC_STAGE


def process_arguments(args=None):
    """
    Process command-line arguments using argparse.

    Parameters:
    - args: A list of command-line arguments
            (default is None, which means using sys.argv).

    Returns:
    - A dictionary containing the parsed command-line arguments.
    """

    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS,
        prog="MetadataETL",
        description="Extract metadata from research data \
            and load it into the metadata catalog.",
        epilog="European XFEL GmbH."
    )

    # Define command-line arguments
    parser.add_argument('-b', '--base_folder', help='Base folder (default: $PWD)')
    parser.add_argument('-p', '--proposal', help='Full proposal number')
    parser.add_argument('-r', '--run', help='Run numbers', type=int)
    parser.add_argument('files', help='List of data file(s)', nargs='*', default=[])
    # We can also use the option type=argparse.FileType('r')
    # to check that the provided file names/paths are valid
    parser.add_argument('-s', '--scope', default=Scope.PROPOSAL, choices=Scope.get_scopes())
    parser.add_argument('-d', '--data', help='Input file for data and metadata specifications')
    parser.add_argument('-g', '--stage', default="load", choices=PROC_STAGE)
    parser.add_argument('-v', '--verbose', help='Verbose mode', default=False, action='store_true')

    # Parse the command-line arguments and store them in a dictionary
    # args = vars(parser.parse_args(args))
    return parser.parse_args(args)
