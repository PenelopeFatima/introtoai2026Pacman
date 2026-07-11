# search.py
# ---------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that:
# (1) you do not distribute or publish solutions,
# (2) you retain this notice, and
# (3) you provide clear attribution to UC Berkeley,
# including a link to http://ai.berkeley.edu.
#
# Attribution Information:
# The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by
# John DeNero and Dan Klein.
# Student-side autograding was added by Brad Miller, Nick Hay,
# and Pieter Abbeel.


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).

Implemented search strategies:
    1. Depth-First Search (DFS)
    2. Breadth-First Search (BFS)
    3. Uniform-Cost Search (UCS)
    4. A* Search
"""


import util
from game import Directions
from typing import List


class SearchProblem:
    """
    This class outlines the structure of a search problem, but does not
    implement any of the methods.

    You do not need to change anything in this class.
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

        For a given state, this returns a list of triples:

            (successor, action, stepCost)

        successor:
            The next state.

        action:
            The action required to reach that state.

        stepCost:
            The cost of moving to that state.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take.

        Returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


# ============================================================
# DEPTH-FIRST SEARCH (DFS)
# ============================================================

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    DFS uses a Stack (LIFO):
        Last In, First Out.
    """

    # Create the stack
    frontier = util.Stack()

    # Get the starting state
    start_state = problem.getStartState()

    # Store:
    # (current state, actions taken to reach the state)
    frontier.push((start_state, []))

    # Keep track of visited states
    visited = set()

    # Continue until there are no states left to explore
    while not frontier.isEmpty():

        # Remove the most recently added state
        state, actions = frontier.pop()

        # Skip the state if it has already been explored
        if state in visited:
            continue

        # Check if the current state is the goal
        if problem.isGoalState(state):
            return actions

        # Mark the state as visited
        visited.add(state)

        # Get all possible successor states
        for successor, action, stepCost in problem.getSuccessors(state):

            # Only add states that have not been visited
            if successor not in visited:

                # Add the new action to the current path
                new_actions = actions + [action]

                # Add the successor to the stack
                frontier.push(
                    (successor, new_actions)
                )

    # Return an empty list if no solution is found
    return []


# ============================================================
# BREADTH-FIRST SEARCH (BFS)
# ============================================================

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the shallowest nodes in the search tree first.

    BFS uses a Queue (FIFO):
        First In, First Out.

    BFS finds the shortest path when all step costs are equal.
    """

    # Create the queue
    frontier = util.Queue()

    # Get the starting state
    start_state = problem.getStartState()

    # Store:
    # (current state, actions taken to reach the state)
    frontier.push((start_state, []))

    # Mark the starting state as visited
    visited = {start_state}

    # Continue until there are no states left to explore
    while not frontier.isEmpty():

        # Remove the oldest state from the queue
        state, actions = frontier.pop()

        # Check if the current state is the goal
        if problem.isGoalState(state):
            return actions

        # Explore all successor states
        for successor, action, stepCost in problem.getSuccessors(state):

            # Only explore states that have not been visited
            if successor not in visited:

                # Mark the successor as visited immediately
                # to prevent duplicate entries in the queue
                visited.add(successor)

                # Add the new action to the current path
                new_actions = actions + [action]

                # Add the successor to the queue
                frontier.push(
                    (successor, new_actions)
                )

    # Return an empty list if no solution is found
    return []


# ============================================================
# UNIFORM-COST SEARCH (UCS)
# ============================================================

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the node with the lowest total path cost first.

    UCS uses a Priority Queue.

    The node with the lowest total cost is explored first.
    """

    # Create the priority queue
    frontier = util.PriorityQueue()

    # Get the starting state
    start_state = problem.getStartState()

    # Starting cost is zero
    start_cost = 0

    # Store:
    # (current state, actions taken, total cost)
    frontier.push(
        (start_state, [], start_cost),
        start_cost
    )

    # Dictionary containing the lowest known cost
    # for each explored state
    best_cost = {}

    # Continue until there are no states left to explore
    while not frontier.isEmpty():

        # Remove the state with the lowest priority
        state, actions, cost = frontier.pop()

        # Skip this path if a cheaper path to the same state
        # has already been processed
        if state in best_cost and cost > best_cost[state]:
            continue

        # Record the lowest known cost
        best_cost[state] = cost

        # Check if the current state is the goal
        if problem.isGoalState(state):
            return actions

        # Explore successor states
        for successor, action, stepCost in problem.getSuccessors(state):

            # Calculate the new total cost
            new_cost = cost + stepCost

            # Add the new action to the current path
            new_actions = actions + [action]

            # Only add the successor if:
            # 1. It has not been explored before, or
            # 2. We found a cheaper path to it
            if (
                successor not in best_cost
                or new_cost < best_cost[successor]
            ):

                # Add successor to the priority queue
                # Priority = total path cost
                frontier.push(
                    (successor, new_actions, new_cost),
                    new_cost
                )

    # Return an empty list if no solution is found
    return []


# ============================================================
# NULL HEURISTIC
# ============================================================

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state
    to the nearest goal.

    This heuristic always returns 0.

    When A* uses this heuristic, it behaves like Uniform-Cost Search.
    """

    return 0


# ============================================================
# A* SEARCH
# ============================================================

def aStarSearch(
    problem: SearchProblem,
    heuristic=nullHeuristic
) -> List[Directions]:
    """
    Search the node with the lowest combined actual cost
    and estimated future cost.

    A* uses:

        f(n) = g(n) + h(n)

    where:

        g(n) = actual cost from the start state
        h(n) = estimated cost from the current state to the goal
        f(n) = estimated total cost
    """

    # Create the priority queue
    frontier = util.PriorityQueue()

    # Get the starting state
    start_state = problem.getStartState()

    # Actual cost at the starting state
    start_cost = 0

    # Calculate the starting priority
    start_priority = (
        start_cost
        + heuristic(start_state, problem)
    )

    # Store:
    # (current state, actions taken, actual cost)
    frontier.push(
        (start_state, [], start_cost),
        start_priority
    )

    # Dictionary containing the cheapest known actual cost
    # for each explored state
    best_cost = {}

    # Continue until there are no states left to explore
    while not frontier.isEmpty():

        # Remove the state with the lowest priority
        state, actions, cost = frontier.pop()

        # Skip this path if a cheaper path to the same state
        # has already been processed
        if state in best_cost and cost > best_cost[state]:
            continue

        # Record the cheapest known cost
        best_cost[state] = cost

        # Check if the current state is the goal
        if problem.isGoalState(state):
            return actions

        # Explore successor states
        for successor, action, stepCost in problem.getSuccessors(state):

            # Calculate the actual cost to the successor
            new_cost = cost + stepCost

            # Add the new action to the current path
            new_actions = actions + [action]

            # Continue if the successor is new
            # or if we found a cheaper path
            if (
                successor not in best_cost
                or new_cost < best_cost[successor]
            ):

                # Calculate A* priority
                #
                # f(n) = g(n) + h(n)
                priority = (
                    new_cost
                    + heuristic(successor, problem)
                )

                # Add successor to the priority queue
                frontier.push(
                    (successor, new_actions, new_cost),
                    priority
                )

    # Return an empty list if no solution is found
    return []


# ============================================================
# ABBREVIATIONS
# ============================================================
#
# These abbreviations allow Pacman to call the search algorithms
# from the command line.
#
# Example:
#
# python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs
#

bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch