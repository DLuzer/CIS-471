# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp
import util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """

  def __init__(self, mdp, discount=0.9, iterations=100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
          mdp.isTerminal(state)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter()  # A Counter is a dict with default 0
    self.runValueIteration()

  def runValueIteration(self):
    # Write value iteration code here
    "*** YOUR CODE HERE ***"
    for i in range(self.iterations):
      counter = util.Counter()
      for state in self.mdp.getStates():
        cur_val = float("-inf")
        for action in self.mdp.getPossibleActions(state):
          q = self.computeQValueFromValues(state, action)
          if q > cur_val:
            cur_val = q
          counter[state] = cur_val
      self.values = counter

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]

  def computeQValueFromValues(self, state, action):
    """
      Compute the Q-value of action in state from the
      value function stored in self.values.
    """
    "*** YOUR CODE HERE ***"
    ret_val = 0
    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
      ret_val += prob * (self.mdp.getReward(state, action,
                                            nextState) + self.discount * self.values[nextState])
    return ret_val

  def computeActionFromValues(self, state):
    """
      The policy is the best action in the given state
      according to the values currently stored in self.values.

      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    # initial check: if no actions, return None
    if self.mdp.isTerminal(state):
      return None
    # ensures any q value larger than initial
    cur_max = float("-inf")
    # look through possible actions
    for action in self.mdp.getPossibleActions(state):
      q = self.computeQValueFromValues(state, action)
      # if q larger, update current max val, ret_action
      if q > cur_max:
        cur_max = q
        ret_action = action
    # return action (or None if no actions available)
    return ret_action

  def getPolicy(self, state):
    return self.computeActionFromValues(state)

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.computeActionFromValues(state)

  def getQValue(self, state, action):
    return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
  """
      * Please read learningAgents.py before reading this.*

      An AsynchronousValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs cyclic value iteration
      for a given number of iterations using the supplied
      discount factor.
  """

  def __init__(self, mdp, discount=0.9, iterations=1000):
    """
      Your cyclic value iteration agent should take an mdp on
      construction, run the indicated number of iterations,
      and then act according to the resulting policy. Each iteration
      updates the value of only one state, which cycles through
      the states list. If the chosen state is terminal, nothing
      happens in that iteration.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state)
          mdp.isTerminal(state)
    """
    ValueIterationAgent.__init__(self, mdp, discount, iterations)

  def runValueIteration(self):
    "*** YOUR CODE HERE ***"
    states = self.mdp.getStates()
    states_len = len(states)
    for i in range(self.iterations):
      # counter = util.Counter() #no need for counter
      # cycle through states for number of iterations using modulo
      cur_state = states[i % states_len]
      #only non-terminal states need to be evaluated
      if not self.mdp.isTerminal(cur_state):
        cur_vals = []
        #get q_value for all actions and save max
        for action in self.mdp.getPossibleActions(cur_state):
          q = self.computeQValueFromValues(cur_state, action)
          cur_vals.append(q)
        self.values[cur_state] = max(cur_vals)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A PrioritizedSweepingValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs prioritized sweeping value iteration
      for a given number of iterations using the supplied parameters.
  """

  def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
    """
      Your prioritized sweeping value iteration agent should take an mdp on
      construction, run the indicated number of iterations,
      and then act according to the resulting policy.
    """
    self.theta = theta
    ValueIterationAgent.__init__(self, mdp, discount, iterations)

  def runValueIteration(self):
    "*** YOUR CODE HERE ***"

    predecessors = {}
    PQ = util.PriorityQueue()

    for state in self.mdp.getStates():
      if self.mdp.isTerminal(state) == False:
        for action in self.mdp.getPossibleActions(state):
          for next_state, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            if next_state in predecessors:
              predecessors[next_state].add(state)
            else:
              predecessors[next_state] = {state}
    
    for state in self.mdp.getStates():
      if self.mdp.isTerminal(state) == False:
        q_values = []
        for action in self.mdp.getPossibleActions(state):
          q = self.computeQValueFromValues(state, action)
          q_values.append(q)
        diff = abs(max(q_values) - self.values[state])
        PQ.update(state, -diff)

    for i in range(self.iterations):
      if PQ.isEmpty() == True:
        break
      temp_state = PQ.pop()
      if self.mdp.isTerminal(temp_state) == False:
        q_values = []
        for action in self.mdp.getPossibleActions(temp_state):
          q = self.computeQValueFromValues(temp_state, action)
          q_values.append(q)
        self.values[temp_state] = max(q_values)
    
      for predecessor in predecessors[temp_state]:
        if self.mdp.isTerminal(predecessor) == False:
          q_values = []
          for action in self.mdp.getPossibleActions(predecessor):
            q = self.computeQValueFromValues(predecessor, action)
            q_values.append(q)
          diff = abs(max(q_values) - self.values[predecessor])
          if diff > self.theta:
            PQ.update(predecessor, -diff)

    

