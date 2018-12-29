# Parsing command-line arguments in Python
The GUI based applications that a normal user interacts with on a computer form a small share of all the possible programs that are run on an os. Most scripts/tools that a developer deals with are those that are intended to be run on the command line, where generally we first mention the program that we want to run, followed by some options/arguments, to get the desired functionality. Like so:

ls command lists all the files/folders in the current directory
```bash
$ ls
bin   home            lib64       opt   sbin  tmp      vmlinuz.old
boot  initrd.img      lost+found  proc  snap  usr
dev   initrd.img.old  media       root  srv   var
etc   lib             mnt         run   sys   vmlinuz
```
...well, not all of them. 
By default, it doesn't show the hidden files/folders. For that, you need to pass the -a option:
```bash
$ ls -a
.     boot  initrd.img      lost+found  proc  snap  usr
..    dev   initrd.img.old  media       root  srv   var
.rnd  etc   lib             mnt         run   sys   vmlinuz
bin   home  lib64           opt         sbin  tmp   vmlinuz.old
```
Notice three new entries: `.rnd`, `.`, and `..`. Among them, `.rnd` is a hidden file. For more info on the other two, Google is your friend :p 

Think of the programs like functions that run on the terminal. Arguments give us a powerful way to modify their default behaviour, provided the program actually supports them.

Let's assume you've made a wonderful script to download youtube videos to your computer. Well, obviously, you'll need to accept the links to videos, desired quality, etc. from the user. You can't just keep editing the source file every time you want to download a new video (admit it, all of us have done this at some point or so :3) The simplest way to do this is to parse the command line arguments.
Fortunately for Python devs, the standard library contains not one, but TWO different modules to handle user arguments.

## [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)
This is the most bare-bones you can get. It is simply a list of all the strings that were entered in the command line. For those who know, it's pretty similar to `argv` in ```int main(int argc, char *argv[])``` in C/C++ or `args` in `public static void main(String[] args)` in Java. 

`argv[0]` refers to the name of the python file itself, and the rest of the arguments are accessible from `argv[1:]`.
Example:
```python
import sys

if len(sys.argv) > 1: 
    print("Script:", sys.argv[0])
    print("Arg:", sys.argv[1])
else: 
    print("No arguments")
```
On the command line:
```
$ python test.py Foo
Script: test.py
Arg: Foo
```

For two/three arguments this is great! But as the need for complexity increases, directly using `sys.argv` becomes infeasible.

