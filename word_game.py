from argparse import ArgumentParser
import sys

class PlayerWords:
    """A class representing a player's words in a word game.
    
    Attributes:
        words (set): A set having the words found by a player.
        
    Side effects: 
        Setting the attribute to 'words'
    
    """
    
    def __init__(self, input_file):
        """Initialize PlayerWords with words read from input_file.
        
        Args:
            input_file (str): Path to a text file containing words found by the player.
        Side effects:
            Reads words from file and add 'words' to set

        """
        self.words = set()
        with open(input_file, "r") as infile:
            for line in infile:
                word = line.strip()
                if len(word) >= 3:  # Only consider words with length 3 or more
                    self.words.add(word)
       
    def score(self, player2_words):
        """Calculate the score of the current player against another player.
        
        Args:
            player2_words (PlayerWords): Another PlayerWords object representing the other player's words.
        
        Returns:
            int: The score of the current player against the other player.
        """
        common_words = self.words.intersection(player2_words.words)
        total_score = sum(len(word) - 2 for word in common_words)
        return total_score

def main(wordfile1, wordfile2):
    """Calculate the team score based on words found by two players.
    
    Args:
        wordfile1 (str): Path to a text file containing words found by player 1.
        wordfile2 (str): Path to a text file containing words found by player 2.
        
    Side effects:
        Prints the team's score
    
    """
    player1_words = PlayerWords(wordfile1)
    player2_words = PlayerWords(wordfile2)
    team_score = player1_words.score(player2_words)
    print("Team score:", team_score)

def parse_args(arglist):
    """Parse command line arguments.
    
    Args:
        arglist (list of str): Arguments from the command line.
    
    Returns:
        namespace: The parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("wordfile1", help="file containing player 1's words")
    parser.add_argument("wordfile2", help="file containing player 2's words")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.wordfile1, args.wordfile2)
