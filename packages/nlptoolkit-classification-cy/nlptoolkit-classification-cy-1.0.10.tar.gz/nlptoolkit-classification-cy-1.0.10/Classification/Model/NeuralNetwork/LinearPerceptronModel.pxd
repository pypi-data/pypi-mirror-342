from Classification.Parameter.Parameter cimport Parameter
from Math.Matrix cimport Matrix
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.NeuralNetwork.NeuralNetworkModel cimport NeuralNetworkModel
from Classification.Parameter.LinearPerceptronParameter cimport LinearPerceptronParameter

cdef class LinearPerceptronModel(NeuralNetworkModel):

    cdef Matrix W

    cpdef calculateOutput(self)
    cpdef constructor1(self, InstanceList trainSet)
    cpdef constructor2(self,
                       InstanceList trainSet,
                       InstanceList validationSet,
                       LinearPerceptronParameter parameters)
    cpdef constructor3(self, str fileName)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)
