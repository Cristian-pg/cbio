import argparse
import os
import tailer as tl
import io
# from biofiles import vcf

class VCF():
    def __init__(self, filepath, args):
        self.filepath = filepath
        self.args = args

    def head(self):
        print('==> HEAD OF VCF FILE <==')
        c = 0
        fhand = open(self.filepath, 'r')
        for line in fhand:
            if line.startswith('##'):
                continue
            elif line.startswith('#'):
                print(line.strip('\n'))
                continue

            line = line.strip('\n').split('\t')

            if self.args.pretty:
                line[7] = line[7][0:4] + '[...]' + line[7][-7:]
            print('\t'.join(line))
            c += 1

            if c == 5:
                print()
                fhand.close()
                break

        return ()

    def tail(self):
        c = 0
        print('==> TAIL OF VCF FILE <==')
        print('#' + "\t".join(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']))

        fhand = open(self.filepath)
        lastLines = tl.tail(fhand, 5)
        fhand.close()

        for line in lastLines:
            if line.startswith('##'):
                continue
            elif line.startswith('#'):
                print(line.strip('\n'))
                continue

            line = line.strip('\n').split('\t')

            if self.args.pretty:
                line[7] = line[7][0:4] + '[...]' + line[7][-7:]
            print('\t'.join(line))
            c += 1

            if c == 5:
                print()
                break

        return ()


def vcf_analysis(args):
    filepath = os.path.abspath(args.vcf)

    vcf = VCF(filepath, args)

    vcf.head()
    vcf.tail()



def vcf_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--vcf", help='Location to tf state file',
                       required=True)
    add_arg.add_argument("-f", "--head", help='First Variants in VCF')
    add_arg.add_argument("-t", "--tail", help='Lasts Variants in VCF')
    add_arg.add_argument("-p", "--pretty", action='store_true', help='Pretty print VCF')

    return add_arg

def parse_options():
    parser = argparse.ArgumentParser(description='Any description to be displayed for the program.')
    # Create a subcommand
    subparsers = parser.add_subparsers(help='Add sub commands', dest='command')
    # Define a primary command apply & set child/sub commands for apply
    add_p = subparsers.add_parser('vcf', help='Apply your changes to system')
    vcf_sub_commands(add_p)
    # add_p = subparsers.add_parser('destroy', help='Destroy the infra from system')
    # sub_commands(add_p)
    # add_p = subparsers.add_parser('plan', help='Verify your changes before apply')
    # sub_commands(add_p)
    args = parser.parse_args()
    return args


def main():

    # parse some argument lists
    # args = parser.parse_args()

    args = parse_options()

    if args.command == 'vcf':
        vcf_analysis(args)

if __name__ == "__main__":

    main()
