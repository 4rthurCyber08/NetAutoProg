import concurrent.futures
import multiprocessing
import time

def do_something(seconds, sample):
    print(f'Sleeping {seconds} seconds(s)...')
    time.sleep(seconds)
    # print (f'Done Sleeping...{seconds}')
    return f'Done Sleeping...{seconds} and {sample}'

if __name__ == '__main__':
    start = time.perf_counter()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        secs2 = [True, False, 1, 0, 'Hi']
        # submit method
        # results = [executor.submit(do_something, sec) for sec in secs]
        
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())
        
        # map method
        results = executor.map(do_something, secs, secs2)
        for result in results:
            print(result)

    # multiprocessing
    # secs2 = [5, 4, 3, 2, 1]
    # procs = []
    # for i in secs2:
    #     proc1 = multiprocessing.Process(target=do_something, args=[i])
    #     procs.append(proc1)
    #     proc1.start()
    
    # for i in procs:
    #     i.join()
        
        
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)}')
    
    
