import argparse
import os
from pathlib import Path
from tkinter import filedialog
import fsutils.functions


parser = argparse.ArgumentParser(description='Parses a given directory and its subdirectories and copies the files ordered to \
                                              the given destination path')
parser.add_argument('-t', '--testcase', type=int, default=0, action='store', dest='test_case',
                    help='Test case number, selects the way to parse the source_path')
parser.add_argument('-s', '--source', action='store', dest='source_path',
                    help='Identifies the source path')
parser.add_argument('-d', '--destination', action='store', dest='dest_path',
                    help='Identifies the destination path')
parser.add_argument('-f', '--useextfilter', action='store_true', dest='use_filter',
                    help='Activate filter usage')

args = parser.parse_args()

# parser.print_help()

ext_filter = ['doc', 'docx', 'xls', 'xlsx', 'zip', '']
test_case = 1
args.source_path = 'C:\\Users\\Thomas\Documents'
args.dest_path = 'C:\\Daten\\_TestDir'

if args.source_path is None:
    root_dir = filedialog.askdirectory(initialdir='C:\\', title='Choose a directory to copy from')
    if root_dir is not None:
        print('root_dir = %s' % str(root_dir))
        root_dir = str(Path(root_dir).absolute())
        print('root_dir = %s' % root_dir)
else:
    root_dir = args.source_path
# root_dir = 'c:\\tmp' if args.source_path is None else args.source_path
# root_dir = 'c:\\Daten\\Audio\\20-Tobias-Collection'

if args.dest_path is None:
    dest_dir = filedialog.askdirectory(initialdir='C:\\', title='Choose a directory to copy to')
    if dest_dir is not None:
        print('dest_dir = %s' % str(dest_dir))
else:
    dest_dir = args.dest_path

if test_case == 1:
    print('-start')
    len_offset = len(root_dir.split(os.sep))
    pathIterator = fsutils.functions.scan_tree(root_dir)
    try:
        while True:
            item = next(pathIterator)
            if item is not None:
                rec_level = len(item.path.split(os.sep))
                if item.is_file(follow_symlinks=False):
                    ext = Path(item.name).suffix[1:]
                    if not args.use_filter or ext in ext_filter:
                        fsutils.functions.copy_entry(item, dest_dir, 'ext')
                    print('f{0}: {1}'.format(rec_level, item.name))
                else:
                    print('d{0}: {1}'.format(rec_level, item.name))
    except StopIteration:
        pass
    pathIterator.close()
    print('-finish')
elif test_case == 2:
    print('Total size of files in {0} is {1} bytes'.format(root_dir, fsutils.functions.get_tree_size(root_dir)))
