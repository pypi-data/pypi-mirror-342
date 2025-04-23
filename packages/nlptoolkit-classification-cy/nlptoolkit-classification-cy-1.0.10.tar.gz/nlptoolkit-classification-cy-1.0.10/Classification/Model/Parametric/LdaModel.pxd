from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Instance.Instance cimport Instance
from Classification.Model.Parametric.GaussianModel cimport GaussianModel

cdef class LdaModel(GaussianModel):
    cdef dict w0
    cdef dict w

    cpdef double calculateMetric(self, Instance instance, str Ci)
    cpdef constructor1(self,
                       DiscreteDistribution priorDistribution,
                       dict w,
                       dict w0)
    cpdef constructor2(self, str fileName)
    cpdef loadWandW0(self, object inputFile, int size)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
