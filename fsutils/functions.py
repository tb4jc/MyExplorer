import os
import stat
import datetime
import shutil
import fsutils

from pathlib import Path
from fsutils.fileprepender import FilePrepender


def __local_log__(msg, log_func=None):
    """
    Local function for logging given message. If log_func is set, given message is appended to it, else the message is
    printed to console.
    :param msg: object containing message to log
    :type msg: string
    :param log_func: object the messsage is appended if not None
    :type log_func: list
    :return: None
    :rtype: None
    """
    if log_func is not None:
        log_func(msg)
    else:
        print(msg)


def copy_entry(entry, dest_dir, order_type='ext', log_func=None):
    """
    Recursively copies given entry to given destination directory based on given ordering type.
    It creates .metafiles containing original full path of copied files.
    If target file already exists, it chooses younger file, else it just appends original file path to meta file
    :param entry: full path to file to copy
    :type entry: string
    :param dest_dir: full path to destination directory
    :type dest_dir: string
    :param order_type: order type used by function, either 'year' for year base ordering using, else it's based on extension
    last access time stamp
    :type order_type: string
    :param log_func: object for appending log messages to
    :type log_func: list
    :return: None
    :rtype: None
    """
    dest_dir_path = Path(dest_dir)
    source_path = Path(entry.path)
    if order_type == 'year':
        entry_datetime = datetime.datetime.fromtimestamp(entry.stat(follow_symlinks=False).st_mtime)
        year = entry_datetime.year
        year_path = dest_dir_path / str(year)
        # __local_log__('year of file {0} = {1}'.format(entry.name, year), log_func)
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
        # if file exists, check also timestamp
        src_stat = entry.stat(follow_symlinks=False)
        src_mod_time = src_stat.st_mtime
        src_size = src_stat.st_size
        dst_stat = os.stat(str(dest_file_path))
        dst_mod_time = dst_stat.st_mtime
        dst_size = dst_stat.st_size
        # used solution so far:
        # if modification time is younger -> file is copied and added to first line in meta
        # else file is not copied but source path is appended to meta, if not already in
        if src_mod_time <= dst_mod_time: # and src_size == dst_size:
            __local_log__('Source file "%s" is older or same age as existing file - file not copied' % entry.name, log_func)
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
    with FilePrepender(meta_file_path, log_func) as meta_file:
        if replaced:
            meta_file.prepend_line(entry.path)
        else:
            meta_file.append_line(entry.path)


def scan_tree(path, log_func=None):
    """
    Recursively scans the given root directory and its sub-directories.
    Skips links and junctions.
    :param path: full path to root directory to scan
    :type path: string
    :param log_func: object for appending log messages to
    :type log_func: list
    :return: object pointing to next file
    :rtype: iterator
    """
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                dir_stats = entry.stat()
                if fsutils.platf_is_win and dir_stats.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    __local_log__('on Windows: %s is a junction and skipped' % entry.name, log_func)
                elif not entry.name.startswith('.'):
                    yield from scan_tree(entry.path)
                else:
                    __local_log__('skipping directory "%s" starting with dot' % entry.name, log_func)
                    pass
            else:   # skip symbolic links
                __local_log__('skipping symbolic link %s' % entry.name, log_func)
                pass


def get_tree_size(path, log_func=None):
    """
    Returns total size of files in given path and sub-directories.
    :param path: full path to root directory
    :type path: string
    :param log_func: object the messsage is appended if not None
    :type log_func: list
    :return: size of all files within directory
    :rtype: int
    """
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            dir_stats = entry.stat()
            if fsutils.platf_is_win and dir_stats.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                __local_log__('%s is a junction' % entry.name, log_func)
                pass
            else:
                total += get_tree_size(entry.path)
        elif entry.is_file(follow_symlinks=False):
            total += entry.stat().st_size
        else:   # skip symbolic links
            __local_log__('skipping symoblic link %s' % entry.name, log_func)
            pass
    return total
