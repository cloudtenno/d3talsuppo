This script is adapted from https://github.com/chengxi600/RLStuff/blob/master/Genetic%20Algorithms/8Queens_GA.ipynb

To run the script, you need python 3 and above, as well as scipy library. Alternatively, you can just run the exe file which contains all the necessary library (Sorry if you are using MacOS, please run the script using python, as I do not have a Mac Computer [Poor Kids No money to buy Apple Product])

To setup the environment please run the command: 

**pip install scipy**

Modification made are detail below:

- When first initializing the population, added code to prevent duplicating sequence from appearing in the population (No queens on the same column)
- When mutation occurs, no more adding random sequence to the population, this is done to prevent duplicating queen on the same column
- Added refresh feature to prevent the algorithm from falling into local point
    - Since initialization plays a huge factor in deriving the answer, reinitialzing the population after a fix epoch is needed to prevent stuck at a local maximum point and not able to find the final answer
- Added feature to allow user to dynamically change the number of queens, population size, mutation rate, etc.

Result will be save as a text file named ***Lu_Xinpei_EE6227_Assignment_3_Result.txt***. This file is located at the same directory as the program.

Lastly, if you wish to stop the program at any time, press Ctrl + C to stop the program!