## [argparse](https://docs.python.org/3/library/argparse.html)
Enter [argparse](https://docs.python.org/3/library/argparse.html). This module makes it easy to write user-friendly command-line interfaces. After you define what arguments your script requires, `argparse` will figure out how to parse those out of `sys.argv`. This module also automatically generates help and usage messages and issues errors when users give the program invalid arguments.


We'll start simple:
```python
# downloader.py

import argparse

parser = argparse.ArgumentParser()
parser.parse_args()
```
Let's switch to the command line:
```bash
$ python downloader.py
```

This doesn't do anything, as our script is nearly empty :P.

But the `argparse` does have some built-in defaults. It adds the help message, and gives an error for unrecognized arguments (which is everything except `help` for now).
```bash
$ python downloader.py --help
usage: downloader.py [-h]

optional arguments:
  -h, --help  show this help message and exit
$ python downloader.py --verbose
usage: downloader.py [-h]
downloader.py: error: unrecognized arguments: --verbose
$ python downloader.py foo
usage: downloader.py [-h]
downloader.py: error: unrecognized arguments: foo
```

#### Positional arguments
Next, we allow the user to enter the link to the video they want to download.
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('link', help="download video from given link")
parser.parse_args()
```

```bash	
$ python3 downloader.py --help
usage: downloader.py [-h] link

positional arguments:
  link        download video from given link

optional arguments:
  -h, --help  show this help message and exit

```
Since our script will be useless if no video link is provided, we make it mandatory to be specified.
```
$ python downloader.py 
usage: downloader.py [-h] link
downloader.py: error: the following arguments are required: link
```

#### Optional Arguments
A typical scenario that arises in command line scripts, is sometimes, we want the program to display minimal information when it is running, and other times, we want a relatively detailed information of each step. For example, normally, you would just specify the video link and run our downloader, and a progress bar of the download is shown. But suppose we want more information, like the exact download url, the audio/video quality, etc, so as to make it more "verbose".

To specify this type of behaviour, the user can enter optional arguments, also called as flags, which modify the script a little, instead of serving as main inputs.
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('link', help="download video from given link")
parser.add_argument('--verbosity', help="specify output verbosity")
args = parser.parse_args()

if args.verbosity:
    print("Verbose mode")
# Your awesome script here
```
By default, the ArgumentParser considers all arguments starting with `-` to be optional.
```
$ python downloader.py --help                     
usage: downloader.py [-h] [--verbosity VERBOSITY] link

positional arguments:
  link                  download video from given link

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY specify output verbosity
$ python downloader.py --verbosity 1 https://link/to/video
Verbose mode
```
#### Short Options
Most command line apps have a simpler way to specify optional arguments, mentioning the argument with only one or two letters. Here's how to do that in argparse:
```python
parser.add_argument('-v', '--verbosity', help="specify output verbosity")
```
This saves us from typing that long word every time.
```
$ python downloader.py -v 1 https://link/to/video
Verbose mode
```
(P.S. If you have been paying attention, you would notice that the `--help` option also has the short option `-h`.)
### Moving forward
Now that we know how to take positional arguments and optional arguments, we can explore some more features provided by the `argparse` library.

#### Limiting choices for options
Suppose we allow the user to specify the video quality that they want to be downloaded. The available options are `1080p`, `720p`, `480p`, and all other choices are invalid. This can be easily added by providing the `choices` parameter to the `add_argument` function.
```python
# previous code here
parser.add_argument('-v', '--verbosity', help="specify output verbosity")
parser.add_argument('-q', '--quality', choices=['1080p', '720p', '480p'],
                    help="specify video quality")
args = parser.parse_args()

if args.verbosity:
    print("Verbose mode")
    if args.quality:
        print("Downloading", args.quality)
```

```
$ python downloader.py --help
usage: downloader.py [-h] [-v VERBOSITY] [--quality {1080p,720p,480p}] link

positional arguments:
  link                  download video from given link

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSITY, --verbosity VERBOSITY
                        specify output verbosity
  --quality {1080p,720p,480p}
                        specify video quality
$ python downloader.py -q 240p https://path/to/vid -v 1
usage: downloader.py [-h] [-v VERBOSITY] [-q {1080p,720p,480p}] link
downloader.py: error: argument -q/--quality: invalid choice: '240p' (choose from '1080p', '720p', '480p')
```
#### Specifying defaults
For most optional requirements, we have to ensure a sane default value is provided in case the user doesn't enter any. This is done using the `default` parameter.
```python
parser.add_argument('-q', '--quality', choices=['1080p', '720p', '480p'],
                    default='720p', help="specify video quality")
```
```
$ python downloader.py https://path/to/vid -v 1 
Verbose mode
Downloading 720p
```
#### Specifying value type
Let's have the script add the ability to do parallel downloads. The user can specify the number of threads.
```python
parser.add_argument('-t', '--threads', type=int, choices=range(1, 32),
                    default=1, help='number of threads for downloading')
args = parser.parse_args()

if args.verbosity:
    print("Verbose mode")
    print("Downloading", args.quality)
    print("Downloading with {} threads".format(args.threads))

```
```
$ python downloader.py https://path/to/vid -v 1 -t 3
Verbose mode
Downloading 720p
Downloading with 3 threads
```
#### Specifying number of required arguments
We can even have more values for the required parameter. For example, we can allow the user to download multiple videos in the same command.
```python
parser.add_argument('links', nargs='+', help="download videos from given links")
```
Notice the `nargs='+'` parameter. The `'+'` means that there at be any number of values for the given argument(`link` in this case), but if no argument is provided, it will generate an error. The result will be stored in a `list`.
```
$ python downloader.py --help
usage: downloader.py [-h] [-v VERBOSITY] [-q {1080p,720p,480p}]
                     [-t {1 .. 31}]
                     links [links ...]

positional arguments:
  links                 download videos from links

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSITY, --verbosity VERBOSITY
                        specify output verbosity
  -q {1080p,720p,480p}, --quality {1080p,720p,480p}
                        specify video quality
  -t {1 .. 31}, --threads {1 .. 31}
                        number of threads for downloading
```
Other possible values for `nargs` are:
1) `N` (an integer): `N` arguments from the command line will be gathered together into a list.
2) `'?'`: If an argument is given, it will be used, otherwise `default` will be used. Remember this as *either one or zero*.
3) `'*'`: Same as `+`, but doesn't generate an error if argument is not given. Remember as *zero or more*.
4) `argparse.REMAINDER`: ALL the remaining command-line arguments are gathered into a list. Not very useful for us.
### More POWER!!
What we have seen till now barely scratches the surface of the powerful, yet flexible `argparse` library. For advanced use cases, from handling conflicting options, to using a custom `Formatter`, you can refer to the official [docs](https://docs.python.org/3/library/argparse.html) for a comprehensive reference.
