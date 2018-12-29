import argparse

parser = argparse.ArgumentParser()
parser.add_argument('links', nargs='+', help="download videos from links")
parser.add_argument('-v', '--verbosity', help="specify output verbosity")
parser.add_argument('-q', '--quality', choices=['1080p', '720p', '480p'],
                    default='720p', help="specify video quality")
parser.add_argument('-t', '--threads', type=int, choices=range(1, 32),
                    default=1, help='number of threads for downloading')
args = parser.parse_args()

if args.verbosity:
    print("Verbose mode")
    print("Downloading", args.quality)
    print("Downloading with {} threads".format(args.threads))
