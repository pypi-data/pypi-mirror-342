from functools import cmp_to_key

from Classification.DistanceMetric.EuclidianDistance cimport EuclidianDistance
from Classification.Model.NonParametric.KnnInstance cimport KnnInstance
from Classification.Instance.CompositeInstance cimport CompositeInstance

cdef class KnnModel(Model):
    cpdef constructor1(self,
                       InstanceList data,
                       int k,
                       DistanceMetric distanceMetric):
        """
        Constructor that sets the data InstanceList, k value and the DistanceMetric.

        PARAMETERS
        ----------
        data : InstanceList
            InstanceList input.
        k : int
            K value.
        distanceMetric : DistanceMetric
            DistanceMetric input.
        """
        self.__data = data
        self.__k = k
        self.__distance_metric = distanceMetric

    cpdef constructor2(self, str fileName):
        """
        Loads a K-nearest neighbor model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        self.__distance_metric = EuclidianDistance()
        inputFile = open(fileName, 'r')
        self.__k = int(inputFile.readline().strip())
        self.__data = self.loadInstanceList(inputFile)
        inputFile.close()

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as an input and finds the nearest neighbors of given instance. Then
        it returns the first possible class label as the predicted class.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The first possible class label as the predicted class.
        """
        cdef InstanceList nearest_neighbors
        cdef str predicted_class
        nearest_neighbors = self.nearestNeighbors(instance)
        if isinstance(instance, CompositeInstance) and nearest_neighbors.size() == 0:
            predicted_class = instance.getPossibleClassLabels()[0]
        else:
            predicted_class = InstanceList.getMaximum(nearest_neighbors.getClassLabels())
        return predicted_class

    cpdef dict predictProbability(self, Instance instance):
        """
        Calculates the posterior probability distribution for the given instance according to K-means model.
        :param instance: Instance for which posterior probability distribution is calculated.
        :return: Posterior probability distribution for the given instance.
        """
        cdef InstanceList nearest_neighbors
        nearest_neighbors = self.nearestNeighbors(instance)
        return nearest_neighbors.classDistribution().getProbabilityDistribution()

    def makeComparator(self):
        def compare(instanceA: KnnInstance, instanceB: KnnInstance):
            if instanceA.distance < instanceB.distance:
                return -1
            elif instanceA.distance > instanceB.distance:
                return 1
            else:
                return 0
        return compare

    cpdef InstanceList nearestNeighbors(self, Instance instance):
        """
        The nearestNeighbors method takes an Instance as an input. First it gets the possible class labels, then loops
        through the data InstanceList and creates new list of KnnInstances and adds the corresponding data with
        the distance between data and given instance. After sorting this newly created list, it loops k times and
        returns the first k instances as an InstanceList.

        PARAMETERS
        ----------
        instance : Instance
            Instance to find nearest neighbors

        RETURNS
        -------
        InstanceList
            The first k instances which are nearest to the given instance as an InstanceList.
        """
        cdef InstanceList result
        cdef list instances, possible_class_labels
        cdef int i
        result = InstanceList()
        instances = []
        possible_class_labels = []
        if isinstance(instance, CompositeInstance):
            possible_class_labels = instance.getPossibleClassLabels()
        for i in range(self.__data.size()):
            if not isinstance(instance, CompositeInstance) or self.__data.get(
                    i).getClassLabel() in possible_class_labels:
                instances.append(KnnInstance(self.__data.get(i), self.__distance_metric.distance(self.__data.get(i),
                                                                                                 instance)))
        instances.sort(key=cmp_to_key(self.makeComparator()))
        for i in range(min(self.__k, len(instances))):
            result.add(instances[i].getInstance())
        return result

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for K-nearest neighbor classifier.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm.
        parameters : KnnParameter
            Parameters of the Knn algorithm.
        """
        self.constructor1(data=trainSet,
                          k=parameters.getK(),
                          distanceMetric=parameters.getDistanceMetric())

    cpdef loadModel(self, str fileName):
        """
        Loads the K-nearest neighbor model from an input file.
        :param fileName: File name of the K-nearest neighbor model.
        """
        self.constructor2(fileName)
