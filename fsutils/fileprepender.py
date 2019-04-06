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
    def __init__(self, file_path, log_func=None):
        """
        Class constructor
        :param file_path: path to the file to open or create
        :type file_path: basestring
        """
        self.file_path = file_path
        self.logger = log_func
        self.__write_queue = []
        # Read in the existing file, so we can write it back later
        if Path(self.file_path).exists():
            with open(file_path, mode='r') as fileDesc:
                self.__write_queue = fileDesc.readlines()

        self.__open_file = open(self.file_path, mode='w')

    def __log__(self, msg):
        """
        Local logging function which checks, if logger object is set and then it appends message to it, else
        it prints out the message to console.
        :param msg: message
        :type msg: basestring
        """
        if self.logger is not None:
            self.logger(msg)
        else:
            print(msg)

    def prepend_line(self, line):
        """
        Member function to prepend given line in file, if it does not exists already
        :param line:    line inserted at beginning of file
        :type line:     basestring
        :return:        None
        :rtype:         None
        """
        if not "%s\n" % line in self.__write_queue:
            self.__write_queue.insert(0, "%s\n" % line)
        else:
            self.__log__('line "%s" already in file "%s"' % (line, self.file_path))

    def append_line(self, line):
        """
        Member function to append given line in containing file, if it does not exists already
        :param line:    line appended at end of file
        :type line:     basestring
        :return:        None
        :rtype:         None
        """
        if not "%s\n" % line in self.__write_queue:
            self.__write_queue.append("%s\n" % line)
        else:
            self.__log__('line "%s" already in file "%s"' % (line, self.file_path))

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

    def log_test(msg):
        print(msg)


    with FilePrepender('test_d.out', log_test) as f:
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
