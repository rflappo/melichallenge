import os
from itertools import chain
from configparser import ConfigParser
from multiprocessing import Process, Manager, cpu_count

from app.items.utils.file_process_manager.line_processor import LineProcessor


class FileParserConfig:
    def __init__(self):
        config = ConfigParser()
        config_file = os.path.join(os.getcwd(), 'parserconfig.ini')
        config.read(config_file)

        self.settings = {}
        if 'FILE' in config.sections():
            self.settings = config['FILE']

    def file_with_headers(self):
        if 'HEADERS_LINE' in self.settings.keys():
            return self.settings['HEADERS_LINE'].lower() == 'true'
        return False

    def get_encoding(self):
        if 'ENCODING' in self.settings.keys():
            return self.settings['ENCODING'].lower()
        return 'utf-8'

    def get_allowed_extension(self):
        if 'EXTENSION' in self.settings.keys():
            return self.settings['EXTENSION'].lower()
        return 'text'


class ExtensionError(Exception):
    ''' Raised when the uploaded file is not of the type we spected '''


class ItemsFileProcessManager():
    def __init__(self, data_file):
        self.headers = None
        self.data_file = data_file

        self.config = FileParserConfig()
        if self.config.file_with_headers():
            self.headers = next(iter(self.data_file)).decode(self.config.get_encoding())
        self._check_file_extension()

        self.num_workers = cpu_count()
        self.manager = Manager()
        self.args_queue = self.manager.Queue(self.num_workers)
        self.pool = list()

    def _check_file_extension(self):
        allowed_ext = self.config.get_allowed_extension()

        splitted = self.data_file.filename.split('.')
        file_ext = splitted[-1] if len(splitted) > 1 else None

        if file_ext is None or allowed_ext != file_ext:
            raise ExtensionError(file_ext)

    def _queued_work(self):
        while True:
            line = self.args_queue.get()

            if line:
                line_process = LineProcessor(
                    line,
                    encoding=self.config.get_encoding(),
                    header_line=self.headers
                )
                line_process.process_line()

            else:
                break
    
    def _start_empty_processes(self):
        for _ in range(self.num_workers):
            p = Process(target=self._queued_work)
            p.start()
            self.pool.append(p)
    
    def _seed_processes(self):
        iters = chain(self.data_file, (None,)*self.num_workers)

        for line in iters:
            self.args_queue.put(line)

        for p in self.pool:
            p.join()

    def run(self):
        self._start_empty_processes()
        self._seed_processes()
