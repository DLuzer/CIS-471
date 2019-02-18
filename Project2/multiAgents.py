# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        distList = []
        foodList = currentGameState.getFood().asList()
        posList = list(successorGameState.getPacmanPosition())
        negINF = -float("inf")

        # trivial case: action is stop
        if action == 'Stop':
            return negINF

        # otherwise, check states for if a "not scared" ghost is at the same position as Pac-Man
        for state in newGhostStates:
            if state.getPosition() == tuple(posList) and state.scaredTimer is 0:
                return negINF

        # if not, use manhattan heuristic to determine closest food pellet
        for dot in foodList:
            distList.append(-1 * manhattanDistance(
                (dot[0], dot[1]), (posList[0], posList[1])))
        return max(distList)
        # return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        curDepth, curIndex = 0, 0
        retAction = self.value(gameState, curIndex, curDepth)
        return retAction[0]

    def value(self, gameState, curIndex, curDepth):
        # trivial checks
        if curIndex >= gameState.getNumAgents():
            curIndex = 0
            curDepth += 1

        if curDepth == self.depth:
            return self.evaluationFunction(gameState)

        # if Pac-Man node, want to find Max; if not, want to find probabilities
        if curIndex == self.index:
            # isMax == True
            return self.expMax(True, gameState, curIndex, curDepth)
        else:
            # isMax == False
            return self.expMax(False, gameState, curIndex, curDepth)

    def expMax(self, isMax, gameState, curIndex, curDepth):
        if not gameState.getLegalActions(curIndex):
            return self.evaluationFunction(gameState)

        # set initial value
        # empty action; 0 for exp and negative infinity for Max
        v = ["", 0] if isMax is False else ("", -float("inf"))

        # set probabilities (for use in exp)
        expProb = 1.0 / len(gameState.getLegalActions(curIndex))

        # recursively update v values for legal action available
        for action in gameState.getLegalActions(curIndex):
            retVal = self.value(gameState.generateSuccessor(
                curIndex, action), curIndex + 1, curDepth)
            if type(retVal) is tuple:
                retVal = retVal[1]
            if isMax == False:
                v[0] = action
                v[1] += retVal * expProb
            elif isMax == True:
                vMax = max(v[1], retVal)

                if vMax is not v[1]:
                    v = (action, vMax)

        retVal = tuple(v) if isMax == False else v

        return retVal


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    FACTORS WE CONSIDERED (for each state):
     - Current game score
     - Number of food dots left
     - Distance to ghosts and their state (scared, not scared)
     - Distance to closest and second closest food


    WHY:
     - CURRENT GAME SCORE is useful for implicitly incentivizing PacMan (to not bump into ghosts, to eat food, to eat scared ghosts). A times 10 multiplier was added to this baseline value to increase its importance.

     - From there, we added incentizes and multipliers to prioritize certain things:
        - FOOD LEFT: A negative incentive was added for the amount of food left, incentivizing Pac-Man to eat food whenever possibe. A times 10 multiplier was added to this value as well.

        - GHOSTS 3 blocks or closer are a large threat and should be avoided at all costs; increasingly larger negative incentives were added to ensure Pac-Man would not die.

        - SCARED GHOSTS 3 blocks or closer are a great opportunity to gain points; a set positive incentive was added for Pac-Man to go chase scared ghosts.

        - CLOSEST FOOD: The two closest foods were both considered to incentivize Pac-Man to travel towards food. We originally only considered the closest food, but ran into problems when one food dot was isolated. In this case, Pac-Man would not eat it, as it would greatly increase the closestFood distance if he did. There was a larger incentive to sit right next to the dot than there was to eat it! Therefore, we decided to add the second closest food as well, to help decrease the effects of a single isolated food dot on the overall evaluation.
    """
    "*** YOUR CODE HERE ***"
    ghostList = currentGameState.getGhostStates()
    foodList = currentGameState.getFood().asList()
    posList = list(currentGameState.getPacmanPosition())

    distToFoodList = []
    ghostInfo = []                          # 2D array: [dist, isScared]
    distToCapsuleList = []
    score = 0

    for state in ghostList:                 # get info for all ghosts
        if state.scaredTimer is not 0:      # scared ghost
            ghostInfo.append([0, 1])
        else:                               # not scared ghost
            ghostXY = state.getPosition()
            manDist = manhattanDistance(
                (ghostXY[0], ghostXY[1]), (posList[0], posList[1]))
            ghostInfo.append([manDist, 0])

    for dot in foodList:                    # get manhattan dist for all food dots
        distToFoodList.append(-1 * manhattanDistance(
            (dot[0], dot[1]), (posList[0], posList[1])))

    # scoring logic
    closestFood = 0
    closestFood2 = 0
    closestFood3 = 0
    ghostScore = 0
    curScore = currentGameState.getScore()
    # incentivize with manhattan distance values for two closest food dots

    temp = distToFoodList
    if temp:
        closestFood = max(temp)
        temp.remove(closestFood)
        if temp:
            closestFood2 = max(temp)

    # positive scores for scared ghosts nearby, (increasing) negative scores for regular ghosts nearby

    for ghost in ghostInfo:
        if ghost[0] == 3 and ghost[1] == 0:  # ghost within 3 spots = get away!
            ghostScore -= 25
        elif ghost[0] == 2 and ghost[1] == 0:
            ghostScore -= 50
        elif ghost[0] <= 1 and ghost[1] == 0:
            ghostScore -= 100
        elif ghost[0] <= 1 and ghost[1] == 1:
            ghostScore += 100

    return closestFood + 2 * closestFood2 + ghostScore + 10 * curScore - 10 * len(foodList)


# Abbreviation
better = betterEvaluationFunction
