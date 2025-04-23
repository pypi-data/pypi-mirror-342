import copy

from Classification.InstanceList.Partition cimport Partition
from Classification.Parameter.MultiLayerPerceptronParameter cimport MultiLayerPerceptronParameter
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance
from Classification.InstanceList.InstanceList cimport InstanceList
from Math.Vector cimport Vector

from Classification.Parameter.ActivationFunction import ActivationFunction

cdef class MultiLayerPerceptronModel(LinearPerceptronModel):
    cpdef __allocateWeights(self,
                            int H,
                            int seed):
        """
        The allocateWeights method allocates layers' weights of Matrix W and V.

        PARAMETERS
        ----------
        H : int
            Integer value for weights.
        """
        self.W = self.allocateLayerWeights(row=H,
                                           column=self.d + 1,
                                           seed=seed)
        self.__V = self.allocateLayerWeights(row=self.K,
                                             column=H + 1,
                                             seed=seed)

    cpdef constructor4(self,
                       InstanceList trainSet,
                       InstanceList validationSet,
                       MultiLayerPerceptronParameter parameters):
        """
        A constructor that takes InstanceLists as trainsSet and validationSet. It  sets the NeuralNetworkModel nodes
        with given InstanceList then creates an input vector by using given trainSet and finds error. Via the
        validationSet it finds the classification performance and reassigns the allocated weight Matrix with the matrix
        that has the best accuracy and the Matrix V with the best Vector input.

        PARAMETERS
        ----------
        trainSet : InstanceList
            InstanceList that is used to train.
        validationSet : InstanceList
            InstanceList that is used to validate.
        parameters : MultiLayerPerceptronParameter
            Multi layer perceptron parameters; seed, learningRate, etaDecrease, crossValidationRatio, epoch,
            hiddenNodes.
        """
        cdef Matrix best_w, best_v, delta_v, delta_w
        cdef ClassificationPerformance best_classification_performance, current_classification_performance
        cdef int epoch, i, j
        cdef double learning_rate
        cdef Vector hidden, hidden_biased, rMinusY, one_minus_hidden, tmp_h, tmp_hidden
        self.class_labels = trainSet.getDistinctClassLabels()
        self.K = len(self.class_labels)
        self.d = trainSet.get(0).continuousAttributeSize()
        self.__activation_function = parameters.getActivationFunction()
        self.__allocateWeights(parameters.getHiddenNodes(), parameters.getSeed())
        best_w = copy.deepcopy(self.W)
        best_v = copy.deepcopy(self.__V)
        best_classification_performance = ClassificationPerformance(0.0)
        epoch = parameters.getEpoch()
        learning_rate = parameters.getLearningRate()
        for i in range(epoch):
            trainSet.shuffle(parameters.getSeed())
            for j in range(trainSet.size()):
                self.createInputVector(trainSet.get(j))
                hidden = self.calculateHidden(self.x, self.W, self.__activation_function)
                hidden_biased = hidden.biased()
                rMinusY = self.calculateRMinusY(trainSet.get(j), hidden_biased, self.__V)
                delta_v = Matrix(rMinusY, hidden_biased)
                tmp_h = self.__V.multiplyWithVectorFromLeft(rMinusY)
                tmp_h.remove(0)
                if self.__activation_function == ActivationFunction.SIGMOID:
                    one_minus_hidden = self.calculateOneMinusHidden(hidden)
                    activation_derivative = one_minus_hidden.elementProduct(hidden)
                elif self.__activation_function == ActivationFunction.TANH:
                    one = Vector(hidden.size(), 1.0)
                    hidden.tanh()
                    activation_derivative = one.difference(hidden.elementProduct(hidden))
                elif self.__activation_function == ActivationFunction.RELU:
                    hidden.reluDerivative()
                    activation_derivative = hidden
                tmp_hidden = tmp_h.elementProduct(activation_derivative)
                delta_w = Matrix(tmp_hidden, self.x)
                delta_v.multiplyWithConstant(learning_rate)
                self.__V.add(delta_v)
                delta_w.multiplyWithConstant(learning_rate)
                self.W.add(delta_w)
            current_classification_performance = self.testClassifier(validationSet)
            if current_classification_performance.getAccuracy() > best_classification_performance.getAccuracy():
                bestClassificationPerformance = current_classification_performance
                best_w = copy.deepcopy(self.W)
                best_v = copy.deepcopy(self.__V)
            learning_rate *= parameters.getEtaDecrease()
        self.W = best_w
        self.__V = best_v

    cpdef constructor3(self, str fileName):
        """
        Loads a multi-layer perceptron model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        inputFile = open(fileName, mode='r', encoding='utf-8')
        self.loadClassLabels(inputFile)
        self.W = self.loadMatrix(inputFile)
        self.__V = self.loadMatrix(inputFile)
        self.__activation_function = self.loadActivationFunction(inputFile)
        inputFile.close()

    cpdef calculateOutput(self):
        """
        The calculateOutput method calculates the forward single hidden layer by using Matrices W and V.
        """
        self.calculateForwardSingleHiddenLayer(W=self.W,
                                               V=self.__V,
                                               activationFunction=self.__activation_function)

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for the multilayer perceptron algorithm. 20 percent of the data is separated as
        cross-validation data used for selecting the best weights. 80 percent of the data is used for training the
        multilayer perceptron with gradient descent.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        parameters : MultiLayerPerceptronParameter
            Parameters of the multilayer perceptron.
        """
        cdef Partition partition
        partition = Partition(instanceList=trainSet,
                              ratio=parameters.getCrossValidationRatio(),
                              seed=parameters.getSeed(),
                              stratified=True)
        self.constructor2(trainSet=partition.get(1),
                          validationSet=partition.get(0),
                          parameters=parameters)

    cpdef loadModel(self, str fileName):
        """
        Loads the multi-layer perceptron model from an input file.
        :param fileName: File name of the multi-layer perceptron model.
        """
        self.constructor3(fileName)
