import os
import stat
import datetime
import shutil
import fsutils

from pathlib import Path
from fsutils.fileprepender import FilePrepender

def copy_entry(entry, dest_dir, order_type='ext'):
    dest_dir_path = Path(dest_dir)
    source_path = Path(entry.path)
    if order_type == 'year':
        entry_datetime = datetime.datetime.fromtimestamp(entry.stat(follow_symlinks=False).st_mtime)
        year = entry_datetime.year
        year_path = dest_dir_path / str(year)
        # print('year of file {0} = {1}'.format(entry.name, year))
        meta_path = year_path / '.metafiles'
        if not meta_path.exists():
            meta_path.mkdir(parents=True)
        dest_file_path = year_path / entry.name
        meta_file_path = year_path / '.metafiles' / (entry.name + '.metafile')
    else:
        ext_path = dest_dir_path / '__' if source_path.suffix is '' else dest_dir_path / source_path.suffix[1:]
        meta_path = ext_path / '.metafiles'
        if not meta_path.exists():
            meta_path.mkdir(parents=True)
        dest_file_path = ext_path / entry.name
        meta_file_path = ext_path / '.metafiles' / (entry.name + '.metafile')
    replaced = True
    if dest_file_path.exists():
        """if file exists, check also timestamp"""
        src_stat = entry.stat(follow_symlinks=False)
        src_mod_time = src_stat.st_mtime
        src_size = src_stat.st_size
        dst_stat = os.stat(str(dest_file_path))
        dst_mod_time = dst_stat.st_mtime
        dst_size = dst_stat.st_size
        # used solution so far:
        # if modification time is younger -> file is copied and added to first line in meta
        # else file is not copied but source path is appended to meta
        if src_mod_time <= dst_mod_time: # and src_size == dst_size:
            print('Source file is older or same age as existing file - file not copied')
            replaced = False
        else:
            shutil.copy2(entry.path, str(dest_file_path))
            # files with index extension as possible solution
            # search_path = str(dest_file_path) + '*'
            # files = glob.glob(str(search_path))
            # nr_of_files = len(files)
            # if nr_of_files == 0:
            #     shutil.copy2(entry.path, str(dest_file_path))
            # else:
            #     shutil.copy2(entry.path, str(dest_file_path) + '.' + str(nr_of_files))
    else:
        shutil.copy2(entry.path, str(dest_file_path))
    # meta_file_path = str(dest_file_path) + '.filemeta'
    with FilePrepender(meta_file_path) as meta_file:
        if replaced:
            meta_file.prepend_line(entry.path)
        else:
            meta_file.append_line(entry.path)


def scan_tree(path):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                dir_stats = entry.stat()
                if fsutils.platf_is_win and dir_stats.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    print('%s is a junction' % entry.name)
                    pass
                elif entry.name.startswith('.'):
                    yield from scan_tree(entry.path)
                else:
                    print('skipping directory starting with dot on parsing')
                    pass
            else:   # skip symbolic links
                print('skipping symoblic link %s' % entry.name)
                pass


def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            dir_stats = entry.stat()
            if fsutils.platf_is_win and dir_stats.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                print('%s is a junction' % entry.name)
                pass
            else:
                total += get_tree_size(entry.path)
        elif entry.is_file(follow_symlinks=False):
            total += entry.stat().st_size
        else:   # skip symbolic links
            print('skipping symoblic link %s' % entry.name)
            pass
    return total
