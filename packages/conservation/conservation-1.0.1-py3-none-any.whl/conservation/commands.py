import argparse
import textwrap
import sys
from conservation.version import __version__
from conservation.conservation_codon import main as codon_main


def conservation_parser():
    usage = '''\
    conservation <command> [options]
    Commands:
        codon           Codon conservation analysis
    Run conservation <command> -h for help on a specific command.
    '''
    parser = argparse.ArgumentParser(
        description='Conservation: Codon and Amino Acid Conservation Analysis',
        usage=textwrap.dedent(usage)
    )

    parser.add_argument('-v', '--version', action='version', version=f'conservation {__version__}')
    parser.add_argument('command', nargs='?', help='Subcommand to run')

    return parser


def codon_parser():
    from conservation.conservation_codon import parse_args
    return parse_args()


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'codon':
        # Shift sys.argv so codon_main sees the correct arguments
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        codon_main()
        return 0

    parser = conservation_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == 'codon':
        # Should already be handled above
        pass
    else:
        sys.stderr.write(f"Unknown command: {args.command}\n")
        parser.print_help()
        return 1

    return 0

