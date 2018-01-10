import random

def stones_game():
    # Generate a random amount of stones
    stones = random.randrange(20, 30)

    is_finished = False  # Signal when game is complete
    player_turn = 'A'  # Keep track of whos turn it is

    while not is_finished:
        # Print before we cancel loop. Prints at the ends that 1 stone is remaining
        print('\nPlayer', player_turn, 'turn :: ', stones, 'stones remain')
        if stones <= 1:
            break
        # Chck for a valid entry from the user
        valid_grab = False
        while not valid_grab:
            player_grabs = int(input('Pick a number 1, 2, or 3: Or enter 0 for a suggestion'))
            if player_grabs >= 1 and player_grabs <= 3:
                valid_grab = True
            elif player_grabs == 0:
                print('=== Magic wizard suggest you take', callCheat(stones), 'stone(s) to win ===')
            else:
                print('Invalid Entry, please try again')

        if player_turn == 'A':
            player_turn = 'B'
        else:
            player_turn = 'A'

        stones -= player_grabs

    if player_turn == 'A':
        print('\nCongradulations player B wins!')
    if player_turn == 'B':
        print('\nCongradulations player A wins!')


# Function that runs the cheat mode for the player
# low_val is the lowest value to reach in order to win.
def callCheat(stones_left):
    # Player will loose so just choose random number of stones to take
    if stones_left == 5:
        return random.randrange(1, 4)
    # Guaranteed win for player
    elif stones_left < 5:
        return stones_left - 1
    else:
        new_cheat = GameTree()
        return new_cheat.run(stones_left, 1)


# Must add children to the node in the order from -1 to -3 stones takes from the pile
class Node(object):
    def __init__(self, v):
        self.kids = []
        self.value = v

    def addKid(self, kid):
        self.kids.append(kid)

    def getValue(self):
        return self.value


# Inserting first object will set the root value of the game tree.
class GameTree(object):
    def __init__(self):
        self.root = None

    def run(self, start_value, lowest_value):
        self.root_node = Node(start_value)
        self.buildTree(self.root_node, start_value, lowest_value)
        # add one because the index starts at 0. We need it to start at 1.
        return self.searchBestMove(self.root_node, lowest_value) + 1

    def buildTree(self, node, value, lowest_value):
        if value < lowest_value:
            return
        for j in range(1, 4):
            temp_node = Node(node.value - j)
            node.addKid(temp_node)
            self.buildTree(temp_node, node.value - j, lowest_value)

    # Collects the occurence, if any, of the lowest_value. Searching the child node array of each node 2 tree levels down.
    # This is done for each child nodes of the root_node. Each lowest lowest_value increments the rank of the branch by 1.
    # The total becomes branch rank. and becomes the brach of choice. Basically the branch that you have the highest chance
    # of reaching the lowest_value.
    def searchBestMove(self, root, low_val):

        return round(self.traverseTreeRankBranch(root, low_val))

    def traverseTreeRankBranch(self, root_node, lowest_value):
        # i us the choice that needs to be returned
        temp_roots = []
        branch_rank = [0, 0, 0]
        x_zero = 0
        x_max = 0
        x_index = 2
        for i, child_node in enumerate(root_node.kids):
            for sub_child_node in child_node.kids:
                temp_roots.append(sub_child_node)
                for n in sub_child_node.kids:
                    if n.value is lowest_value:
                        branch_rank[i] += 1

        # Get the index of the largest value in the array

        for i, n in enumerate(branch_rank):
            x_zero = 0
            x_zero += n
            if x_max < n:
                x_max = n
                x_index = i

        # All branches are the same rank. traverseTreeRankBranch again
        if x_zero is 0:
            return (self.traverseTreeRankBranch(temp_roots[0], lowest_value) + self.traverseTreeRankBranch(temp_roots[1],
                                                                                                          lowest_value) + self.traverseTreeRankBranch(
                temp_roots[2], lowest_value) ) / 3
        # found a good match return the value of the index. note index starts at 0
        else:
            return x_index


# Main program
stones_game()
