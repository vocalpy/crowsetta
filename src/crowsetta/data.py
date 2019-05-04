# utility function for fetching files
# Adapted from MNE-Python under BSD-3 License
# https://github.com/mne-tools/mne-python/blob/master/mne/utils.py#L1884
# https://github.com/mne-tools/mne-python/blob/master/LICENSE.txt

from math import log
import sys
import os
import time
import urllib.request
import urllib.parse
import ftplib
import hashlib
import shutil
import tarfile
from zipfile import ZipFile
from collections.abc import Iterable


def md5sum(fname, block_size=1048576):  # 2 ** 20
    """Calculate the md5sum for a file.
    Parameters
    ----------
    fname : str
        Filename.
    block_size : int
        Block size to use when reading.
    Returns
    -------
    hash_ : str
        The hexadecimal digest of the hash.
    """
    md5 = hashlib.md5()
    with open(fname, 'rb') as fid:
        while True:
            data = fid.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def sizeof_fmt(num):
    """Turn number of bytes into human-readable str.
    Parameters
    ----------
    num : int
        The number of bytes.
    Returns
    -------
    size : str
        The size in human-readable format.
    """
    units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB']
    decimals = [0, 0, 1, 2, 2, 2]
    if num > 1:
        exponent = min(int(log(num, 1024)), len(units) - 1)
        quotient = float(num) / 1024 ** exponent
        unit = units[exponent]
        num_decimals = decimals[exponent]
        format_string = '{0:.%sf} {1}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


class ProgressBar:
    """Generate a command-line progressbar.
    Parameters
    ----------
    max_value : int | iterable
        Maximum value of process (e.g. number of samples to process, bytes to
        download, etc.). If an iterable is given, then `max_value` will be set
        to the length of this iterable.
    initial_value : int
        Initial value of process, useful when resuming process from a specific
        value, defaults to 0.
    mesg : str
        Message to include at end of progress bar.
    max_chars : int
        Number of characters to use for progress bar (be sure to save some room
        for the message and % complete as well).
    progress_character : char
        Character in the progress bar that indicates the portion completed.
    spinner : bool
        Show a spinner.  Useful for long-running processes that may not
        increment the progress bar very often.  This provides the user with
        feedback that the progress has not stalled.
    Example
    -------
    >>> progress = ProgressBar(13000)
    >>> progress.update(3000) # doctest: +SKIP
    [.........                               ] 23.07692 |
    >>> progress.update(6000) # doctest: +SKIP
    [..................                      ] 46.15385 |
    >>> progress = ProgressBar(13000, spinner=True)
    >>> progress.update(3000) # doctest: +SKIP
    [.........                               ] 23.07692 |
    >>> progress.update(6000) # doctest: +SKIP
    [..................                      ] 46.15385 /
    """

    spinner_symbols = ['|', '/', '-', '\\']
    template = '\r[{0}{1}] {2:.05f} {3} {4}   '

    def __init__(self, max_value, initial_value=0, mesg='', max_chars=40,
                 progress_character='.', spinner=False,
                 verbose_bool=True):
        self.cur_value = initial_value
        if isinstance(max_value, Iterable):
            self.max_value = len(max_value)
            self.iterable = max_value
        else:
            self.max_value = float(max_value)
            self.iterable = None
        self.mesg = mesg
        self.max_chars = max_chars
        self.progress_character = progress_character
        self.spinner = spinner
        self.spinner_index = 0
        self.n_spinner = len(self.spinner_symbols)
        self._do_print = verbose_bool
        self.cur_time = time.time()
        self.cur_rate = 0

    def update(self, cur_value, mesg=None):
        """Update progressbar with current value of process.
        Parameters
        ----------
        cur_value : number
            Current value of process.  Should be <= max_value (but this is not
            enforced).  The percent of the progressbar will be computed as
            (cur_value / max_value) * 100
        mesg : str
            Message to display to the right of the progressbar.  If None, the
            last message provided will be used.  To clear the current message,
            pass a null string, ''.
        """
        cur_time = time.time()
        cur_rate = ((cur_value - self.cur_value) /
                    max(float(cur_time - self.cur_time), 1e-6))
        # cur_rate += 0.9 * self.cur_rate
        # Ensure floating-point division so we can get fractions of a percent
        # for the progressbar.
        self.cur_time = cur_time
        self.cur_value = cur_value
        self.cur_rate = cur_rate
        progress = min(float(self.cur_value) / self.max_value, 1.)
        num_chars = int(progress * self.max_chars)
        num_left = self.max_chars - num_chars

        # Update the message
        if mesg is not None:
            if mesg == 'file_sizes':
                mesg = '(%s / %s, %s/s)' % (
                    sizeof_fmt(self.cur_value).rjust(8),
                    sizeof_fmt(self.max_value).rjust(8),
                    sizeof_fmt(cur_rate).rjust(8))
            self.mesg = mesg

        # The \r tells the cursor to return to the beginning of the line rather
        # than starting a new line.  This allows us to have a progressbar-style
        # display in the console window.
        bar = self.template.format(self.progress_character * num_chars,
                                   ' ' * num_left,
                                   progress * 100,
                                   self.spinner_symbols[self.spinner_index],
                                   self.mesg)
        # Force a flush because sometimes when using bash scripts and pipes,
        # the output is not printed until after the program exits.
        if self._do_print:
            sys.stdout.write(bar)
            sys.stdout.flush()
        # Increment the spinner
        if self.spinner:
            self.spinner_index = (self.spinner_index + 1) % self.n_spinner

    def update_with_increment_value(self, increment_value, mesg=None):
        """Update progressbar with an increment.
        Parameters
        ----------
        increment_value : int
            Value of the increment of process.  The percent of the progressbar
            will be computed as
            (self.cur_value + increment_value / max_value) * 100
        mesg : str
            Message to display to the right of the progressbar.  If None, the
            last message provided will be used.  To clear the current message,
            pass a null string, ''.
        """
        self.update(self.cur_value + increment_value, mesg)

    def __iter__(self):
        """Iterate to auto-increment the pbar with 1."""
        if self.iterable is None:
            raise ValueError("Must give an iterable to be used in a loop.")
        for obj in self.iterable:
            yield obj
        self.update_with_increment_value(1)


