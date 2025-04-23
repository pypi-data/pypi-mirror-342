from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Instance.Instance cimport Instance
from Classification.Model.Parametric.LdaModel cimport LdaModel

cdef class QdaModel(LdaModel):

    cdef dict __W

    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef constructor3(self,
                     DiscreteDistribution priorDistribution,
                     dict W,
                     dict w,
                     dict w0)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
