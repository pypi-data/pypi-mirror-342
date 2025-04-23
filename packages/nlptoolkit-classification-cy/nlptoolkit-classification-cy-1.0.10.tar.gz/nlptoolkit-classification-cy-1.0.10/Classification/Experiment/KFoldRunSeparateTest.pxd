from Sampling.CrossValidation cimport CrossValidation
from Classification.Model.Model cimport Model
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.KFoldRun cimport KFoldRun
from Classification.InstanceList.InstanceList cimport InstanceList
from Classification.Parameter.Parameter cimport Parameter
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class KFoldRunSeparateTest(KFoldRun):

    cpdef runExperimentSeparate(self, Model classifier, Parameter parameter, ExperimentPerformance experimentPerformance,
                      CrossValidation crossValidation, InstanceList testSet)
    cpdef ExperimentPerformance execute(self, Experiment experiment)
