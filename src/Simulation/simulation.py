from event import *
from queue import PriorityQueue

class Queue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.events= dict()
        self.event_index= 0
        

    def push(self, time: int, event: Event):
        '''
        Push an event and its time in the queue
        :param time: the time the event should occur
        :param event: the event to be executed
        '''
        self.events[self.event_index] = event
        self.queue.put((time, self.event_index))
        self.event_index += 1
    
    def get(self):
        '''
        Get the next event in the queue
        :return: the next event in the queue
        '''
        if self.empty():
            return None
        element= self.queue.get()
        return (element[0], self.events[element[1]])
    
    def look(self):
        '''
        Look at the next event in the queue and its time without removing it
        :return: the next event in the queue and its time
        '''
        if self.empty():
            return None
        element= self.get()
        self.push(element[0], element[1])
        return element
    
    def pop(self):
        '''
        Get all the events in the queue with the same time
        :return: a list of all the events in the queue with the same time
        '''
        if self.empty():
            return None
        element= self.get()
        elemets= [element]
        while self.look() and self.look()[0] == element[0]:
            elemets.append(self.get())
        return elemets
    
    def empty(self):
        return self.queue.empty()
    
    def len(self):
        return len(self.queue.queue)
    
    def __len__(self):
        return len(self.queue.queue)
    
    def __str__(self):
        return '[' + ', '.join(['('+ str(self.queue.queue[i][0]) + ', ' + str(self.events[self.queue.queue[i][1]]) + ')' for i in range(self.len())])


