# Agent Based Passenger Transport Model: case study of France

We will focus in this paper on the application of agent based modelling (ABM) methods for transportation of passengers and their choice of transport means. To create a good transport based model, we will focus on existing data so as to try to reproduce the conditions in which travelling is done today and deduce people's motivation for this. The main goal will be to assess the complementary existence of two important transport method: train and airplane. A second advantage of modelling in general, and ABM models in particular, is that in the case of transport infrastructure, investments plans need to be thoroughly tested before being implemented.

Agents are households with certain individual characteristics that may impact the simulation.
The goal is to have a representative population based on their characteristics. The database used to achieve this was the Enquête Nationale Transports et Déplacements (2007 - 2008), which gave a broad overview on the habits and preferences of people living in France when it comes to transport. 
There are 2651 individuals in the database representative of the French population living in the departments where an airport is existing. 
The sample population from the database has the following distribution:

![Population](https://github.com/JovanP1/Passenger-Transport-Model-for-France/blob/main/results/Population_pond.png)

Most notable information that were extracted from the ENTD are the department of residence of the agent, his income group (in a scale of 1-10) and whether time is a priority when the person travels or not.
This constitutes the characteristics of the agent that will be used in the decision model.
Let us describe the initial population characteristics. The income distribution of the survey population is:

![Population income](https://github.com/JovanP1/Passenger-Transport-Model-for-France/blob/main/results/Population_income.png)

A simulation included a certain evolution of environment conditions: the first scenario changed prices and the second changed speed of trains.

Scenario 1 showed that agents will change their behaviour with a different relative price, to choose the more cheaper mode of transport, but that this evolution is not linear and is probably possible only up to a certain level. Above this level, other factors are prevalent and action on those should be considered.

![Scenario 1](https://github.com/JovanP1/Passenger-Transport-Model-for-France/blob/main/results/scenario_1.png)

Scenario 2 showed that time is the most important innovation by which more people would tend to use trains, but that this is a long term investment as it would take some time for agents to acknowledge the fact that trains are not as time-consuming as planes.

![Scenario 2](https://github.com/JovanP1/Passenger-Transport-Model-for-France/blob/main/results/scenario_2.png)
