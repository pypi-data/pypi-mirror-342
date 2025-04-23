from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree

cdef class TreeEnsembleModel(Model):

    cpdef constructor1(self, list forest):
        """
        A constructor which sets the list of DecisionTree with given input.

        PARAMETERS
        ----------
        forest list
            A list of DecisionTrees.
        """
        self.__forest = forest

    cpdef constructor2(self, str fileName):
        """
        Loads a tree ensemble model such as Random Forest model or Bagging model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        cdef int number_of_trees, i
        inputFile = open(fileName, mode='r', encoding='utf-8')
        number_of_trees = int(inputFile.readline().strip())
        self.__forest = list()
        for i in range(number_of_trees):
            self.__forest.append(DecisionTree(DecisionNode(inputFile)))
        inputFile.close()

    def __init__(self, forest: object = None):
        if isinstance(forest, list):
            self.constructor1(forest)
        elif isinstance(forest, str):
            self.constructor2(forest)

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input and loops through the list of DecisionTrees.
        Makes prediction for the items of that ArrayList and returns the maximum item of that ArrayList.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The maximum prediction of a given Instance.
        """
        cdef DiscreteDistribution distribution
        cdef Model tree
        distribution = DiscreteDistribution()
        for tree in self.__forest:
            distribution.addItem(tree.predict(instance))
        return distribution.getMaxItem()

    cpdef dict predictProbability(self, Instance instance):
        """
        Calculates the posterior probability distribution for the given instance according to ensemble tree model.
        :param instance: Instance for which posterior probability distribution is calculated.
        :return: Posterior probability distribution for the given instance.
        """
        distribution = DiscreteDistribution()
        for tree in self.__forest:
            distribution.addItem(tree.predict(instance))
        return distribution.getProbabilityDistribution()
