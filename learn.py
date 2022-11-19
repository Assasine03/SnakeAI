#execute this to let the AI learn from produced data
#replace with directory file
directory = "PATH/.pickle"
directory2 = "PATH/.json"
# if you get in to math range problems play around a bit with those ->
badgeSize = 10
learningRate = 0.1

import pickle, json
import numpy as np

file = open(directory, "rb")
snake = pickle.load(file)

file.close()

with open(directory2) as json_file:
    data = json.load(json_file)

training_in = []
training_out =[]
for i in data["Data"]:
    try:
        training_in.append(np.array(i["InputData"]))
        training_out.append(np.array(i["WishData"]))
    except:
        continue

snake.learn(training_in,training_out,badgeSize,learningRate)

with open(directory, "wb") as outfile:
    pickle.dump(snake, outfile)

outfile.close()
print("-----------DONE----------")