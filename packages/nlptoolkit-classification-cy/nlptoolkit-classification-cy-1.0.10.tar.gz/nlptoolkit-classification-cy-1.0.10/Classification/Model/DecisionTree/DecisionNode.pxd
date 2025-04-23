from Math.DiscreteDistribution cimport DiscreteDistribution

from Classification.Instance.Instance cimport Instance
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Model.DecisionTree.DecisionCondition cimport DecisionCondition
from Classification.Parameter.RandomForestParameter cimport RandomForestParameter


cdef class DecisionNode(object):

    cdef list children
    cdef str __class_label
    cdef bint leaf
    cdef DecisionCondition __condition
    cdef DiscreteDistribution __classLabelsDistribution

    cpdef __entropyForDiscreteAttribute(self, InstanceList data, int attributeIndex)
    cpdef __createChildrenForDiscreteIndexed(self, InstanceList data, int attributeIndex, int attributeValue,
                                           RandomForestParameter parameter, bint isStump)
    cpdef __createChildrenForDiscrete(self, InstanceList data, int attributeIndex, RandomForestParameter parameter, bint isStump)
    cpdef __createChildrenForContinuous(self, InstanceList data, int attributeIndex, double splitValue, RandomForestParameter parameter,
                                      bint isStump)
    cpdef str predict(self, Instance instance)
    cpdef dict predictProbabilityDistribution(self, Instance instance)
    cpdef constructor1(self, InstanceList data, object condition, object parameter, bint isStump)
    cpdef constructor2(self, object inputFile)
