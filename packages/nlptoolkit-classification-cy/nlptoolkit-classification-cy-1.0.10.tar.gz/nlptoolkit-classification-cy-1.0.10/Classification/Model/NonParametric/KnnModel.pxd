from Classification.DistanceMetric.DistanceMetric cimport DistanceMetric
from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.Model cimport Model
from Classification.Parameter.Parameter cimport Parameter

cdef class KnnModel(Model):

    cdef InstanceList __data
    cdef int __k
    cdef DistanceMetric __distance_metric

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
    cpdef InstanceList nearestNeighbors(self, Instance instance)
    cpdef InstanceList loadInstanceList(self, object inputFile)
    cpdef constructor1(self, InstanceList data, int k, DistanceMetric distanceMetric)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
