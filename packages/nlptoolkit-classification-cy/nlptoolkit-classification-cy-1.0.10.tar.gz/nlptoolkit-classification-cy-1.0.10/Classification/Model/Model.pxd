from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Classification.Performance.Performance cimport Performance
from Math.Matrix cimport Matrix

from Classification.Instance.Instance cimport Instance


cdef class Model(object):

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
    cpdef Instance loadInstance(self, str line, list attributeTypes)
    cpdef Matrix loadMatrix(self, object inputFile)

    cpdef InstanceList loadInstanceList(self, object inputFile)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)

    cpdef bint discreteCheck(self, Instance instance)
    cpdef Performance test(self, InstanceList testSet)
    cpdef Performance singleRun(self, Parameter parameter, InstanceList trainSet, InstanceList testSet)
