import pp, time

def doInParallel(getSizeP, total, data, numbers):
    ppservers = ("*",)
    # # # if len(sys.argv) > 1:
    # # # ncpus = int(sys.argv[1])
    # # # # Creates jobserver with ncpus workers
    # # # job_server = pp.Server(2, ppservers=ppservers)
    # # # else:
    # Creates jobserver with automatically detected number of workers
    # job_server = pp.Server(ppservers=ppservers)
    job_server = pp.Server(ppservers=ppservers)
    start_time = time.time()
    # # # # job1 = job_server.submit(proof, (1,50000), (), ())
    # # # # job2 = job_server.submit(proof, (1,40000), (), ())
    # # # # jobs = [job_server.submit(getSizeP,(total,data,numbers,p,int(s)), (), ("urllib2","json")) for s in range(int(p))]
    # # # # for job in jobs:
    # # # # print "Worker number ", s , job()
    # # # # total,data,numbers = job()
    p = int(round(total / 4))
    print "Starting download"
    for s in range(int(p)):
        connection = True
        while connection:
            job = job_server.submit(getSizeP, (total, data, numbers, p, int(s)), (), ("urllib2", "json" , "time"))
            total, data, numbers, connection = job()
    job_server.wait()
#    print "Time elapsed: ", time.time() - start_time, "s"
#    job_server.print_stats()
    job_server.destroy()
    return total, data
