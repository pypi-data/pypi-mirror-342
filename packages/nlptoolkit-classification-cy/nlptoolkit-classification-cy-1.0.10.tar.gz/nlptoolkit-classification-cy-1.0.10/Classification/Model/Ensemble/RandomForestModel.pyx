from Sampling.Bootstrap cimport Bootstrap

from Classification.Model.DecisionTree.DecisionNode cimport DecisionNode
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree

cdef class RandomForestModel(TreeEnsembleModel):

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for random forest classifier. Basically the algorithm creates K distinct decision trees from
        K bootstrap samples of the original training set.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        parameters : RandomForestParameter
            Parameters of the bagging trees algorithm. ensembleSize returns the number of trees in the random forest.
        """
        cdef int forest_size, i
        cdef list forest
        cdef Bootstrap bootstrap
        cdef DecisionTree tree
        forest_size = parameters.getEnsembleSize()
        forest = []
        for i in range(forest_size):
            bootstrap = trainSet.bootstrap(i)
            tree = DecisionTree(DecisionNode(data=InstanceList(bootstrap.getSample()),
                                             parameter=parameters,
                                             isStump=False))
            forest.append(tree)
        self.constructor1(forest)

    cpdef loadModel(self, str fileName):
        """
        Loads the random forest model from an input file.
        :param fileName: File name of the random forest model.
        """
        self.constructor2(fileName)
