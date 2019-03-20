from pathlib import Path


class FilePrepender(object):
    """
    Class FilePrepender
    Used as context manager class for pre- or appending
    lines to the given file. The file might exists or
    it newly created.
    Lines of the file are stored in a list.
    Shall be used with 'with' statement, e.g.
    with FilePrepender(filepath) as file:
        file.prepend_line('line inserted at first line in file')
        file.append_line('line appended at end of file')
    """
    def __init__(self, file_path):
        """
        Class constructor
        :param file_path: path to the file to open or create
        :type file_path: basestring
        """
        self.__write_queue = []
        # Read in the existing file, so we can write it back later
        if Path(file_path).exists():
            with open(file_path, mode='r') as fileDesc:
                self.__write_queue = fileDesc.readlines()

        self.__open_file = open(file_path, mode='w')

    def prepend_line(self, line):
        """
        Member function to prepend given line in file.
        :param line:    line inserted at beginning of file
        :type line:     basestring
        :return:        None
        :rtype:         None
        """
        self.__write_queue.insert(0, "%s\n" % line)

    def append_line(self, line):
        """
        Member function to append given line in containing file.
        :param line:    line appended at end of file
        :type line:     basestring
        :return:        None
        :rtype:         None
        """
        if not "%s\n" % line in self.__write_queue:
            self.__write_queue.append("%s\n" % line)

    def close(self):
        """
        close function for 'with' statement
        :return:
        :rtype:
        """
        self.__exit__(None, None, None)

    def __enter__(self):
        """
        Context manager's __enter__ function implementation
        :return:    self
        :rtype:     FilePrepender
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Context manager's __exit__ function implementation
        :param type:        exception type
        :type type:
        :param value:       exception value
        :type value:
        :param traceback:
        :type traceback:
        :return:            if True and if exception given, exception is suppressed
        :rtype:             None or bool
        """
        if self.__write_queue:
            self.__open_file.writelines(self.__write_queue)
        self.__open_file.close()


if __name__ == '__main__':
    with FilePrepender('test_d.out') as f:
        # Must write individual lines in reverse order
        f.prepend_line('This will be line 3')
        f.prepend_line('This will be line 2')
        f.prepend_line('This will be line 1')

    with FilePrepender('test_d.out') as f:
        # Or, use write_lines instead - that maintains order.
        f.append_line('This will be line 1.1')
        f.append_line('This will be line 1.2')
        f.append_line('This will be line 1.3')

    with FilePrepender('test_d.out') as f:
        f.prepend_line('now first line')
