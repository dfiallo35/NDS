from elements.elements import Element
from elements.map import *
from ia.planning_reacts import reaction_for_an_event

from queue import PriorityQueue
a = PriorityQueue()
import time as cp_time


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




class Simulate:
    def __init__(self, map: Map, initial_events: Pqueue):
        self.event_queue = initial_events
        self.map = map
    
    @property
    def en_dis(self):
        return self.map.en_dis_events
    
    @property
    def events(self):
        return self.map.events

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
                if event.is_enabled and self.events[event.name].is_enabled:
                    print(time, event)
                    t1=cp_time.time()
                    old_map = copy(self.map)
                    # for nation in self.map.nationdict.values():
                    #     print(event,nation.name,nation.get_nation_all_data())

                    t=cp_time.time()
                    print('time to copy the map',event.name,t-t1)

                    event.execute(self.map)
                    # for nation in self.map.nationdict.values():
                    #     print(event,nation.name,nation.get_nation_all_data())
                    t2=cp_time.time()
                    print('time to do the event',event.name,t2-t)
                    self.map.log.add(time, event, old_map, self.map)
                    t5=cp_time.time()
                    print('time to do the log',event.name,t5-t2)
                    self.generate_event(event, time)
                    t3=cp_time.time()
                    print('time to generate the next event',event.name,t3-t5)
                    self.decide(old_map,self.map, event, time)
                    t4=cp_time.time()
                    print('time to return the decisions',event.name,t4-t3)


    def generate_event(self, event: Event, time: int):
        '''
        Generate an event and add it to the queue
        :param event: the event to be generated
        :param time: the current time of the simulation
        '''
        if event.name in self.map.decision_eventdict:
            pass

        elif event.name in self.en_dis['enable']:
            self.map.eventdict[event.name].enabled = True
            
            self.event_queue.push((self.new_time(event, time), event))
            self.en_dis['enable'].remove(event.name)
        
        elif event.name in self.en_dis['disable']:
            self.map.eventdict[event.name].enabled = False
            self.en_dis['disable'].remove(event.name)
        
        elif event.is_enabled:
            self.event_queue.push((self.new_time(event, time), event))
        
        
    
    def new_time(self, event, time):
        nt= time + event.next()
        if nt == time:
            nt += 1
        return nt
    
    def decide(self,old_map:Map, map: Map, event: Event, time: int):
        '''
        Decisions of a nation given an event and the moment in which it occurs
        :param event: the event that occurred
        :param time: the time the event occurred
        '''

        if map.decision_eventdict.get(event.name):
            return
        t=cp_time.time()
        changes=old_map.compare(map)  
        t1=cp_time.time() 
        print("time_to compare",t1-t)
        decisions=self.get_events_from_decisions(reaction_for_an_event(old_map, map,changes,event))
        t2=cp_time.time() 
        print("time_to get decisions in decide",t2-t1)

        for nation in decisions.keys():
            nation_decs=self.get_time(time,decisions[nation],distribution="uniform")
            for time_dec in nation_decs:
                print("planning",time_dec[0],time_dec[1].name,nation)
                self.event_queue.push(time_dec)
        t3=cp_time.time() 
        print("time_to get decisions time and push in queue in decide",t3-t2)
        

    
    def get_time(self,initial_time,decisions,distribution="uniform",scale=10):
        """Get the time of the event and return a list of tuples with the time and the event""" 
        distribution=Distribution(distribution,distribution)        
        timed_decisions=[]
        for decision in decisions:
            initial_time = int(initial_time + distribution.rvs() * scale)
            timed_decisions.append((initial_time, decision))            
        return timed_decisions

    def get_events_from_decisions(self,decisions):
        """Get the events from the decisions"""        
        events={}        
        for nation in decisions.keys():
            events[nation]=[]
            for decision in decisions[nation]:
                # decision.event.enabled=True
                # event=decision.event.get_event(nation)
                events[nation].append(decision.event.get_event(nation))
        return events

















