from events.event import *
from elements.elements import *
from elements.elements import *
from elements.map import Map
from queue import PriorityQueue

class Queue:
    def __init__(self, *args):
        self.queue = PriorityQueue()
        self.events= dict()
        self.event_index= 0
        
        for arg in args:
            self.push((0, arg))
        

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
#todo: time in Time not int
class Simulate:
    def __init__(self, map: Map, initial_events: Queue):
        self.event_queue = initial_events
        self.map = map

    def simulate(self, end_time: int):
        '''
        Run the simulation for a certain amount of time
        :param time: the time the simulation should run
        '''
        while not self.event_queue.empty():
            if self.event_queue.look()[0] > end_time:
                print('break in ', end_time, 'next ', self.event_queue.look()[0])
                break

            for time, event in self.event_queue.pop():
                print(time, event)
                event.execute(self.map)
                self.generate_event(event, time)
                self.decide(map, event, time)


    def generate_event(self, event: Event, time: int):
        '''
        Generate an event and add it to the queue
        :param event: the event to be generated
        :param time: the time the event should occur
        '''
        if event.is_enabled:
            self.event_queue.push((time + event.next(), event))
    
    def decide(self, map: Map, event: Event, time: int):
        '''
        Decisions of a nation given an event and the moment in which it occurs
        :param event: the event that occurred
        :param time: the time the event occurred
        '''
        ...
    

















