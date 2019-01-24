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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # Data Structs
    BFSdirections = []
    Visited = []
    current_path = []
    Fringe = util.Stack()
    all_paths = util.Stack()

    # Initial actions
    root = problem.getStartState()
    Fringe.push((root, "", 0))

    while(Fringe.isEmpty() == False):
        # erase previous successors
        currentSuccessors = []
        # pop new node from Fringe
        current_node = Fringe.pop()
        print("")
        print("-------New Node-------")
        print("Current node:     ", current_node[0], current_node[1])

        # if current_node is not root, get path
        if problem.getStartState() != current_node[0]:
            current_path = all_paths.pop()

        # if we are at the goal, break loop and send directions to game
        if problem.isGoalState(current_node[0]) == True:
            break

        # mark state as visited
        Visited.append(current_node[0])

        currentSuccessors = problem.getSuccessors(current_node[0])
        # for each successor, check if it is a legal action
        for state, dir, cost in currentSuccessors:
            print("Legal successor?: ", state, dir)

            # if action is legal and not visited yet, add to fringe and current_path
            if problem.getCostOfActions(current_path + [dir]) != 999999 and state not in Visited:
                print("Yes, + to fringe: ", state, dir)
                Fringe.push((state, dir, cost))
                all_paths.push(current_path + [dir])
            # else do nothing
            else:
                print("No.")

        print("Current paths in consideration:")
        for path in all_paths.list:
            print(path)
        print("")

    print("")

    print("----------------------------------------")
    print("-------------DONE WITH LOOP-------------")
    print("----------------------------------------")
    print("OUR ANSWER: ", current_path)
    print("")
    return current_path
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # Data Structs
    BFSdirections = []
    Visited = []
    current_path = []
    Fringe = util.Queue()
    all_paths = util.Queue()

    # Initial actions
    root = problem.getStartState()
    Fringe.push((root, "", 0))

    while(Fringe.isEmpty() == False):
        # erase previous successors
        currentSuccessors = []
        # pop new node from Fringe
        current_node = Fringe.pop()
        print("")
        print("-------New Node-------")
        print("Current node:     ", current_node[0], current_node[1])

        # if current_node is not root, get path
        if problem.getStartState() != current_node[0]:
            current_path = all_paths.pop()

        # if we are at the goal, break loop and send directions to game
        if problem.isGoalState(current_node[0]) == True:
            break

        # mark state as visited
        Visited.append(current_node[0])

        currentSuccessors = problem.getSuccessors(current_node[0])
        # for each successor, check if it is a legal action
        for state, dir, cost in currentSuccessors:
            print("Legal successor?: ", state, dir)

            # if action is legal and not visited yet, add to fringe and current_path
            if problem.getCostOfActions(current_path + [dir]) != 999999 and state not in Visited:
                print("Yes, + to fringe: ", state, dir)
                Fringe.push((state, dir, cost))
                all_paths.push(current_path + [dir])
            # else do nothing
            else:
                print("No.")

        print("Current paths in consideration:")
        for path in all_paths.list:
            print(path)
        print("")

    print("")

    print("----------------------------------------")
    print("-------------DONE WITH LOOP-------------")
    print("----------------------------------------")
    print("OUR ANSWER: ", current_path)
    print("")
    return current_path
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # Data Structs
    BFSdirections = []
    Visited = []
    current_path = []
    Fringe = util.Stack()
    all_paths = util.Stack()

    # Initial actions
    root = problem.getStartState()
    Fringe.push((root, "", 0))

    while(Fringe.isEmpty() == False):
        # erase previous successors
        currentSuccessors = []
        # pop new node from Fringe
        current_node = Fringe.pop()
        print("")
        print("-------New Node-------")
        print("Current node:     ", current_node[0], current_node[1])

        # if current_node is not root, get path
        if problem.getStartState() != current_node[0]:
            current_path = all_paths.pop()

        # if we are at the goal, break loop and send directions to game
        if problem.isGoalState(current_node[0]) == True:
            break

        # mark state as visited
        Visited.append(current_node[0])

        currentSuccessors = problem.getSuccessors(current_node[0])
        # for each successor, check if it is a legal action
        ordered_successors = []
        for state, dir, cost in currentSuccessors:
            print("Legal successor?: ", state, dir)
            # if action is legal and not visited yet, add to fringe and current_path
            if problem.getCostOfActions(current_path + [dir]) != 999999 and state not in Visited:
                print("Yes, + to fringe: ", state, dir)
                # ordered_successors.append((state, dir, cost))
                if not ordered_successors:
                    print("appending")
                    ordered_successors.append((state, dir, cost))
                else:
                    print("in else")
                    added = 0
                    i = 0
                    for succ in ordered_successors:
                        print("for-looping")
                        print(succ[2])
                        if cost >= succ[2]:
                            ordered_successors.insert(i, (state, dir, cost))
                            added = 1
                            break
                        else:
                            i += 1
                    if added == 0:
                        ordered_successors.append((state, dir, cost))
            # else do nothing
            else:
                print("No.")
        print("ORDERED_SUCCESSORS: ", ordered_successors)
        for succ in ordered_successors:
            Fringe.push(succ)
            all_paths.push(current_path + [succ[1]])

        print("Current paths in consideration:")
        for path in all_paths.list:
            print(path)
        print("")

    print("")

    print("----------------------------------------")
    print("-------------DONE WITH LOOP-------------")
    print("----------------------------------------")
    print("OUR ANSWER: ", current_path)
    print("")
    return current_path
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    Fringe = util.PriorityQueue()

    #Keeps track of path coordinates EX: (1,1)
    Visited = []

    #Alternative_nodes = util.PriorityQueue()

    ASTARdirections = []
    Sketchy_path = []

    root = problem.getStartState()
    Fringe.push((root, "", 0), 0)

    while(Fringe.isEmpty() == False):
        print("Fringe before pop:", Fringe.heap)
        current_node = Fringe.pop()
        print("Successful node:", current_node)
        print(Fringe.count,"left in the Fringe")
        
        if problem.isGoalState(current_node[0]) == True:
            break

        Visited.append(current_node[0])
        
        ordered_successors = util.PriorityQueue()

        for next_node in problem.getSuccessors(current_node[0]):
            if next_node[0] in Visited:
                print("Failed node - In Visited:", next_node)
                #print(Visited)
                continue
            if problem.getCostOfActions(ASTARdirections + [next_node[1]]) == 999999:
                print("Failed node - Invalid Path:", next_node)
                #print(ASTARdirections + [next_node[1]])
                continue
            heuristic_cost = heuristic(next_node[0], problem)
            actual_cost = next_node[2]

            fn = heuristic_cost + actual_cost
            ordered_successors.push((next_node, fn), fn)

            print(next_node,"- f(n):", fn)
        print("All successors:", ordered_successors.heap)
        #Went down the wrong path
        if ordered_successors.count == 0:
            print("Sketchy path:", Sketchy_path)
            print("ASTARdirections:", ASTARdirections)
            for i in range(len(Sketchy_path)):
                del ASTARdirections[-1]
            Sketchy_path = []
        #Have multiple paths, picks the best one depending on f(n) = g(n) + h(n)
        else:
            #print("First:", ordered_successors.count)
            if ordered_successors.count == 1:
    
            chosen_successor = ordered_successors.pop()
            print("Chosen successor:", chosen_successor)
            ASTARdirections.append(chosen_successor[0][1])
            Fringe.push(chosen_successor[0], chosen_successor[1])
        
            while ordered_successors.isEmpty() == False:
                #print("Next:", ordered_successors.count)
                next_successor = ordered_successors.pop()
                print("Next successor:", next_successor)
                Fringe.push(next_successor[0], next_successor[1])
                #Alternative_nodes.push(next_successor[0], next_successor[1])
    
    test = ['North','North','North']

    #return test
    return ASTARdirections

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