def _chunk_write(chunk, local_file, progress):
    """Write a chunk to file and update the progress bar."""
    local_file.write(chunk)
    progress.update_with_increment_value(len(chunk))


def _get_ftp(url, temp_file_name, initial_size, file_size, verbose_bool):
    """Safely (resume a) download to a file from FTP."""
    # Adapted from: https://pypi.python.org/pypi/fileDownloader.py
    # but with changes

    parsed_url = urllib.parse.urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    server_path = parsed_url.path.replace(file_name, "")
    unquoted_server_path = urllib.parse.unquote(server_path)

    data = ftplib.FTP()
    if parsed_url.port is not None:
        data.connect(parsed_url.hostname, parsed_url.port)
    else:
        data.connect(parsed_url.hostname)
    data.login()
    if len(server_path) > 1:
        data.cwd(unquoted_server_path)
    data.sendcmd("TYPE I")
    data.sendcmd("REST " + str(initial_size))
    down_cmd = "RETR " + file_name
    assert file_size == data.size(file_name)
    progress = ProgressBar(file_size, initial_value=initial_size,
                           max_chars=40, spinner=True, mesg='file_sizes',
                           verbose_bool=verbose_bool)

    # Callback lambda function that will be passed the downloaded data
    # chunk and will write it to file and update the progress bar
    mode = 'ab' if initial_size > 0 else 'wb'
    with open(temp_file_name, mode) as local_file:
        def chunk_write(chunk):
            return _chunk_write(chunk, local_file, progress)
        data.retrbinary(down_cmd, chunk_write)
        data.close()
    sys.stdout.write('\n')
    sys.stdout.flush()


def _get_http(url, temp_file_name, initial_size, file_size, verbose_bool):
    """Safely (resume a) download to a file from http(s)."""
    # Actually do the reading
    req = urllib.request.Request(url)
    if initial_size > 0:
        req.headers['Range'] = 'bytes=%s-' % (initial_size,)
    try:
        response = urllib.request.urlopen(req)
    except Exception:
        # There is a problem that may be due to resuming, some
        # servers may not support the "Range" header. Switch
        # back to complete download method
        logger.info('Resuming download failed (server '
                    'rejected the request). Attempting to '
                    'restart downloading the entire file.')
        del req.headers['Range']
        response = urllib.request.urlopen(req)
    total_size = int(response.headers.get('Content-Length', '1').strip())
    if initial_size > 0 and file_size == total_size:
        logger.info('Resuming download failed (resume file size '
                    'mismatch). Attempting to restart downloading the '
                    'entire file.')
        initial_size = 0
    total_size += initial_size
    if total_size != file_size:
        raise RuntimeError('URL could not be parsed properly '
                           '(total size %s != file size %s)'
                           % (total_size, file_size))
    mode = 'ab' if initial_size > 0 else 'wb'
    progress = ProgressBar(total_size, initial_value=initial_size,
                           max_chars=40, spinner=True, mesg='file_sizes',
                           verbose_bool=verbose_bool)
    chunk_size = 8192  # 2 ** 13
    with open(temp_file_name, mode) as local_file:
        while True:
            t0 = time.time()
            chunk = response.read(chunk_size)
            dt = time.time() - t0
            if dt < 0.005:
                chunk_size *= 2
            elif dt > 0.1 and chunk_size > 8192:
                chunk_size = chunk_size // 2
            if not chunk:
                if verbose_bool:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                break
            local_file.write(chunk)
            progress.update_with_increment_value(len(chunk),
                                                 mesg='file_sizes')


