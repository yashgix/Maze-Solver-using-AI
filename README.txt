Implemented a basic Q-learning algorithm to learn a policy of behaviour for a simple grid world. Using q learn we had to make the player reach the good location while avoiding the bad location.
First, we begin by filling in the code to represent the Q-table, that is, the table that will represent Q(S,A). The table includes a Q value for each state-action pair and the implementation of the related helper functions (get_q(), get_q_row(), set_q()) performs these actions in whatever way is appropriate.
Then, the learning episode starts at a random state in the environment, selects a random legal action, and proceeds to update the Q-table according to the equation.
After running a single episode, we implement the __str__() function that converts the Q-table to a string, to allow for printing of the table values and then we finally proceed to implement the learn() function that runs multiple episodes.

>> sh run.sh learn