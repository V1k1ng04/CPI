import peices
from ratings import Ratings

class ChessBoard:
    """
    Chessboard class will contain the 8x8 board array as well
    as all the functions needed to evaluate moves
    """

    def __init__(self):
        '''
        Initialize the chessboard. 
        Make sure that the first move when white plays is always e4.
        '''
        self.boardArray = [
            ["r", "k", "b", "q", "a", "b", "k", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "K", "B", "Q", "A", "B", "K", "R"]
        ]
        self.TOTALPIECES = 64
        self.kingPosition_White = 60
        self.kingPosition_Black = 4
        self.MAXDEPTH = 3

        # Flag to track if the first move (e4) has been played
        self.firstMovePlayed = False
        self.whiteTurn = True  # Flag to track white's turn

        # Play the first move as e4 if it's white's turn
        self.playFirstMove()

    def playFirstMove(self):
        """
        Makes the first move for white, which is always e4.
        This will only be done once and will be followed by AI's move.
        """
        if not self.firstMovePlayed and self.whiteTurn:
            # e4 move in chess translates to moving Pawn from e2 to e4
            self.computeMove(["1", "4", "3", "4", " "])  # Move pawn from e2 (1) to e4 (3)
            self.firstMovePlayed = True
            self.whiteTurn = False  # Switch turn after white's first move

    def generateMoveList(self):
        """
        Generates the list of possible moves for the pieces on the board.
        """
        movelist = ""
        rook = peices.Rook(self)
        knight = peices.Knight(self)
        bishop = peices.Bishop(self)
        queen = peices.Queen(self)
        king = peices.King(self)
        pawn = peices.Pawn(self)

        for index in range(self.TOTALPIECES):
            currentPosition = self.boardArray[index // 8][index % 8]

            # If current position is a rook
            if currentPosition == 'R':
                movelist += rook.findMoveSet(index)

            # If current position is a knight
            elif currentPosition == 'K':
                movelist += knight.findMoveSet(index)

            # If current position is a bishop
            elif currentPosition == 'B':
                movelist += bishop.findMoveSet(index)

            # If current position is a queen
            elif currentPosition == 'Q':
                movelist += queen.findMoveSet(index)

            # If current position is a king
            elif currentPosition == 'A':
                movelist += king.findMoveSet(index)

            # If current position is a pawn
            elif currentPosition == 'P':
                movelist += pawn.findMoveSet(index)

        return movelist

    def computeMove(self, move):
        """
        This method would simulate the actual move computation.
        Update the board with the new position based on the move.
        """
        # Here you would implement the logic that executes the move on the board
        # For example:
        start_row, start_col = int(move[0]), int(move[1])
        end_row, end_col = int(move[2]), int(move[3])

        # Logic to update board with the move would be here
        self.boardArray[end_row][end_col] = self.boardArray[start_row][start_col]
        self.boardArray[start_row][start_col] = " "

    def AI_make_move(self):
        """
        Make the AI's move after the first move is played.
        This method is called after white plays e4, and it generates the next move for AI.
        """
        if not self.whiteTurn:
            # AI would calculate its best move based on some strategy
            ai_move = self.calculate_ai_move()  # Placeholder for AI move calculation
            self.computeMove(ai_move)
            self.whiteTurn = True  # Switch turn back to white after AI's move

    def calculate_ai_move(self):
        """
        Placeholder function to simulate AI's move generation.
        """
        # Example AI move: this should be replaced by the actual AI decision-making logic
        return ["6", "4", "4", "4", " "]  # Sample move (e.g., move pawn from d7 to d5)

    # Other methods like kingissafe, computeMove, etc. remain the same


    def kingissafe(self):
        """
        Function that evaluates if a king is in check or is at risk of being in check
        This is very important, as this function affects the move sets of every Other
        peice if king is not safe (in check or at risk in being check)

        Returns: True if king is not at risk of being in check. False if king is
        at risk of being in check
        """

        # Initialize row and column king is currently on
        kingRow = self.kingPosition_White//8
        kingColumn = self.kingPosition_White % 8
        # For evaluating knight
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    # If position contains a knight
                    if self.boardArray[kingRow + i][kingColumn + 2*j] == "k" and kingRow + i >= 0 and kingColumn + 2*j >=0:
                        return False  # Move is not safe!
                except IndexError:
                    pass
                try:
                    # If position contains a knight
                    if self.boardArray[kingRow + 2*i][kingColumn +j] == "k" and kingRow + 2*i >= 0 and kingColumn + j >=0:
                        return False  # Move is not safe!
                except IndexError:
                    pass

        board_roamer = 1  # board_roamer variable used to increment through board

        # For evaluating King Moves
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i != 0 or j != 0:
                    try:
                        # If encountered move is a king
                        if self.boardArray[kingRow + i][kingColumn + j] == "a" and kingRow + i >= 0 and kingColumn + j >=0:
                            return False  # Move is not safe!
                    except IndexError:
                        pass

        # For evaluating Pawn
        # This is saying as long as the king is not in the top two rows (saves a bit of running time)
        if self.kingPosition_White >= 16:
            try:
                # If diagonal position contains a pawn
                if self.boardArray[kingRow -1][kingColumn -1] == "p" and kingRow - 1 >= 0 and kingColumn -1 >=0:
                    return False  # Move is not safe!
            except IndexError:
                pass
            try:
                # If diagonal position contains a pawn
                if self.boardArray[kingRow -1][kingColumn +1] == "p" and kingRow - 1 >= 0:
                    return False  # Move is not safe!
            except IndexError:
                pass

        # For evaluating multiple straight moving maxPlayers like the queen or rook
        for i in range(-1, 2, 2):
            try:
                # Infinite loop for traversing down horizontal until we hit a non-blank position
                while self.boardArray[kingRow][kingColumn + board_roamer*i] == " ":
                    board_roamer += 1  # Increment board roamer
                # If current detected peice is a queen or rook
                if self.boardArray[kingRow][kingColumn + board_roamer*i] == "r" or self.boardArray[kingRow][kingColumn + board_roamer*i] == "q" and kingColumn + board_roamer*i >= 0:
                    return False  # Move is not safe!
            except IndexError:
                pass
            board_roamer = 1  # set board_roamer back to start
            try:
                # Infinite loop for traversing down vertical until we hit a non-blank position
                while self.boardArray[kingRow + board_roamer*i][kingColumn] == " ":
                    board_roamer += 1  # Increment board roamer

                # If current postion we are looking at contains a rook or a queen
                if self.boardArray[kingRow + board_roamer*i][kingColumn] == "r" or self.boardArray[kingRow + board_roamer*i][kingColumn] == "q" and kingRow + board_roamer*i >= 0:
                    return False  # Move is not safe!
            except IndexError:
                pass
            board_roamer = 1  # set board_roamer back to start

        # For multiple diagonal moving maxPlayers like the queen or bishop
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    # Infinite loop for traversing down diagonal until we hit a non-blank position
                    while self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == " ":
                        board_roamer += 1  # Increment board roamer until we hit a peice or an edge
                    # If current detected peice is a queen or bishop
                    if self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == "b" or self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == "q" and kingRow + board_roamer*i >= 0 and kingColumn + board_roamer*j >= 0:
                        return False  # Move is not safe!

                except IndexError:
                    pass
                board_roamer = 1  # set board_roamer back to start

        # Return true if King passes all the tests!
        return True

    def computeMove(self, givenMove):
        """
        Function used to move a peice makes in the board to a legal position.

        Args: givenMove in the following forms:
            For regular Moves: [oldRow][oldColumn][newRow][newColumn][Peice]
            For Pawn Promotion: [oldColumn][newColumn][capturedPeice][PromotionPeice]["P"]
            For Castling: [columnRookOld][columnRookFinal][columnKing]["R"]["C"]

        """

        # If move is NOT regular move
        if givenMove[4] == "P" or givenMove[4] == "C":
            # If pawn promotion
            if givenMove[4] == "P":
                self.boardArray[1][int(givenMove[0])] = " "  # Set current position to blank
                self.boardArray[0][int(givenMove[1])] = givenMove[3]  # set position to Given promotion peice
            # If it's a castling move
            elif givenMove[4] == "C":
                # Moving the King
                self.boardArray[7][int(givenMove[0])] = " " # Set position rook sits in to blank
                self.boardArray[7][int(givenMove[1])] = "A" # Set new king position
                self.boardArray[7][int(givenMove[2])] = givenMove[3]  # set new rook position

        else:
            # Set previous position to blank and currentPosition to Peice
            self.boardArray[int(givenMove[2])][int(givenMove[3])] = self.boardArray[int(givenMove[0])][int(givenMove[1])]  # Set position to peice we are moving
            self.boardArray[int(givenMove[0])][int(givenMove[1])] = " "  # Set previous position peice was in to blank
            #  If new position is the human king
            if self.boardArray[int(givenMove[2])][int(givenMove[3])] == "A":
                self.kingPosition_White = 8*int(givenMove[2])+int(givenMove[3])  # Re adjust global king position
                # This is done so that our global position of king is properly adjusted



    def uncomputeMove(self, givenMove):
        """
        Function used to undo a move a peice makes in the board to a position. Move made
        will be unmade. Function is essentially the reverse of computeMove

        Args: givenMove in the form "[oldRow][oldColumn][newRow][newColumn][Piece]" for capturing or moving
        or "[column1][column2][captured-piece][new-piece][P]'' for pawn promotions
        """
        # Otherwise if it is a pawn promotion

        # If move is NOT a pawn promotion
        if givenMove[4] == "P" or givenMove[4] == "C":
            if givenMove[4] == "P":
                self.boardArray[1][int(givenMove[0])] = "P"  # Set square before promotion back to pawn
                self.boardArray[0][int(givenMove[1])] = givenMove[2]  # Set promotion position back to captured peice
            elif givenMove[4] == "C":
                # Moving the King
                self.boardArray[7][int(givenMove[1])] = " "
                self.boardArray[7][int(givenMove[2])] = "A"
                # Moving the Rook
                self.boardArray[7][int(givenMove[0])] = givenMove[3]

        else:
            # Set previous position to blank and currentPosition to PEICE
            self.boardArray[int(givenMove[0])][int(givenMove[1])] = self.boardArray[int(givenMove[2])][int(givenMove[3])]  # Set position back to previous peice
            self.boardArray[int(givenMove[2])][int(givenMove[3])] = givenMove[4]  # Set potential postion back to captured peice
            #  If position we undid was a king
            if self.boardArray[int(givenMove[0])][int(givenMove[1])] == "A":
                self.kingPosition_White = 8*int(givenMove[0])+int(givenMove[1])  # Undo global king position adjustment




    def alphaBeta(self, depth, beta, alpha, givenMove, maxPlayer):
        """
        Description: a search algorithm function based off the known alphaBeta pruning
        algorithm (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
        This algorithm is meant to find the best potential move the computer player can make

        For more information on the algorithm: http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
        Args:
                depth: How deep are we evaluating the tree (MAXDEPTH is 3 which is the deepest function will go to)
                Beta: is the minimum upper bound of possible solutions
                Alpha: is the maximum lower bound of possible solutions
                givenMove: is the move we are evaluating for rating
                maxPlayer: represented as either a 0 or 1 : the main idea is for a two-maxPlayer game,
                there are two kinds of nodes: nodes representing our moves and nodes representing our opponent's (The computer) moves.

        Returns: the optimal move with it's rating, represented in the form [move][score] (refer to findMoveSet for move format
                 The optimal rating will be alpha <= rating <= beta
        """
        moveslist = self.generateMoveList()  # Start by finding all current moves possible
        ratingE = Ratings(self)

        # If we hit the deepest possible depth or no moves are available
        if depth == 0 or len(moveslist) == 0:
            if givenMove == "":
                return None
            else:
                return givenMove + str(ratingE.evaluateRating(len(moveslist), depth)*(maxPlayer*2-1))  # Return move with negated rating

        maxPlayer = 1 - maxPlayer  # Set maxPlayer to opposite of current value

        # This loop will evaluate every single move in moveselist
        for i in range(0, len(moveslist), 5):
            # Make the move on the board
            self.computeMove(moveslist[i:(i+5)])
            # Change the perspective
            self.changePerspective()
            # Recursively calls alphaBeta with a depth 1 less than it's current
            # As well as evaluates the move we are currently on
            nextNode = self.alphaBeta(depth-1, beta, alpha, moveslist[i:(i+5)], maxPlayer)

            value = int(nextNode[5:])  # Store the value returned from next node
            #  We must change the perspective right side up again
            self.changePerspective()
            self.uncomputeMove(moveslist[i:(i+5)])  # Undo current move
            #  If we are currently looking at maxPlayer 0
            if maxPlayer == 0:
                # If our value is less than or equal to the current value of beta
                if value <= beta:
                    beta = value  # Set new beta to be current value
                    #  If we are at our global depth
                    if depth == self.MAXDEPTH:
                        givenMove = nextNode[0:5]  # Our current move is currently the optimal move that can be made
            else:
                # If our value is greater than the current value of alpha
                if value > alpha:
                    alpha = value  # Set new alpha to current value
                    # If we have reached our global depth
                    if depth == self.MAXDEPTH:
                        givenMove = nextNode[0:5]  # Our current move is currently the optimal move tha can be made
                # If we have broken out of our bound
                if alpha >= beta:
                    # If we are currently maxPlayer 0
                    if maxPlayer == 0:
                        return givenMove + str(beta)  # Return move plus our value (in this case beta)
                    # Otherwise if we are currently maxPlayer 1
                    else:

                        return givenMove + str(alpha)  # Return move plus our value (in this case alpha)
        # In the case where every move we have evaluated is not better than our current value
        # If we are currently maxPlayer 0
        if maxPlayer == 0:

            return givenMove + str(beta)  # Return move plus our value (in this case beta)
        # Otherwise if we are currently maxPlayer 1
        else:

            return givenMove + str(alpha)  # Return move plus our value (in this case alpha)

    def changePerspective(self):
        """
        Function to switch the point of view of the chessboard.
        Will switch maxPlayer's peices to opponent's chessPieces

        IMPORTANT NOTE: Don't think of this function as a visual flip of a Board
        but rather a change of perspective
        Example:
        Board is in Player's perspective
        call changePerspective
        Board is in opponent's perspective
        call call changePerspective
        Board is again in Player's perspective
        """

        # We only need to loop through the 'top' of the board
        for index in range(32):
            # Set our current row and column with respect to index
            row = index//8
            column = index % 8
            # If we are currently on one of our peices
            if self.boardArray[row][column].isupper():
                flipPeice = self.boardArray[row][column].lower()  # Set it as an enemy peice
            else:
                flipPeice = self.boardArray[row][column].upper()  # Set enemy peice as friendly otherwise

            # We compute the same evaluations as above but for the peice at the opposite corner
            # If currently one of our peices
            if self.boardArray[7-row][7-column].isupper():
                self.boardArray[row][column] = self.boardArray[7-row][7-column].lower() # Set current peice to enemy peice
            else:
                self.boardArray[row][column] = self.boardArray[7-row][7-column].upper()  # Set enemy peice as friendly otherwise

            self.boardArray[7-row][7-column] = flipPeice  # Set peice to flipped peice

        kingFlipped = self.kingPosition_White  # Set temporary kingFlipped variable for white position
        # Set new white and black king positions
        self.kingPosition_White = 63 - self.kingPosition_Black
        self.kingPosition_Black = 63 - kingFlipped
