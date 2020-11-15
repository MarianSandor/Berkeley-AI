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


class Node:
    def __init__(self, state=None, parent=None, action=None, path_cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __str__(self):
        return "Current State: {} Parent State: {} Action: {} Cost = {}".format(self.state, self.parent, self.action,
                                                                                self.path_cost)

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

def randomSearch(problem):
    from game import Directions
    from random import choice

    actions = []

    succ = choice(problem.getSuccessors(problem.getStartState()))
    actions.append(succ[1])

    while not problem.isGoalState(succ[0]):
        succ = choice(problem.getSuccessors(succ[0]))
        actions.append(succ[1])

    return actions

def getPath(node):
    solution = []

    while node is not None:
        if node.action is not None:
            solution = [node.action] + solution
        node = node.parent

    return solution

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    S = util.Stack()
    E = []

    S.push(Node(problem.getStartState(), None, None, 0))

    while not S.isEmpty():
        node = S.pop()

        if node.state not in E:
            if problem.isGoalState(node.state):
                return getPath(node)

            E.append(node.state)

            for (state, action, cost) in problem.getSuccessors(node.state):
                new_node = Node(state, node, action, node.path_cost + cost)
                S.push(new_node)

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    Q = util.Queue()
    E = []

    Q.push(Node(problem.getStartState(), None, None, 0))

    while not Q.isEmpty():
        node = Q.pop()

        if node.state not in E:
            if problem.isGoalState(node.state):
                return getPath(node)

            E.append(node.state)

            for (state, action, cost) in problem.getSuccessors(node.state):
                new_node = Node(state, node, action, node.path_cost + cost)
                Q.push(new_node)

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    PQ = util.PriorityQueue()
    E = []

    node = Node(problem.getStartState(), None, None, 0)
    PQ.push(node, node.path_cost)

    while not PQ.isEmpty():
        node = PQ.pop()

        if node.state not in E:
            if problem.isGoalState(node.state):
                return getPath(node)

            E.append(node.state)

            for (state, action, cost) in problem.getSuccessors(node.state):
                new_node = Node(state, node, action, node.path_cost + cost)
                PQ.push(new_node, new_node.path_cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    PQ = util.PriorityQueue()
    E = []

    node = Node(problem.getStartState(), None, None, 0)
    PQ.push(node, node.path_cost + heuristic(node.state, problem))

    while not PQ.isEmpty():
        node = PQ.pop()

        if node.state not in E:
            if problem.isGoalState(node.state):
                return getPath(node)

            E.append(node.state)

            for (state, action, cost) in problem.getSuccessors(node.state):
                new_node = Node(state, node, action, node.path_cost + cost)
                PQ.push(new_node, new_node.path_cost + heuristic(new_node.state, problem))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
