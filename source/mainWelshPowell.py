# currentBlock = 0
# Find the degree of each vertex
# Sort the vertices in order of descending degrees.
# while the queue is not empty:
    # set top vertex to currentBlock
    # remove top vertex from the queue
    # for each course in the queue:
    #   if not concurrent to a course with timeBlock = currentBlock, set it to currentBlock
    # currentBlock += 1

# https://www.geeksforgeeks.org/welsh-powell-graph-colouring-algorithm/

#from queue import Queue
import heapq, itertools
#priority queue implementation: https://docs.python.org/3/library/heapq.html
Q = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of vertices to entries
REMOVED = '<removed-vertex>'      # placeholder for a removed vertex
counter = itertools.count()     # unique sequence count

#Note: In this case distance = len(concurrents)
def add_vertex(vertex, distance=0):
    'Add a new vertex or update the priority of an existing vertex'
    if vertex in entry_finder:
        remove_vertex(vertex)
    count = next(counter)
    entry = [distance, count, vertex]
    entry_finder[vertex] = entry
    heapq.heappush(Q, entry)

def remove_vertex(vertex):
    'Mark an existing vertex as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(vertex)
    entry[-1] = REMOVED

def pop_vertex():
    'Remove and return the lowest priority vertex. Raise KeyError if empty.'
    while Q:
        distance, count, vertex = heapq.heappop(Q)
        if vertex is not REMOVED:
            del entry_finder[vertex]
            return vertex
    return -1   #  to indicate removal has occured for this vertex

timeBlocks = {-1:"Null",0:"M1250", 1:"T1250", 2:"M1145", 3:"T1145", 4:"M1025", 5:"T930", 6:"M905", 7:"M155", 8:"T220", 9:"M315", 10:"T350", 11:"M435", 12:"T800", 13:"M800"}

class Graph:
    def __init__(self):
        self.courses = []
    def __str__(self):
        for c in self.courses:
            print(c)
        return ""
    def addCourse(self, course):
        self.courses.append(course)
    def sort(self):
        #sort graph by len(i.concurrents)
        self.courses.sort(key=lambda x: len(x.concurrents), reverse=True)
       
    def welshPowell(self):
        #each i corresponds to a list index of a course
        for i in range(len(self.courses)):
            add_vertex(i,-1*len(self.courses[i].concurrents))
       
        currentBlock = 0
        while Q:
            top = pop_vertex()
            if top != -1: #top is going to be an index for courses list
                currentBlock += 1
                self.courses[top].timeBlock = currentBlock
            for c in Q: #c is an entry in Q, c[2] is the vertex
                flag = False    #flag for if a concurrent.timeblock == currentBlock
                if c[2] != REMOVED:
                    for concurrent in self.courses[c[2]].concurrents:
                        if concurrent.timeBlock == currentBlock:
                            flag = True #currentblock found in concurrents
                            break
                    if flag == False:   # no concurrent with currentBlock was found
                        self.courses[c[2]].timeBlock = currentBlock
                        remove_vertex(c[2])
        return(currentBlock)               
         
class Course:
    def __init__(self, ID,name,prof):
        self.ID = ID
        self.name = name
        self.timeBlock = -1
        self.concurrents = []
        self.prof = prof
    def __str__(self):
        return "Course "+self.ID+" "+self.name+", taught by "+self.prof+" is scheduled for time block "+timeBlocks[self.timeBlock]#+" and has "+str(len(self.concurrents))+" concurrent courses: "+str(self.concurrents)
    def __repr__(self):
        return self.ID

with open('./GraphColoringAlgorithmFinal/classInfo.txt','r') as classList, open('./GraphColoringAlgorithmFinal/input.txt','r') as concurrentClasses:
    numClasses = int(concurrentClasses.readline())
    algoGraph = Graph()
    
    #add classes from input.txt to the graph
    for c in range(numClasses):
        current = classList.readline().split()
        algoGraph.addCourse(Course(current[0],current[1],current[2]))
    
    # add connections between courses commonly taken in the same semester
    concurrentClasses.readline()
    i = 0
    while True:
        c1,c2 = map(int,concurrentClasses.readline().split())
        if c1 != 0 and c2 != 0:
            i+= 1
            algoGraph.courses[c1-1].concurrents.append(algoGraph.courses[c2-1])
            algoGraph.courses[c2-1].concurrents.append(algoGraph.courses[c1-1])

        else:
            break
    
    #add connections between courses taught by the same prof
    for c1 in range(numClasses):
        for c2 in range(numClasses):
            if c1 != c2 and algoGraph.courses[c1].prof == algoGraph.courses[c2].prof and algoGraph.courses[c1] not in algoGraph.courses[c2].concurrents:
                algoGraph.courses[c1].concurrents.append(algoGraph.courses[c2])
                algoGraph.courses[c2].concurrents.append(algoGraph.courses[c1])
    
    numBlocks = algoGraph.welshPowell()
    print(algoGraph)
    print("Welsh-Powell was able to schedule all courses in",numBlocks,"time blocks!")