import pp, time

def doInParallel(getSizeP, total, data, numbers):
    ppservers = ("*",)
    job_server = pp.Server(ppservers=ppservers)
    start_time = time.time()
    p = int(round(total / 4))
    print "Starting download"
    for s in range(int(p)):
        connection = True
        while connection:
            job = job_server.submit(getSizeP, (total, data, numbers, p, int(s)), (), ("urllib2", "json" , "time"))
            total, data, numbers, connection = job()
    job_server.wait()
    job_server.destroy()
    return total, data
