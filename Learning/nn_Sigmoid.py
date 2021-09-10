import numpy as np
import warnings

warnings.filterwarnings("ignore")  # suppress warnings
import matplotlib.pyplot as plt


class NeuralNet:
    """
    A two layer neural network
    """

    def __init__(self, layers=[13, 8, 1], learning_rate=0.001, iterations=100):
        self.params = {}
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.loss = []
        self.sample_size = None
        self.layers = layers
        self.X = None
        self.y = None

    def init_weights(self):
        """
        Randomize Weights
        """
        np.random.seed(1)  # Seed the random number generator
        self.params["W1"] = np.random.randn(self.layers[0], self.layers[1])
        self.params["b1"] = np.random.randn(
            self.layers[1],
        )
        self.params["W2"] = np.random.randn(self.layers[1], self.layers[2])
        self.params["b2"] = np.random.randn(
            self.layers[2],
        )

    def relu(self, Z):
        """
        Turns negative numbers into 0
        """
        return np.maximum(0, Z)

    def dRelu(self, x):
        """
        Derivative of reLU
        """
        x[x <= 0] = 0
        x[x > 0] = 1
        return x

    def eta(self, x):
        ETA = 0.0000000001
        return np.maximum(x, ETA)

    def sigmoid(self, Z):
        """
        The sigmoid function takes in real numbers in any range and
        squashes it to a real-valued output between 0 and 1.
        """
        return 1 / (1 + np.exp(-Z))

    def entropy_loss(self, y, yhat):
        """
        Loss Function
        """
        nsample = len(y)
        yhat_inv = 1.0 - yhat
        y_inv = 1.0 - y
        yhat = self.eta(yhat)  ## clips value to avoid NaNs in log
        yhat_inv = self.eta(yhat_inv)
        loss = (
            -1
            / nsample
            * (
                np.sum(
                    np.multiply(np.log(yhat), y)
                    + np.multiply((y_inv), np.log(yhat_inv))
                )
            )
        )
        return loss

    def forward_propagation(self):
        """
        Performs the forward propagation
        """

        Z1 = self.X.dot(self.params["W1"]) + self.params["b1"]
        A1 = self.relu(Z1)
        Z2 = A1.dot(self.params["W2"]) + self.params["b2"]
        yhat = self.sigmoid(Z2)
        loss = self.entropy_loss(self.y, yhat)

        # save calculated parameters
        self.params["Z1"] = Z1
        self.params["Z2"] = Z2
        self.params["A1"] = A1

        return yhat, loss

    def back_propagation(self, yhat):
        """
        Computes the derivatives and update weights and bias according.
        """
        y_inv = 1 - self.y
        yhat_inv = 1 - yhat

        dl_wrt_yhat = np.divide(y_inv, self.eta(yhat_inv)) - np.divide(
            self.y, self.eta(yhat)
        )
        dl_wrt_sig = yhat * (yhat_inv)
        dl_wrt_z2 = dl_wrt_yhat * dl_wrt_sig

        dl_wrt_A1 = dl_wrt_z2.dot(self.params["W2"].T)
        dl_wrt_w2 = self.params["A1"].T.dot(dl_wrt_z2)
        dl_wrt_b2 = np.sum(dl_wrt_z2, axis=0, keepdims=True)

        dl_wrt_z1 = dl_wrt_A1 * self.dRelu(self.params["Z1"])
        dl_wrt_w1 = self.X.T.dot(dl_wrt_z1)
        dl_wrt_b1 = np.sum(dl_wrt_z1, axis=0, keepdims=True)

        # update the weights and bias
        self.params["W1"] = self.params["W1"] - self.learning_rate * dl_wrt_w1
        self.params["W2"] = self.params["W2"] - self.learning_rate * dl_wrt_w2
        self.params["b1"] = self.params["b1"] - self.learning_rate * dl_wrt_b1
        self.params["b2"] = self.params["b2"] - self.learning_rate * dl_wrt_b2

    def fit(self, X, y):
        """
        Trains the neural network using the specified data and labels
        """
        self.X = X
        self.y = y
        self.init_weights()  # initialize weights and bias

        for i in range(self.iterations):
            yhat, loss = self.forward_propagation()
            self.back_propagation(yhat)
            self.loss.append(loss)

    def predict(self, X):
        """
        Predicts on a test data
        """
        Z1 = X.dot(self.params["W1"]) + self.params["b1"]
        A1 = self.relu(Z1)
        Z2 = A1.dot(self.params["W2"]) + self.params["b2"]
        pred = self.sigmoid(Z2)
        return np.round(pred)

    def acc(self, y, yhat):
        """
        Calculates the accutacy between the predicted valuea and the truth labels
        """
        acc = int(sum(y == yhat) / len(y) * 100)
        return acc

    def plot_loss(self):
        """
        Plots the loss curve
        """
        plt.plot(self.loss)
        plt.xlabel("Iteration")
        plt.ylabel("logloss")
        plt.title("Loss curve for training")
        plt.show()


nn = NeuralNet()  # create the NN model
