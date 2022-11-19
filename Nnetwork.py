import numpy as np
from math import exp
from random import randint, seed, shuffle

def reverser(x): # thx to Assasine03#9403 for fixing his own code
    tab = []
    for i in range(len(x)):
        tab.append(x[len(x)-i-1])
    return tab

class Nnetwork():
    def sigmoid(self, x):     # function taken from unwind in https://stackoverflow.com/questions/3985619/how-to-__calculate-a-logistic-sigmoid-function-in-python
        return 1 / (1 + exp(-x))

    def dsigmoid(self, x):
        x = self.sigmoid(x) * (1 - self.sigmoid(x))
        return x

    # for init arguement: rbias, rweight

    def zeros_like_network(self):
        weight = []
        bias = []
        for i in range(len(self.__weights)):
            weight.append(np.zeros_like(self.__weights[i]))
            bias.append(np.zeros_like(self.__biases[i]))
        return weight, bias

    def build(self, layers):
        # layers as list, with the entires representing the nodecount
        # layers[0] = inputlayer
        # r{bias/range} als list anzugeben
        self.__weights = []
        self.__biases = []

        self.__input_depth = layers[0]
        layers.pop(0)
        self.input = np.empty(self.__input_depth)

        for index,value in enumerate(layers):
            if index == 0:
                prev_layer = self.__input_depth
            else:
                prev_layer = layers[index - 1]

            layer = np.empty((prev_layer, value))
            biases =  np.empty(value)

            self.__weights.append(layer)
            self.__biases.append(biases)

    def randpopulate(self, rweight, rbias):
        for i, v in enumerate(self.__weights):
            for i2, k in enumerate(v):
                for i3, u in enumerate(k):
                    randonr = randint(rweight[0], rweight[1])
                    self.__weights[i][i2][i3] =  randonr
            
        for i, v in enumerate(self.__biases):
            for i2, u in enumerate(v):
                self.__biases[i][i2] = randint(rbias[0], rbias[1])

    def __calculate(self):
        result = self.input
        for index, value in enumerate(self.__weights): 
            result = result.dot(value * self.__biases[index])
            for i,v in enumerate(result):
                result[i] = self.sigmoid(v)
        return result

    def __calculate_steps(self):
        result = self.input
        steps = []
        for index, value in enumerate(self.__weights): 
            result = result.dot(value * self.__biases[index])
            for i,v in enumerate(result):
                result[i] = self.sigmoid(v)
            steps.append(result)
        return steps

    def __apply_ajustment(self, w, b, l=1):
        for i in range(len(w)):
            self.__weights[i] = -l * w[i]
            self.__biases[i] = -l * b[i]

    def __backprop(self, train_input, train_out): # thx to 0zomi#7337 and my physics teacher for help
        self.input = train_input
        restults = self.__calculate_steps()
        restults.insert(0, self.input)
        want = train_out
        dbias = []
        dweight = []

        for i1,v1 in enumerate(reversed(restults)): # thx to Assasine03#9403 for rubberducking
            i1_reversed = len(restults) - i1 - 1
            if not i1_reversed == 0:
                new_want = np.zeros_like(restults[i1_reversed - 1])
                karl_bias = np.zeros_like(self.__biases[i1_reversed - 1])
                karl_weight = np.zeros_like(self.__weights[i1_reversed - 1])
            else:
                continue

            for i2 in range(len(v1) - 1):
                z = self.dsigmoid(v1[i2])
                c = 2 * (want[i2] - z)
                # bias calc
                karl_bias[i2] = z * c
                for i3 in range(len(karl_weight[i2]) - 1):
                    # weight calc
                    karl_weight[i2][i3] = v1[i3] * z * c
                    # a l-1 calc
                    if not i1_reversed == 1:
                        aL = self.__weights[i1_reversed - 1][i2][i3] * c * z
                        new_want[i2] += aL
            want = new_want
            dbias.append(karl_bias)
            dweight.append(karl_weight)
        return reverser(dweight), reverser(dbias)

    def __avg_cost(self, train_in, train_out):
        dweight, dbias = self.zeros_like_network()

        for i in range(len(train_in)):
            karl_weight, karl_bias = self.__backprop(train_in[i], train_out[i])
            for i2 in range(len(dweight)):
                dweight[i2] += karl_weight[i2]
                dbias[i2] += karl_bias[i2]

        return dweight, dbias

    def learn(self, data_in, data_out, batch_no, lrate):
        shuffler = list(zip(data_in, data_out))
        shuffle(shuffler)
        data_in, data_out = zip(*shuffler)
        AdjustmentW, AdjustmentB = self.zeros_like_network()
        batch_size = int(len(data_in)/batch_no - 1)
        print("--starting learning process--")
        print(f"  dataset lenght: {len(data_in)}")
        print(f"  batch size:{batch_size} | batch count: {batch_no}")
        for i in range(batch_no):
            print(f">>start set No. {i}") 
            karl_data_in = []
            karl_data_out = []
            for i2 in range(batch_size):
                karl_data_in.append(data_in[i2+i*batch_size])
                karl_data_out.append(data_out[i2+i*batch_size])
            localAdjustmentW, localAdjustmentB = self.__avg_cost(karl_data_in, karl_data_out)
            print("  calculated adjustment")
            for i2 in range(len(AdjustmentW)):
                AdjustmentW[i2] += localAdjustmentW[i2]
                AdjustmentB[i2] += localAdjustmentB[i2]
            self.__apply_ajustment(AdjustmentW, AdjustmentB, lrate)
            print(f">>finished set No.{i}")
        
    def get_result(self, input):
        self.input = input
        return self.__calculate()

    def __str__(self):
        string = f"------inputvector-------\n{self.input}"

        for i in range(len(self.__biases)):
            string += f"\n------weightmatrix {i}----\n"
            string += str(self.__weights[i])
            string += f"\n------biasvector {i}------\n"
            string += str(self.__biases[i])

        return string
