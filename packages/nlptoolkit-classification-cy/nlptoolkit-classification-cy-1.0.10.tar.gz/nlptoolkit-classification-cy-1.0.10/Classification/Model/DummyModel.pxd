from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.Model cimport Model
from Classification.Instance.Instance cimport Instance
from Classification.Parameter.Parameter cimport Parameter
from Math.DiscreteDistribution cimport DiscreteDistribution


cdef class DummyModel(Model):

    cdef DiscreteDistribution distribution

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
    cpdef constructor1(self, InstanceList trainSet)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
