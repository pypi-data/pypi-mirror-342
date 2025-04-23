from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode

cdef class DecisionStump(DecisionTree):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for C4.5 Stump univariate decision tree classifier.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters: Parameter
            Parameter of the C45Stump algorithm.
        """
        self.constructor1(DecisionNode(data=trainSet, isStump=True))

    cpdef loadModel(self, str fileName):
        """
        Loads the decision tree model from an input file.
        :param fileName: File name of the decision tree model.
        """
        self.constructor2(fileName)
