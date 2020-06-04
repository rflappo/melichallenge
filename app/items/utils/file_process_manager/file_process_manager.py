from itertools import chain
from multiprocessing import Process, Manager, cpu_count

from app.items.utils.file_process_manager.line_processor import LineProcessor


class ItemsFileProcessManager():
    def __init__(self, data_file):

        self.data_file = data_file

        self.num_workers = cpu_count()
        self.manager = Manager()
        self.args_queue = self.manager.Queue(self.num_workers)

        self.pool = list()

        for _ in range(self.num_workers):
            p = Process(target=self._queued_work)
            p.start()
            self.pool.append(p)

    def _queued_work(self):

        while True:
            line = self.args_queue.get()

            if line:
                line_process = LineProcessor(line)
                line_process.process_line()

            else:
                break

    def run(self):
        iters = chain(self.data_file, (None,)*self.num_workers)

        for line in iters:
            self.args_queue.put(line)

        for p in self.pool:
            p.join()
