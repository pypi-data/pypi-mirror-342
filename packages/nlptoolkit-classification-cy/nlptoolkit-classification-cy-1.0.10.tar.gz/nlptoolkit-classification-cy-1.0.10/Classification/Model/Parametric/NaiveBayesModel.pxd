from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.InstanceList.Partition cimport Partition
from Classification.Parameter.Parameter cimport Parameter
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Instance.Instance cimport Instance
from Classification.Model.Parametric.GaussianModel cimport GaussianModel


cdef class NaiveBayesModel(GaussianModel):

    cdef dict __class_means
    cdef dict __class_deviations
    cdef dict __class_attribute_distributions

    cpdef initForContinuous(self, dict classMeans, dict classDeviations)
    cpdef initForDiscrete(self, dict classAttributeDistributions)
    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef double __logLikelihoodContinuous(self, str classLabel, Instance instance)
    cpdef double __logLikelihoodDiscrete(self, str classLabel, Instance instance)
    cpdef constructor1(self, DiscreteDistribution priorDistribution)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
    cpdef trainContinuousVersion(self, DiscreteDistribution priorDistribution, Partition classLists)
    cpdef trainDiscreteVersion(self, DiscreteDistribution priorDistribution, Partition classLists)
