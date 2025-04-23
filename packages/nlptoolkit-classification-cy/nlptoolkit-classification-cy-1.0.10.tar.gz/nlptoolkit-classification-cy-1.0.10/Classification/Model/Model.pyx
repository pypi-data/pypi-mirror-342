from io import TextIOWrapper

from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Performance.ConfusionMatrix cimport ConfusionMatrix
from Classification.Performance.DetailedClassificationPerformance cimport DetailedClassificationPerformance
from Math.DiscreteDistribution cimport DiscreteDistribution
from Math.Matrix cimport Matrix

cdef class Model(object):

    cpdef train(self,
              trainSet: InstanceList,
              parameters: Parameter):
        pass

    cpdef loadModel(self, fileName: str):
        pass

    cpdef str predict(self, Instance instance):
        """
         An abstract predict method that takes an Instance as an input.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The class label as a String.
        """
        pass

    cpdef dict predictProbability(self, Instance instance):
        pass

    cpdef Instance loadInstance(self, str line, list attributeTypes):
        cdef list items
        cdef Instance instance
        cdef int i
        items = line.split(",")
        instance = Instance(items[len(items) - 1])
        for i in range(len(items) - 1):
            if attributeTypes[i] == "DISCRETE":
                instance.addDiscreteAttribute(items[i])
            elif attributeTypes[i] == "CONTINUOUS":
                instance.addContinuousAttribute(float(items[i]))
        return instance

    cpdef Matrix loadMatrix(self, object inputFile):
        cdef Matrix matrix
        cdef int j, k
        cdef str line
        cdef list items
        items = inputFile.readline().strip().split(" ")
        matrix = Matrix(int(items[0]), int(items[1]))
        for j in range(matrix.getRow()):
            line = inputFile.readline().strip()
            items = line.split(" ")
            for k in range(matrix.getColumn()):
                matrix.setValue(j, k, float(items[k]))
        return matrix

    @staticmethod
    def loadClassDistribution(inputFile: TextIOWrapper) -> DiscreteDistribution:
        distribution = DiscreteDistribution()
        size = int(inputFile.readline().strip())
        for i in range(size):
            line = inputFile.readline().strip()
            items = line.split(" ")
            count = int(items[1])
            for j in range(count):
                distribution.addItem(items[0])
        return distribution

    cpdef InstanceList loadInstanceList(self, object inputFile):
        cdef list types
        cdef int instance_count, i
        cdef InstanceList instance_list
        types = inputFile.readline().strip().split(" ")
        instance_count = int(inputFile.readline().strip())
        instance_list = InstanceList()
        for i in range(instance_count):
            instance_list.add(self.loadInstance(inputFile.readline().strip(), types))
        return instance_list

    cpdef bint discreteCheck(self, Instance instance):
        """
        Checks given instance's attribute and returns true if it is a discrete indexed attribute, false otherwise.

        PARAMETERS
        ----------
        instance Instance to check.

        RETURNS
        -------
        bool
            True if instance is a discrete indexed attribute, false otherwise.
        """
        cdef int i
        for i in range(instance.attributeSize()):
            if isinstance(instance.getAttribute(i), DiscreteAttribute) and not isinstance(instance.getAttribute(i),
                                                                                          DiscreteIndexedAttribute):
                return False
        return True

    cpdef Performance test(self, InstanceList testSet):
        """
        TestClassification an instance list with the current model.

        PARAMETERS
        ----------
        testSet : InstaceList
            Test data (list of instances) to be tested.

        RETURNS
        -------
        Performance
            The accuracy (and error) of the model as an instance of Performance class.
        """
        cdef list class_labels
        cdef ConfusionMatrix confusion
        cdef int i
        cdef Instance instance
        class_labels = testSet.getUnionOfPossibleClassLabels()
        confusion = ConfusionMatrix(class_labels)
        for i in range(testSet.size()):
            instance = testSet.get(i)
            confusion.classify(instance.getClassLabel(), self.predict(instance))
        return DetailedClassificationPerformance(confusion)

    cpdef Performance singleRun(self,
                                Parameter parameter,
                                InstanceList trainSet,
                                InstanceList testSet):
        """
        Runs current classifier with the given train and test data.

        PARAMETERS
        ----------
        parameter : Parameter
            Parameter of the classifier to be trained.
        trainSet : InstanceList
            Training data to be used in training the classifier.
        testSet : InstanceList
            Test data to be tested after training the model.

        RETURNS
        -------
        Performance
            The accuracy (and error) of the trained model as an instance of Performance class.
        """
        self.train(trainSet, parameter)
        return self.test(testSet)
