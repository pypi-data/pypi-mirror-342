from Classification.InstanceList.Partition cimport Partition
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.DistanceMetric.EuclidianDistance cimport EuclidianDistance

cdef class KMeansModel(GaussianModel):
    cpdef constructor1(self,
                       DiscreteDistribution priorDistribution,
                       InstanceList classMeans,
                       DistanceMetric distanceMetric):
        """
        The constructor that sets the classMeans, priorDistribution and distanceMetric according to given inputs.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            DiscreteDistribution input.
        classMeans : InstanceList
            InstanceList of class means.
        distanceMetric : DistanceMetric
            DistanceMetric input.
        """
        self.__class_means = classMeans
        self.prior_distribution = priorDistribution
        self.__distance_metric = distanceMetric

    cpdef constructor2(self, str fileName):
        """
        Loads a K-means model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        self.__distance_metric = EuclidianDistance()
        inputFile = open(fileName, 'r')
        self.loadPriorDistribution(inputFile)
        self.__class_means = self.loadInstanceList(inputFile)
        inputFile.close()

    cpdef double calculateMetric(self, Instance instance, str Ci):
        """
        The calculateMetric method takes an {@link Instance} and a String as inputs. It loops through the class means,
        if the corresponding class label is same as the given String it returns the negated distance between given
        instance and the current item of class means. Otherwise it returns the smallest negative number.

        PARAMETERS
        ----------
        instance : Instance
            Instance input.
        Ci : str
            String input.

        RETURNS
        -------
        float
            The negated distance between given instance and the current item of class means.
        """
        cdef int i
        for i in range(self.__class_means.size()):
            if self.__class_means.get(i).getClassLabel() == Ci:
                return -self.__distance_metric.distance(instance, self.__class_means.get(i))
        return -1000000

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for K-Means classifier. K-Means finds the mean of each class for training.
        :param trainSet: Training data given to the algorithm.
        :param parameters: distance metric used to calculate the distance between two instances.
        """
        cdef DiscreteDistribution prior_distribution
        cdef InstanceList class_means
        cdef Partition class_lists
        cdef int i
        prior_distribution = trainSet.classDistribution()
        class_means = InstanceList()
        class_lists = Partition(trainSet)
        for i in range(class_lists.size()):
            class_means.add(class_lists.get(i).average())
        self.constructor1(priorDistribution=prior_distribution,
                          classMeans=class_means,
                          distanceMetric=parameters.getDistanceMetric())

    cpdef loadModel(self, str fileName):
        """
        Loads the K-means model from an input file.
        :param fileName: File name of the K-means model.
        """
        self.constructor2(fileName)
