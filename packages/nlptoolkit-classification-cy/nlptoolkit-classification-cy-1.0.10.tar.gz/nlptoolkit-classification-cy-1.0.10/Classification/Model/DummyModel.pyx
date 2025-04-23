from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class DummyModel(Model):

    cpdef constructor1(self, InstanceList trainSet):
        """
        Constructor which sets the distribution using the given InstanceList.

        PARAMETERS
        ----------
        trainSet : InstanceList
            InstanceList which is used to get the class distribution.
        """
        self.distribution = trainSet.classDistribution()

    cpdef constructor2(self, str fileName):
        """
        Loads a dummy model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        cdef int size, i, count, j
        cdef str line
        cdef list items
        inputFile = open(fileName, mode='r', encoding='utf-8')
        self.distribution = Model.loadClassDistribution(inputFile)
        inputFile.close()

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input and returns the entry of distribution which has the maximum
        value.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The entry of distribution which has the maximum value.
        """
        cdef list possible_class_labels
        if isinstance(instance, CompositeInstance):
            possible_class_labels = instance.getPossibleClassLabels()
            return self.distribution.getMaxItemIncludeTheseOnly(possible_class_labels)
        else:
            return self.distribution.getMaxItem()

    cpdef dict predictProbability(self, Instance instance):
        """
        Calculates the posterior probability distribution for the given instance according to dummy model.
        :param instance: Instance for which posterior probability distribution is calculated.
        :return: Posterior probability distribution for the given instance.
        """
        return self.distribution.getProbabilityDistribution()

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for the dummy classifier. Actually dummy classifier returns the maximum occurring class in
        the training data, there is no training.

        PARAMETERS
        ----------
        trainSet: InstanceList
            Training data given to the algorithm.
        parameters: Parameter
            Parameter of the Dummy algorithm.
        """
        self.constructor1(trainSet)

    cpdef loadModel(self, str fileName):
        """
        Loads the dummy model from an input file.
        :param fileName: File name of the dummy model.
        """
        self.constructor2(fileName)
