#execute this to build the network
#replace with directory file
directory = "PATH/.pickle"

from Nnetwork import Nnetwork
import pickle
snake = Nnetwork()
snake.build([3,4,4,4])
snake.randpopulate((-3,3), (-3,3))

print("Build Network")
print(snake)

with open(directory, "wb") as outfile:
    pickle.dump(snake, outfile)