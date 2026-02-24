
## Project Description

The project consisted in coding a version of the game Snake and then training a neural 
network to play the game using the library neat-python. 

The neat-python library implements the neat algorithm which stands for NeuroEvolution of 
Augmenting Topologies. Using this algorithm a population of neural networks is created, and 
each neural network control a snake and plays the game. A fitness function evaluates the 
performance of the snakes, and the next generation of neural 
networks is created by selecting the highest-performing snakes and creating copies 
of them with random variations. 

Unlike other algorithms involving neural network what changes over time is not just the 
weight and biases but the nodes and connections themselves (that is the topology of 
the neural network).

## Results 

There is some variability on how well the algorithm performs based on the initial generation 
of weights and biases. On a good run the highest fitness is around 50, which correspons to eating the food 50 times.
Below is an example of the highest scoring snake.
