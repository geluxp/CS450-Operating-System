# MLFQ scheduler implementation
# Some of codes and structures are in reference to the rr.py
#Kun Mei A20291908 Main Campus
from __future__ import print_function
from collections import deque
    
class MLFQScheduler:
    def __init__(self, quanta):
        self.quanta = quanta   # get the values of inputing quanta
        self.ready_queue = deque() # internal wait queue
        self.queue_lengths = []
    # we dont need  self.   = dict() since we will not output those values
        self.switch_cnts = dict() # Used to count the switches between queues and ready to output.
        self.current_queue_num = dict() #Used to trace the number of the current queue.
        self.job_quantum_expired_flag = dict()
        self.most_recent_hop_jid = []#Used to trace the most recent three jobs that have been swapped
        for i in xrange(len(quanta)): 
            self.ready_queue.append(deque())
            self.queue_lengths.append(list())
        current_jid = None  #Initiation

    # called when a job is first created -- the job is assumed
    # to be ready at this point (note: job_ready will not be called
    # for a job's first CPU burst)
    def job_created(self, jid):
        self.ready_queue[0].append(jid)
        self.switch_cnts[jid] = 0
        self.current_queue_num[jid] = 0
        self.job_quantum_expired_flag[jid] = 0

    # called when a job becomes ready after an I/O burst completes
    def job_ready(self, jid):
        temp = self.current_queue_num[jid]
        for i in xrange(len(self.ready_queue)):
            self.queue_lengths[i].append(len(self.ready_queue[i]))
        self.ready_queue[temp].append(jid)
        self.job_quantum_expired_flag[jid] = 0

    # called when a job's current CPU burst runs to the end of its
    # allotted time quantum without completing -- the job is
    # still in the ready state
    def job_quantum_expired(self, jid): 
        temp = self.current_queue_num[jid]
        for i in xrange(len(self.ready_queue)):  
            self.queue_lengths[i].append(len(self.ready_queue[i]))
            #check if the job is among the most recent three jobs that have been swapped
        if temp < (len(self.ready_queue) - 1) and not(jid in self.most_recent_hop_jid = [])           
            self.current_queue_num[jid] += 1
            self.ready_queue[temp+1].append(jid)
            self.switch_cnts[jid] += 1
            self.most_recent_hop_jid.insert(0, jid)
            if len(self.most_recent_hop_jid) > 3:
                self.most_recent_hop_jid.pop()
        else:
            self.ready_queue[temp].append(jid)
        self.job_quantum_expired_flag[jid] = 1
    
    # called when a job is preempted mid-quantum due to our
    # returning True to `needs_resched` -- the job is still in
    # the ready state
    def job_preempted(self, jid):
        for i in xrange(len(self.ready_queue)):
            self.queue_lengths[i].append(len(self.ready_queue[i]))
        self.ready_queue[self.current_queue_num[jid]].appendleft(jid)

    # called after a job completes its final CPU burst -- the job
    # will never become ready again
    def job_terminated(self, jid):
        pass

    # called when a job completes its CPU burst within the current
    # time quantum and has moved into its I/O burst -- the job is
    # currently blocked
    def job_blocked(self, jid):
        if self.job_quantum_expired_flag[jid] != 1 and self.current_queue_num[jid] > 0 and not(jid in self.most_recent_hop_jid):
            self.current_queue_num[jid] -= 1
            self.switch_cnts[jid] += 1
            self.most_recent_hop_jid.insert(0, jid)
            if len(self.most_recent_hop_jid) > 3:
                self.most_recent_hop_jid.pop()

    # called by the simulator after new jobs have been made ready.
    # we should return True here if we have a more deserving job and
    # want the current job to be preempted; otherwise return False
    def needs_resched(self):
        if self.current_jid == -1:
            return False
        for i in xrange(self.current_queue_num[self.current_jid]):
            if self.ready_queue[i]:
                return True
        return False

    # return a two-tuple containing the job ID and time quantum for
    # the next job to be scheduled; if there is no ready job,
    # return (None, 0)
    def next_job_and_quantum(self):
        for i in xrange(len(self.ready_queue)):
            if self.ready_queue[i]:
                self.current_jid = self.ready_queue[i].popleft()
                return (self.current_jid, self.quanta[i])
        self.current_jid = None
        return (None, 0)

    # called by the simulator after all jobs have terminated -- we
    # should at this point compute and print out well-formatted
    # scheduler statistics
    def print_report(self):
        print()
        print('  JID | # Switches')
        print('------------------')
        for jid in sorted(self.switch_cnts.keys()):
            print('{:5d} | {:10d}'.format(jid, self.switch_cnts[jid]))
        print()
        print('Queue | Avg length | Max Length')
        print('-------------------------------')
        for i in xrange(len(self.ready_queue)):
              avg_q_len = sum(self.queue_lengths[i], 0.0) / len(self.queue_lengths[i])
                 
              print('{:5d} | {:.2f}       |  {:.2f} '.format(i, avg_q_len, max(self.queue_lengths[i])))
              print()
