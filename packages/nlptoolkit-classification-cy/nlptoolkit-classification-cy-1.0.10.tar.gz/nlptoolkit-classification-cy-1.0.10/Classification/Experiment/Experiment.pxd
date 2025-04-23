from Classification.FeatureSelection.FeatureSubSet cimport FeatureSubSet
from Classification.Model.Model cimport Model
from Classification.Parameter.Parameter cimport Parameter
from Classification.DataSet.DataSet cimport DataSet


cdef class Experiment(object):

    cdef Model __classifier
    cdef Parameter __parameter
    cdef DataSet __dataSet

    cpdef Model getClassifier(self)
    cpdef Parameter getParameter(self)
    cpdef DataSet getDataSet(self)
    cpdef Experiment featureSelectedExperiment(self, FeatureSubSet featureSubSet)
