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
import random, util

from game import Agent

class RandomAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        # Pick randomly among the legal
        chosenIndex = random.choice(range(0, len(legalMoves)))
        return legalMoves[chosenIndex]

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        total = successorGameState.getScore()

        distanceToGhost = min([manhattanDistance(newPos, ghostPos) for ghostPos in successorGameState.getGhostPositions()])
        total += distanceToGhost

        distanceToFood = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        total -= min(distanceToFood) if len(distanceToFood) > 0 else 0

        return total

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"
        def H_Minimax(state, currDepth, agentIndex):
            result = []

            result = [(action, MinValue(state.generateSuccessor(agentIndex, action), currDepth, agentIndex + 1)) for
                      action in state.getLegalActions(agentIndex)]

            action, cost = max(result, key=lambda x:x[1])
            return action

        def MaxValue(state, currDepth, agentIndex):
            if currDepth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            result = []

            result = [MinValue(state.generateSuccessor(agentIndex, action), currDepth, agentIndex + 1) for
                      action in state.getLegalActions(agentIndex)]

            return max(result) if len(result) > 0 else float('-inf')


        def MinValue(state, currDepth, agentIndex):
            if state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            result = []

            if agentIndex + 1 == state.getNumAgents():
                result = [MaxValue(state.generateSuccessor(agentIndex, action), currDepth + 1, 0) for
                          action in state.getLegalActions(agentIndex)]
            else:
                result = [MinValue(state.generateSuccessor(agentIndex, action), currDepth, agentIndex + 1) for
                          action in state.getLegalActions(agentIndex)]

            return min(result) if len(result) > 0 else float('inf')

        return H_Minimax(gameState, 0, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def AlphaBeta(state, currDepth, agentIndex):

            value, action = MaxValue(state, currDepth, agentIndex, float('-inf'), float('inf'))

            return action

        def MaxValue(state, currDepth, agentIndex, alpha, beta):
            if currDepth == self.depth or state.isLose() or state.isWin():
                return self.evaluationFunction(state), None
            v = float('-inf')
            move = None

            for action in state.getLegalActions(agentIndex):
                newState = state.generateSuccessor(agentIndex, action)
                v2, a2 = MinValue(newState, currDepth, agentIndex + 1, alpha, beta)

                if v2 > v:
                    v, move = v2, action
                    alpha = max(alpha, v)

                if v >   beta:
                    return v, move

            return v, move

        def MinValue(state, currDepth, agentIndex, alpha, beta):
            if state.isLose() or state.isWin():
                return (self.evaluationFunction(state), None)
            v = float('inf')

            for action in state.getLegalActions(agentIndex):
                newState = state.generateSuccessor(agentIndex, action)

                if agentIndex + 1 == state.getNumAgents():
                    v2, a2 = MaxValue(state.generateSuccessor(agentIndex, action), currDepth + 1, 0, alpha, beta)
                else:
                    v2, a2 = MinValue(state.generateSuccessor(agentIndex, action), currDepth, agentIndex + 1, alpha, beta)

                if v2 < v:
                   v, move = v2, action
                   beta = min(beta, v)

                if v < alpha:
                    return v, move

            return v, move

        return AlphaBeta(gameState, 0, 0)

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

