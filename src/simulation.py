from events.event import *
from elements.elements import *
from queue import PriorityQueue

class Queue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.events= dict()
        self.event_index= 0
        

    def push(self, element: tuple[Time,Event]) -> None:
        '''
        Push an event and its time in the queue
        :param time: the time the event should occur
        :param event: the event to be executed
        '''
        self.events[self.event_index] = element[1]
        self.queue.put((element[0], self.event_index))
        self.event_index += 1
    
    def get(self) -> tuple[int, Event]:
        '''
        Get the next event in the queue
        :return: the next event in the queue
        '''
        if self.empty():
            return None
        element= self.queue.get()
        return (element[0], self.events[element[1]])
    
    def look(self) -> tuple[int, Event]:
        '''
        Look at the next event in the queue and its time without removing it
        :return: the next event in the queue and its time
        '''
        if self.empty():
            return None
        element= self.get()
        self.push(element)
        return element
    
    def pop(self) -> list[tuple[int, Event]]:
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
    
    def empty(self) -> bool:
        return self.queue.empty()
    
    def len(self) -> int:
        return len(self.queue.queue)
    
    def __len__(self) -> int:
        return len(self.queue.queue)
    
    def __str__(self) -> str:
        return '[' + ', '.join(['('+ str(self.queue.queue[i][0]) + ', ' + str(self.events[self.queue.queue[i][1]]) + ')' for i in range(self.len())])





#todo: events add events to the queue
#todo: add decisions to simulation
class Simulate:
    def __init__(self):
        self.event_queue = Queue()
        self.basic_events()

    def simulate(self, time: Time):
        '''
        Run the simulation for a certain amount of time
        :param time: the time the simulation should run
        '''
        while not self.event_queue.empty():
            if self.event_queue.look()[0] > time:
                break

            for time, event in self.event_queue.pop():
                event.execute()
                self.generate_event(event, time)
                self.decide(event, time)

                

    def basic_events(self):
        '''
        Add the basic events to the queue
        Basic events are the events that are always in the simulations
        '''
        ...

    def generate_event(self, event: Event, time: Time):
        '''
        Generate an event and add it to the queue
        :param event: the event to be generated
        :param time: the time the event should occur
        '''
        if event.is_enabled:
            self.event_queue.push(time + event.next(), event)
    
    def decide(self, event: Event, time: Time):
        '''
        Decisions of a nation given an event and the moment in which it occurs
        :param event: the event that occurred
        :param time: the time the event occurred
        '''
        ...
    

















