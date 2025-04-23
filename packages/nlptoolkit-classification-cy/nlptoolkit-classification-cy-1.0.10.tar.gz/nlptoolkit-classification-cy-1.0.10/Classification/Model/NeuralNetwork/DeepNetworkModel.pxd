from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.NeuralNetwork.NeuralNetworkModel cimport NeuralNetworkModel
from Classification.Parameter.DeepNetworkParameter cimport DeepNetworkParameter
from Classification.Parameter.Parameter cimport Parameter

cdef class DeepNetworkModel(NeuralNetworkModel):

    cdef list __weights
    cdef int __hidden_layer_size
    cdef object __activation_function

    cpdef __allocateWeights(self, DeepNetworkParameter parameters)
    cpdef list __setBestWeights(self)
    cpdef calculateOutput(self)
    cpdef constructor1(self,
                       InstanceList trainSet,
                       InstanceList validationSet,
                       DeepNetworkParameter parameters)
    cpdef constructor2(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)