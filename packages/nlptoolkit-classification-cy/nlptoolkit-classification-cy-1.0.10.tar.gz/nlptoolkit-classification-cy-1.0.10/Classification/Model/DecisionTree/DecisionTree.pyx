from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.InstanceList.Partition cimport Partition
from Classification.Performance.ClassificationPerformance cimport ClassificationPerformance


cdef class DecisionTree(ValidatedModel):

    cpdef constructor1(self, DecisionNode root):
        """
        Constructor that sets root node of the decision tree.

        PARAMETERS
        ----------
        root : DecisionNode
            DecisionNode type input.
        """
        self.__root = root

    cpdef constructor2(self, str fileName):
        cdef object inputFile
        inputFile = open(fileName, mode='r', encoding='utf-8')
        self.__root = DecisionNode(inputFile)
        inputFile.close()

    def __init__(self, root: object = None):
        if isinstance(root, DecisionNode):
            self.constructor1(root)
        elif isinstance(root, str):
            self.constructor2(root)

    cpdef str predict(self, Instance instance):
        """
        The predict method  performs prediction on the root node of given instance, and if it is null, it returns the
        possible class labels. Otherwise it returns the returned class labels.

        PARAMETERS
        ----------
        instance : Instance
            Instance make prediction.

        RETURNS
        -------
        str
            Possible class labels.
        """
        cdef str predicted_class
        predicted_class = self.__root.predict(instance)
        if predicted_class is None and isinstance(instance, CompositeInstance):
            predicted_class = instance.getPossibleClassLabels()
        return predicted_class

    cpdef dict predictProbability(self, Instance instance):
        return self.__root.predictProbabilityDistribution(instance)

    cpdef pruneNode(self,
                    DecisionNode node,
                    InstanceList pruneSet):
        """
        The prune method takes a DecisionNode and an InstanceList as inputs. It checks the classification performance
        of given InstanceList before pruning, i.e making a node leaf, and after pruning. If the after performance is
        better than the before performance it prune the given InstanceList from the tree.

        PARAMETERS
        ----------
        node : DecisionNode
            DecisionNode that will be pruned if conditions hold.
        pruneSet : InstanceList
            Small subset of tree that will be removed from tree.
        """
        cdef ClassificationPerformance before, after
        if node.leaf:
            return
        before = self.testClassifier(pruneSet)
        node.leaf = True
        after = self.testClassifier(pruneSet)
        if after.getAccuracy() < before.getAccuracy():
            node.leaf = False
            for child in node.children:
                self.pruneNode(child, pruneSet)

    cpdef prune(self, InstanceList pruneSet):
        """
        The prune method takes an InstanceList and  performs pruning to the root node.

        PARAMETERS
        ----------
        pruneSet : InstanceList
            InstanceList to perform pruning.
        """
        self.pruneNode(self.__root, pruneSet)

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for C4.5 univariate decision tree classifier. 20 percent of the data are left aside for
        pruning 80 percent of the data is used for constructing the tree.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters: C45Parameter
            Parameter of the C45 algorithm.
        """
        cdef Partition partition
        cdef DecisionTree tree
        if parameters.isPrune():
            partition = Partition(instanceList=trainSet,
                                  ratio=parameters.getCrossValidationRatio(),
                                  seed=parameters.getSeed(),
                                  stratified=True)
            self.constructor1(DecisionNode(partition.get(1)))
            self.prune(partition.get(0))
        else:
            self.constructor1(DecisionNode(trainSet))

    cpdef loadModel(self, str fileName):
        """
        Loads the decision tree model from an input file.
        :param fileName: File name of the decision tree model.
        """
        self.constructor2(fileName)
