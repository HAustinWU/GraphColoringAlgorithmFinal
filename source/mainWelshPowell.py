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
# REMOVED = 1     # placeholder for a removed vertex
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
    #return -1 to indicate removal has occured for this vertex
    return -1

timeBlocks = {0:"8:00AM MWF",1:"9:05AM MWF"}

class Graph:
    def __init__(self):
        self.courses = []
    def __str__(self):
        for course in self.courses:
            print(course)
        return ""
    def addCourse(self, course):
        self.courses.append(course)
    
    #def sort(self):
        #sort graph by len(i.concurrents)
        #self.courses.sort(key=lambda x: len(x.concurrents), reverse=True)
        
    def welshPowell(self):
        # courseQueue = []
        # for c in self.courses:
        #     courseQueue.append(c)
        #each i corresponds to a list index of a course
        for i in range(len(self.courses)):
            add_vertex(i,-1*len(self.courses[i].concurrents))
        
        currentBlock = 0
        while Q:
            top = pop_vertex() #top is going to be an index for courses list
            self.courses[top].timeBlock = currentBlock
            #newList.append(top)
            for c in Q: #c is an entry in Q, c[2] is the vertex
                flag = False    #flag for if a concurrent.timeblock == currentBlock
                if c[2] != REMOVED:
                    for concurrent in self.courses[c[2]].concurrents:
                        if concurrent.timeBlock == currentBlock:
                            flag = True #currentblock found in concurrents
                            break
                    if flag == False:   # no concurrent with currentBlock was found
                        self.courses[c[2]].timeBlock = currentBlock
                        #newList.append(course)
                        remove_vertex(c[2])
            currentBlock += 1
        #self.courses = newList                
         
class Course:
    def __init__(self, ID):
        self.ID = ID
        self.name = "Whitworth Course"
        self.timeBlock = -1
        self.concurrents = []
    def __str__(self):
        return "Course "+self.ID+" is slated for time block "+str(self.timeBlock)+" and has "+str(len(self.concurrents))+" concurrent courses: "+str(self.concurrents)
    def __repr__(self):
        return self.ID

A = Course("A")
B = Course("B")
C = Course("C")
D = Course("D")
E = Course("E")
F = Course("F")
G = Course("G")
H = Course("H")
I = Course("I")
J = Course("J")

H.concurrents.append(E)
H.concurrents.append(I)
H.concurrents.append(J)
H.concurrents.append(G)

E.concurrents.append(D)
E.concurrents.append(F)
E.concurrents.append(H)

C.concurrents.append(A)
C.concurrents.append(B)
C.concurrents.append(D)

I.concurrents.append(J)
I.concurrents.append(H)

J.concurrents.append(I)
J.concurrents.append(H)

D.concurrents.append(E)
D.concurrents.append(C)

F.concurrents.append(E)

G.concurrents.append(H)

B.concurrents.append(C)

A.concurrents.append(C)

G1 = Graph()
G1.addCourse(A)
G1.addCourse(B)
G1.addCourse(C)
G1.addCourse(D)
G1.addCourse(E)
G1.addCourse(F)
G1.addCourse(G)
G1.addCourse(H)
G1.addCourse(I)
G1.addCourse(J)

# #G1.sort()
# print(G1)

G1.welshPowell()
print(G1)

# h = []
# for course in G1.courses:
#     heappush(h,(-1*len(course.concurrents),course))

# for c in h:
#     print(heappop(c))