# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #initialization
    state = problem.getStartState()
    visit =[]
    road=[]
    unvisit=util.Stack()
    #until meet goal
    while  problem.isGoalState(state)!=True:
        action = problem.getSuccessors(state)
        visit.append(state)
        i = 0
        #when there isn't any successors
        while len(action)==0 and problem.isGoalState(state)!=True:
            road.pop()
            temp=unvisit.pop()
            while temp[0] in visit:
                temp = unvisit.pop()
                if temp == [0, 0]:
                    temp = unvisit.pop()
                    road.pop()
            state=temp[0]
            visit.append(state)
            road.append(temp[1])
            action= problem.getSuccessors(state)
        #memory unvisit points
        if len(action)>0:
            unvisit.push([0, 0]) #add signal
            for k in range(1,len(action)):
                unvisit.push([action[len(action)-k][0],action[len(action)-k][1]])
        #avoid walking backward
        while action[i][0] in visit and problem.isGoalState(state)!=True:
            i=i+1
            if i== len(action):
                temp = unvisit.pop()
                while temp[0] in visit:
                    temp = unvisit.pop()
                    if temp==[0,0]:
                        temp = unvisit.pop()
                        road.pop()
                state = temp[0]
                visit.append(state)
                road.append(temp[1])
                action = problem.getSuccessors(state)
                i=0
                continue

        state=action[i][0]
        road.append(action[i][1])

    return road



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # initialization
    state = problem.getStartState()
    visit = []
    visit.append(state)
    road = []
    unvisit = util.Queue()
    ans=util.Stack()
    end=[]
    # until meet goal
    while problem.isGoalState(state) != True:
        action = problem.getSuccessors(state)
        # memory unvisit points
        if len(action) > 0:
            for k in range(0, len(action)):
                unvisit.push([action[k][0], action[k][1], state]) #[now,path,parent]

        temp = unvisit.pop()

        # avoid walking backward
        while temp[0] in visit and problem.isGoalState(state) != True:
            temp = unvisit.pop()

        state=temp[0]
        road.append([temp[0],temp[1],temp[2]])
        visit.append(state)

    # get one road
    k=road.pop()
    ans.push(k[1])
    for n in range(len(road)):
        p=road.pop()
        if k[2]==p[0]:
            ans.push(p[1])
            k=p
    while ans.isEmpty()!=True:
        end.append(ans.pop())

    return end


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # initialization
    state = problem.getStartState()
    visit = []
    visit.append(state)
    road = []
    unvisit = util.PriorityQueue()
    ans = util.Stack()
    previousWeight= 0
    end = []

     # until meet goal
    while problem.isGoalState(state) != True:
        action = problem.getSuccessors(state)
        # memory unvisit points
        if len(action) > 0:
            for k in range(0, len(action)):
                for h in range(k+1, len(action)):
                    if action[k][2]>action[h][2]:
                        d=action[k]
                        action[k]=action[h]
                        action[h]=d
            for k in range(0, len(action)):
                unvisit.push([action[k][0], action[k][1], state,previousWeight+action[k][2]],previousWeight+action[k][2]) #[now,path,parent,trackWeightTotal],trackWeightTotal

        temp = unvisit.pop()

        # avoid walking backward
        while temp[0] in visit and problem.isGoalState(state) != True:
            temp = unvisit.pop()

        state=temp[0]
        previousWeight = temp[3] #previous trackWeight
        road.append([temp[0],temp[1],temp[2]])
        visit.append(state)

    # get one road
    k=road.pop()
    ans.push(k[1])
    for n in range(len(road)):
        p=road.pop()
        if k[2]==p[0]:
            ans.push(p[1])
            k=p
    while ans.isEmpty()!=True:
        end.append(ans.pop())

    return end
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    visit = []
    visit.append(state)
    road = []
    unvisit = util.PriorityQueue()
    ans = util.Stack()
    previousWeight= 0
    end = []

     # until meet goal
    while problem.isGoalState(state) != True:
        action = problem.getSuccessors(state)
        # memory unvisit points

        if len(action) > 0:
            for k in range(0, len(action)):
                for h in range(k+1, len(action)):
                    if action[k][2]>action[h][2]:
                        d=action[k]
                        action[k]=action[h]
                        action[h]=d
            for k in range(0, len(action)):
                unvisit.push([action[k][0], action[k][1], state,previousWeight+action[k][2]],previousWeight+action[k][2]+heuristic(action[k][0], problem)) #[now,path,parent,trackWeightTotal],trackWeightTotal

        temp = unvisit.pop()

        # avoid walking backward
        while temp[0] in visit and problem.isGoalState(state) != True:
            temp = unvisit.pop()

        state=temp[0]
        previousWeight = temp[3] #previous trackWeight
        road.append([temp[0],temp[1],temp[2]])
        visit.append(state)

    # get one road
    k=road.pop()
    ans.push(k[1])
    for n in range(len(road)):
        p=road.pop()
        if k[2]==p[0]:
            ans.push(p[1])
            k=p
    while ans.isEmpty()!=True:
        end.append(ans.pop())

    return end


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