def _fetch_file(url, file_name, print_destination=True, resume=True,
                hash_=None, timeout=10., verbose_bool=True):
    """Load requested file, downloading it if needed or requested.
    Parameters
    ----------
    url: string
        The url of file to be downloaded.
    file_name: string
        Name, along with the path, of where downloaded file will be saved.
    print_destination: bool, optional
        If true, destination of where file was saved will be printed after
        download finishes.
    resume: bool, optional
        If true, try to resume partially downloaded files.
    hash_ : str | None
        The hash of the file to check. If None, no checking is
        performed.
    timeout : float
        The URL open timeout.
    verbose_bool : bool
        If True, send messages/events that occur during file fetching
        to standard output using print().
        Default is True.
    """
    #md5 hash should be 32 characters (hex digits, i.e. 128 bits)
    if hash_ is not None and len(hash_) != 32:
        raise ValueError('Bad hash value given, should be a 32-character '
                         'string:\n%s' % (hash_,))
    temp_file_name = file_name + ".part"
    try:
        # Check file size and displaying it alongside the download url
        u = urllib.request.urlopen(url, timeout=timeout)
        u.close()
        # this is necessary to follow any redirects
        url = u.geturl()
        u = urllib.request.urlopen(url, timeout=timeout)
        try:
            file_size = int(u.headers.get('Content-Length', '1').strip())
        finally:
            u.close()
            del u
        print('Downloading %s (%s)' % (url, sizeof_fmt(file_size)))

        # Triage resume
        if not os.path.exists(temp_file_name):
            resume = False
        if resume:
            with open(temp_file_name, 'rb', buffering=0) as local_file:
                local_file.seek(0, 2)
                initial_size = local_file.tell()
            del local_file
        else:
            initial_size = 0
        # This should never happen if our functions work properly
        if initial_size > file_size:
            raise RuntimeError('Local file (%s) is larger than remote '
                               'file (%s), cannot resume download'
                               % (sizeof_fmt(initial_size),
                                  sizeof_fmt(file_size)))
        elif initial_size == file_size:
            # This should really only happen when a hash is wrong
            # during dev updating
            warn('Local file appears to be complete (file_size == '
                 'initial_size == %s)' % (file_size,))
        else:
            # Need to resume or start over
            scheme = urllib.parse.urlparse(url).scheme
            fun = _get_http if scheme in ('http', 'https') else _get_ftp
            fun(url, temp_file_name, initial_size, file_size, verbose_bool)

        # check md5sum
        if hash_ is not None:
            print('Verifying hash %s.' % (hash_,))
            md5 = md5sum(temp_file_name)
            if hash_ != md5:
                raise RuntimeError('Hash mismatch for downloaded file %s, '
                                   'expected %s but got %s'
                                   % (temp_file_name, hash_, md5))
        shutil.move(temp_file_name, file_name)
        if print_destination is True:
            print('File saved as %s.\n' % file_name)
    except Exception:
        print('Error while fetching file %s.'
              ' Dataset fetching aborted.' % url)
        raise


FORMATS = {
    'notmat': {
        'download_url': 'https://ndownloader.figshare.com/files/13993349',
        'readme': '',
        'file_name': 'cbin-notmat.tar.gz',
    },
    'koumura': {
        'download_url': 'https://ndownloader.figshare.com/files/13993352',
        'readme': '',
        'file_name': 'wav-koumura.tar.gz',
    }
}


def fetch(format, destination_path='.', remove_compressed_file=True):
    """fetches data from repositories

    Parameters
    ----------
    format : str
        name of birdsong annotation format. A small example dataset that is
        annotated with this format will be downloaded. See the "Examples"
        section below for an example of how to print the formats built in to
        crowsetta.
    destination_path : str
        Path where downloaded examples should be saved.
    remove_compressed_file : bool
        if True, remove tar.gz files after extracting.
        Default is True

    Returns
    -------
    None

    Examples
    --------

    """
    try:
        format_dict = FORMATS[format]
    except KeyError:
        raise KeyError('Currently there is no example dataset to download for '
                         f'{format}. To see the built-in formats, type:\n'
                         f'>>> crowsetta.formats()')
    destination_path = os.path.expanduser(destination_path)
    if not os.path.isdir(destination_path):
        raise NotADirectoryError('could not find destination_path: {}'
                                 .format(destination_path))

    file_name = format_dict['file_name']
    file_name = os.path.join(destination_path, file_name)

    if 'md5_hash' in format_dict:
        md5_hash = format_dict['md5_hash']
    else:
        md5_hash = None

    # helpers from MNE-Python that do actual downloading
    _fetch_file(url=format_dict['download_url'],
                file_name=file_name,
                hash_=md5_hash)

    if file_name.endswith('.tar.gz') or file_name.endswith('.zip'):
        print('extracting {}'.format(file_name))

        if file_name.endswith('.tar.gz'):
            with tarfile.open(file_name) as tar:
                tar.extractall(path=destination_path)

        elif file_name.endswith('.zip'):
            with ZipFile(file_name, 'r') as zipfile:
                zipfile.extractall(path=destination_path)

        if remove_compressed_file:
            os.remove(file_name)
