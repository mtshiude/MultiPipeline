from multiprocessing import Value,Process, Lock, Queue
import time

class Queue_template:
    def __init__(self, name, queue_size):
        self.queue_name = name
        self.queue_size = queue_size
        self.create_time = time.time()

    def define_queue(self,queue_size):
        return Queue(maxsize=queue_size)

class Queue_manager(Queue_template):
    def __init__(self):
        self.lock = Lock()
        self.queue_stack = {}
        self.kill_queue_num = 10

    def make_queue(self, name, size):
        _queue = self.define_queue(size)
        use_num = 0
        self.queue_stack[name] = [size,time.time(),use_num]
        return _queue

    def get_queue_process(self,target_queue):
        get_req = True
        while get_req:
            try:
                self.lock.acquire()
                if not target_queue.empty():
                    data = target_queue.get(block=True)
                    return data
            finally:
                self.lock.release()
                time.sleep(0.1)

    def put_queue_process(self, target_queue, data):
        put_req = True
        while put_req:
            try:
                self.lock.acquire()
                if not target_queue.full():
                    target_queue.put(data, block=True)
                    put_req = False
            finally:
                self.lock.release()
                time.sleep(0.1)

class Multi_pipeline(Queue_manager):
    def __init__(self):
        super().__init__()
        self.max_process_life = 200
        self.process_stack = {}

    def manager_info(self):
        print('manager info---------')
        print('processes---------')
        print(self.process_stack)

    def queue_splitter(self, in_queue, out_queue1, out_queue2):
        process_num = 1
        func_args = (in_queue, out_queue1, out_queue2)
        def splitter_core(in_queue, out_queue1, out_queue2):
            while True:
                input_data = self.get_queue_process(in_queue)
                self.put_queue_process(out_queue1, input_data)
                self.put_queue_process(out_queue2, input_data)

        _process_stack = [Process(target=splitter_core, args=func_args) for _ in range(process_num)]
        return _process_stack

    def roop_worker(self,my_func, func_args, input_queue, output_queue,kill_sw=False):
        print('roop_worker', my_func, func_args, input_queue, output_queue)
        while not kill_sw:
            if (input_queue and output_queue):#middle mode
                input_data = self.get_queue_process(input_queue)
                if None not in func_args:
                    ret_data = my_func(input_data, func_args)
                else:
                    ret_data = my_func(input_data)
                self.put_queue_process(output_queue,ret_data)

            elif input_queue:#tail mode
                input_data = self.get_queue_process(input_queue)
                if None not in func_args :
                    ret_data = my_func(input_data, func_args)
                else:
                    ret_data = my_func(input_data)

            elif output_queue:#head mode
                if None not in func_args:
                    ret_data = my_func(func_args)
                else:
                    ret_data = my_func()
                self.put_queue_process(output_queue, ret_data)

    def make_process(self, func, *func_args, input_queue=None, out_put_queue=None, process_num=1, type='roop'):
        #3type mode
        #head mode
        #[process] -> [queue]

        #hidden mode
        #[queue] -> [process] -> [queue]

        # tail mode
        # [queue] -> [process]

        target_args = (func, func_args, input_queue, out_put_queue)
        _process_stack = []
        print('func_args',func_args)
        if type == 'roop':
            _process_stack = [Process(target=self.roop_worker,args=target_args) for _ in range(process_num)]
        elif type == 'func':
            _process_stack = [Process(target=func, args=func_args) for _ in range(process_num)]
        else:
            print('bat process type->',type)

        return _process_stack

    def run_process(self,process_stack):
        for _ in process_stack:
            print('run_process->',_)
            _.start()

    def end_process(self,process_stack):
        for _ in process_stack:
            _.join()

