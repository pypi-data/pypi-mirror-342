import contextlib
import logging
import multiprocessing

log = logging.getLogger(__name__)


class Parallel:
    def run(self):
        msg = "Please implement the method `run`."
        raise NotImplementedError(msg)

    @classmethod
    def start(cls, tasks):
        multiprocessing.set_start_method("spawn")
        with multiprocessing.Manager() as m:
            queue = m.Queue()
            [queue.put(task, block=False) for task in tasks]
            cls.process(queue=queue)
            log.info("Done!")

    @classmethod
    def process(cls, queue):
        """
        Run type generation using multiprocessing lib
        """
        num_procs = multiprocessing.cpu_count()
        with multiprocessing.Pool(num_procs) as p:
            p.map(cls.run_parallel, [queue] * num_procs)

    @staticmethod
    def run_parallel(queue):
        while not queue.empty():
            factory = queue.get()
            factory.run()
            with contextlib.suppress(NotImplementedError):
                queue_size = queue.qsize()
                if queue_size and queue_size % 500 == 0:
                    log.info("%s items remaining.", queue_size)
