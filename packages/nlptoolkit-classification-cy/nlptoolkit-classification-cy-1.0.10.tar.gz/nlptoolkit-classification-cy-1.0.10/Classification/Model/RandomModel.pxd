from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.Model cimport Model
from Classification.Parameter.Parameter cimport Parameter

cdef class RandomModel(Model):

    cdef list __class_labels
    cdef int __seed

    cpdef str predict(self, Instance instance)
    cpdef dict predictProbability(self, Instance instance)
    cpdef constructor1(self, list classLabels, int seed)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)