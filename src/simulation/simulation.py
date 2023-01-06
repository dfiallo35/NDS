
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from elements.elements import Element
from elements.map import *
from ia.planning_reacts import reaction_for_an_event

from queue import PriorityQueue
a = PriorityQueue()

class Pqueue:
    def __init__(self, events: list[Event]= []):
        self.queue = PriorityQueue()
        self.events= dict()
        self.event_index= 0
        
        for arg in events:
            self.push((0, arg))
    
    @property
    def event_list(self):
        return list(self.events.values())

    def push(self, element: tuple[int,Event]) -> None:
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





#todo: events add events to the queue(param enent_queue in execute or return events in list)

#todo: add decisions to simulation
#todo: time in Time not int

#todo: decide without event

#check: add and disable events
class Simulate:
    def __init__(self, map: Map, initial_events: Pqueue):
        self.event_queue = initial_events
        self.map = map

    def simulate(self, end_time: int) -> None:
        '''
        Run the simulation for a certain amount of time
        :param time: the time the simulation should run
        '''
        while not self.event_queue.empty():
            if self.event_queue.look()[0] > end_time:
                print('break in', end_time, 'next', self.event_queue.look()[0])
                break

            for time, event in self.event_queue.pop():
                if event.is_enabled and self.map.eventdict[event.name].is_enabled:
                    print(time, event)

                    #execute the event and return a dictionary
                    #the eventdict is a dictionary with: {'enable': <list of events to be added to the queue>, 'disable': <list of events to be disabled>}
                    
                    old_map= copy(self.map)
                    eventdict: dict= event.execute(self.map)

                    #todo: log of changes
                    old_map.compare(self.map)
                    
                    if eventdict and eventdict.get('enable'):
                        self.enable_events(time, eventdict['enable'])
                    if eventdict and eventdict.get('disable'):
                        self.disable_events(eventdict['disable'])
                    
                    #generate the next event
                    self.generate_event(event, time)

                    #the nations make decisions based on the event and the map
                    self.decide(self.map, event, time)


    def generate_event(self, event: Event, time: int):
        '''
        Generate an event and add it to the queue
        :param event: the event to be generated
        :param time: the current time of the simulation
        '''
        if event.is_enabled:
            self.event_queue.push((time + event.next(), event))
    
    def enable_events(self,time: int, events: list[str]):
        '''
        Add a list of events to the queue given from the current event
        :param events: the list of events to be added
        :param time: the current time of the simulation
        '''
        for event in [self.map.eventdict[ev] for ev in events]:
            event.enabled= True
            self.generate_event(event, time)
    
    def disable_events(self, events: list[str]):
        '''
        Disable an event
        :param event: the event to be disabled
        '''
        for event in [self.map.eventdict[ev] for ev in events]:
            event.enabled= False
    
    def decide(self, map: Map, event: Event, time: int):
        '''
        Decisions of a nation given an event and the moment in which it occurs
        :param event: the event that occurred
        :param time: the time the event occurred
        '''
        new_map=copy(map)
        event.execute(new_map)
        changes=map.compare(new_map)        
        decisions=self.get_evets_from_decisions(reaction_for_an_event(map, new_map,changes))
        for nation in decisions.keys():
            timed_decisions=self.get_time(time,decisions[nation],distribution="uniform")
            for time_dec in timed_decisions:
                self.event_queue.push(time_dec)
        # return decisions

    
    def get_time(initial_time,decisions,distribution="uniform",scale=10):
        """Get the time of the event and return a list of tuples with the time and the event""" 
        distribution=Distribution(distribution,distribution)
        timed_decisions=[]
        for decision in decisions:
            initial_time=initial_time + distribution.rvs*scale
            timed_decisions.push((initial_time, decision))
        return timed_decisions
            
    def get_evets_from_decisions(decisions):
        """Get the events from the decisions"""
        events=[]
        for decision in decisions:
            events.append(Event(decision.name,None,decision.Category,decision.effect))
        return events

















