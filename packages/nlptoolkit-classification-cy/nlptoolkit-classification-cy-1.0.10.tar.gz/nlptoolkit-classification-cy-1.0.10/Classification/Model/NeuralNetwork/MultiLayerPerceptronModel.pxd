from Classification.Parameter.Parameter cimport Parameter
from Math.Matrix cimport Matrix

from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.NeuralNetwork.LinearPerceptronModel cimport LinearPerceptronModel
from Classification.Parameter.MultiLayerPerceptronParameter cimport MultiLayerPerceptronParameter

cdef class MultiLayerPerceptronModel(LinearPerceptronModel):

    cdef Matrix __V
    cdef object __activation_function

    cpdef __allocateWeights(self, int H, int seed)
    cpdef calculateOutput(self)
    cpdef constructor3(self, str fileName)
    cpdef constructor4(self,
                     InstanceList trainSet,
                     InstanceList validationSet,
                     MultiLayerPerceptronParameter parameters)
    cpdef train(self, InstanceList trainSet, Parameter parameters)
    cpdef loadModel(self, str fileName)