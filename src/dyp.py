import argparse
import file_parser

parser = argparse.ArgumentParser(description="Document your Prolog")
parser.add_argument('-m', '--main', type=str, help='Main file of the project',)
parser.add_argument('-d', '--src-dir', type=str, help='Directory with all the sources')
parser.add_argument('-r', '--recursive', type=bool, help='Parse source directory recursively')
args = parser.parse_args()


print "Parsing:", args.main
main_file = file_parser.file_parser(args.main, ["min/2", "max/2", "asdf/2"])

