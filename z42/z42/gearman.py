#!/usr/bin/env python
#coding:utf-8

import socket
import os
from msgpack import dumps, loads
import traceback

class GearmanClient(object):
    def __init__(self, gearman):
        self.gearman = gearman

    def client(self, name, background=True):
        def _(*args, **kwds):
            return self.gearman.submit_job(
                name ,
                dumps((args, kwds)) ,
                background=background
            )
        if background:
            _client = _
        else:
            def _client(*args, **kwds):
                request = _(*args, **kwds)
                if request.complete:
                    return loads(request.result)
                else:
                    raise request.state
        
        return _client

class GearmanServer(object):
    def __init__(self, gearman):
        self.gearman = gearman

    def _rpc(self, func, background):
        namespace = func.__module__.rsplit('.',1)[-1]
        name = '%s.%s'%(namespace, func.func_name)

        if background:
            def _server(gearman_worker, gearman_job):
                args , kwds = loads(gearman_job.data)
                try:
                    func(*args, **kwds)
                except:
                    traceback.print_exc()
                return ''
        else:
            def _server(gearman_worker, gearman_job):
                args , kwds = loads(gearman_job.data)
                try:
                    r = func(*args, **kwds)
                except:
                    traceback.print_exc()
                return dumps(r) 

        self.gearman.register_task( name, _server )


    def sync(self, func):
        return self._rpc(func, False)

    def async(self, func):
        return self._rpc(func, True)


#gearman.set_client_id("%s.%s"%(socket.gethostname(),os.getpid()))
#if job_request.complete:
#    print 'Job %s finished!  Result: %s - %s' % (job_request.job.unique, job_request.state, job_request.result)
#elif job_request.timed_out:
#    print 'Job %s timed out!' % job_request.unique
#elif job_request.state == JOB_UNKNOWN:
#print 'Job %s connection failed!' % job_request.unique
#return _client 



if __name__ == '__main__':

    import time
    import gearman as _gearman

    from z42.web.rendermail import rendermail
    rendermail = gearman.async(rendermail)


    import rendermail
    gearman.run()

    @gearman.async
    def _():
        time.sleep(10)
        return abc*2

    GM_WORKER = _gearman.GearmanWorker(['localhost:4730'])
    gearman = Gearman(GM_WORKER, 'Mail')


    print test('1z')
    GM_WORKER.work()

#    

    #print "%s.%s"%(socket.gethostname(),os.getpid())


