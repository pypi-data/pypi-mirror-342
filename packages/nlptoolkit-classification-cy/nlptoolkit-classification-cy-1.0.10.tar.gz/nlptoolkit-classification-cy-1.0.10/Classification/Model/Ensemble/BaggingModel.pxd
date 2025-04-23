from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.Ensemble.TreeEnsembleModel cimport TreeEnsembleModel
from Classification.Parameter.Parameter cimport Parameter

cdef class BaggingModel(TreeEnsembleModel):

    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
