from multipipeline import Multipipeline

mp = Multipipeline()

args_data = [_ for _ in range(1000)]
master_list = []
print('args_data', args_data)
print(len(args_data))

def range_worker(arg_data):
    print(arg_data)
    path_data, output_queue = arg_data
    print('path_data',path_data)
    print('output_queue',output_queue)
    for _arg in path_data:
        mp.put_queue_process(output_queue, _arg)

def append_worker(data):
    master_list.append(data)
    print('master_list len',len(master_list))

def preprocess_worker(data):
    return data*2


def simple_queue_test_arch():
    queue1 = mp.make_queue('path_worker__to__pross_test_worker', 50)
    queue2 = mp.make_queue('pross_test_worker__to__append_worker', 50)
    path_process = mp.make_process(range_worker, (args_data, queue1), input_queue=None,
                                        out_put_queue=None, process_num=1, type='func')
    pross_process = mp.make_process(preprocess_worker, None, input_queue=queue1,
                                         out_put_queue=queue2, process_num=10, type='roop')
    data_process = mp.make_process(append_worker, None, input_queue=queue2,
                                        out_put_queue=None, process_num=1, type='roop')
    
    mp.run_process(path_process)
    mp.run_process(pross_process)
    mp.run_process(data_process)

    mp.end_process(path_process)
    mp.end_process(pross_process)
    mp.end_process(data_process)




if __name__ == "__main__":
    simple_queue_test_arch()