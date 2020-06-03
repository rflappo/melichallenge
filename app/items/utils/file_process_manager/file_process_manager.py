from itertools import chain
from multiprocessing import Process, Manager, cpu_count

from app.data import db
from sqlalchemy.orm import sessionmaker
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

    @staticmethod
    def _get_new_db_session():
        # from app import app
        # Session = sessionmaker(bind=db.get_engine(app))
        Session = sessionmaker(bind=db.get_engine())

        return Session()

    def _queued_work(self):

        while True:
            line = self.args_queue.get()

            if line:
                db_session = ItemsFileProcessManager._get_new_db_session()

                line_process = LineProcessor(line, db_session)
                line_process.process_line()

                db_session.close()
            else:
                break

    def run(self):
        iters = chain(self.data_file, (None,)*self.num_workers)

        for line in iters:
            self.args_queue.put(line)

        for p in self.pool:
            p.join()
