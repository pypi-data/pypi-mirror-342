from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionTree cimport DecisionTree
from Classification.Parameter.Parameter cimport Parameter

cdef class DecisionStump(DecisionTree):
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
