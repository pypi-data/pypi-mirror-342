import math

from Math.Vector cimport Vector

from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Math.DiscreteDistribution cimport DiscreteDistribution


cdef class NaiveBayesModel(GaussianModel):

    cpdef constructor1(self, DiscreteDistribution priorDistribution):
        """
        A constructor that sets the priorDistribution.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            DiscreteDistribution input.
        """
        self.prior_distribution = priorDistribution

    cpdef constructor2(self, str fileName):
        """
        Loads a naive Bayes model from an input model file.
        :param fileName: Model file name.
        """
        cdef object inputFile
        cdef int size
        inputFile = open(fileName, mode='r', encoding='utf-8')
        size = self.loadPriorDistribution(inputFile)
        self.__class_means = self.loadVectors(inputFile, size)
        self.__class_deviations = self.loadVectors(inputFile, size)
        self.__class_attribute_distributions = None
        inputFile.close()

    cpdef initForContinuous(self,
                            dict classMeans,
                            dict classDeviations):
        """
        A constructor that sets the classMeans and classDeviations.

        PARAMETERS
        ----------
        classMeans : dict
            A dict of String and Vector.
        classDeviations : dict
            A dict of String and Vector.
        """
        self.__class_means = classMeans
        self.__class_deviations = classDeviations
        self.__class_attribute_distributions = None

    cpdef initForDiscrete(self, dict classAttributeDistributions):
        """
        A constructor that sets the priorDistribution and classAttributeDistributions.

        PARAMETERS
        ----------
        classAttributeDistributions : dict
            A dict of String and list of DiscreteDistributions.
        """
        self.__class_attribute_distributions = classAttributeDistributions

    cpdef double calculateMetric(self,
                                 Instance instance,
                                 str Ci):
        """
        The calculateMetric method takes an Instance and a String as inputs and it returns the log likelihood of
        these inputs.

        PARAMETERS
        ----------
        instance : Instance
            Instance input.
        Ci : str
            String input.

        RETURNS
        -------
        float
            The log likelihood of inputs.
        """
        if self.__class_attribute_distributions is None:
            return self.__logLikelihoodContinuous(Ci, instance)
        else:
            return self.__logLikelihoodDiscrete(Ci, instance)

    cpdef double __logLikelihoodContinuous(self,
                                           str classLabel,
                                           Instance instance):
        """
        The logLikelihoodContinuous method takes an Instance and a class label as inputs. First it gets the logarithm
        of given class label's probability via prior distribution as logLikelihood. Then it loops times of given
        instance attribute size, and accumulates the logLikelihood by calculating -0.5 * ((xi - mi) / si )** 2).

        PARAMETERS
        ----------
        classLabel : str
            String input class label.
        instance : Instance
            Instance input.

        RETURNS
        -------
        float
            The log likelihood of given class label and Instance.
        """
        cdef double log_likelihood, xi, mi, si
        cdef int i
        log_likelihood = math.log(self.prior_distribution.getProbability(classLabel))
        for i in range(instance.attributeSize()):
            xi = instance.getAttribute(i).getValue()
            mi = self.__class_means[classLabel].getValue(i)
            si = self.__class_deviations[classLabel].getValue(i)
            if si != 0:
                log_likelihood += -0.5 * math.pow((xi - mi) / si, 2)
        return log_likelihood

    cpdef double __logLikelihoodDiscrete(self,
                                         str classLabel,
                                         Instance instance):
        """
        The logLikelihoodDiscrete method takes an Instance and a class label as inputs. First it gets the logarithm
        of given class label's probability via prior distribution as logLikelihood and gets the class attribute
        distribution of given class label. Then it loops times of given instance attribute size, and accumulates the
        logLikelihood by calculating the logarithm of corresponding attribute distribution's smoothed probability by
        using laplace smoothing on xi.

        PARAMETERS
        ----------
        classLabel : str
            String input class label.
        instance : Instance
            Instance input.

        RETURNS
        -------
        float
            The log likelihood of given class label and Instance.
        """
        cdef double log_likelihood
        cdef list attribute_distributions
        cdef int i
        cdef str xi
        log_likelihood = math.log(self.prior_distribution.getProbability(classLabel))
        attribute_distributions = self.__class_attribute_distributions.get(classLabel)
        for i in range(instance.attributeSize()):
            xi = instance.getAttribute(i).getValue()
            log_likelihood += math.log(attribute_distributions[i].getProbabilityLaplaceSmoothing(xi))
        return log_likelihood

    cpdef trainContinuousVersion(self,
                                 DiscreteDistribution priorDistribution,
                                 Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a continuous data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict class_means, class_deviations
        cdef int i
        cdef str class_label
        cdef Vector average_vector, standard_deviation_vector
        class_means = {}
        class_deviations = {}
        for i in range(classLists.size()):
            class_label = classLists.get(i).getClassLabel()
            average_vector = classLists.get(i).average().toVector()
            class_means[class_label] = average_vector
            standard_deviation_vector = classLists.get(i).standardDeviation().toVector()
            class_deviations[class_label] = standard_deviation_vector
        self.constructor1(priorDistribution)
        self.initForContinuous(class_means, class_deviations)

    cpdef trainDiscreteVersion(self,
                               DiscreteDistribution priorDistribution,
                               Partition classLists):
        """
        Training algorithm for Naive Bayes algorithm with a discrete data set.

        PARAMETERS
        ----------
        priorDistribution : DiscreteDistribution
            Probability distribution of classes P(C_i)
        classLists : Partition
            Instances are divided into K lists, where each list contains only instances from a single class
        """
        cdef dict class_attribute_distributions
        cdef int i
        class_attribute_distributions = {}
        for i in range(classLists.size()):
            class_attribute_distributions[classLists.get(i).getClassLabel()] = \
                classLists.get(i).allAttributesDistribution()
        self.constructor1(priorDistribution)
        self.initForDiscrete(class_attribute_distributions)

    cpdef train(self,
                InstanceList trainSet,
                Parameter parameters):
        """
        Training algorithm for Naive Bayes algorithm. It basically calls trainContinuousVersion for continuous data
        sets, trainDiscreteVersion for discrete data sets.

        PARAMETERS
        ----------
        trainSet : InstanceList
            Training data given to the algorithm
        """
        cdef DiscreteDistribution prior_distribution
        cdef Partition class_lists
        prior_distribution = trainSet.classDistribution()
        class_lists = Partition(trainSet)
        if isinstance(class_lists.get(0).get(0).getAttribute(0), DiscreteAttribute):
            self.trainDiscreteVersion(prior_distribution, class_lists)
        else:
            self.trainContinuousVersion(prior_distribution, class_lists)

    cpdef loadModel(self, str fileName):
        """
        Loads the naive Bayes model from an input file.
        :param fileName: File name of the naive Bayes model.
        """
        self.constructor2(fileName)
