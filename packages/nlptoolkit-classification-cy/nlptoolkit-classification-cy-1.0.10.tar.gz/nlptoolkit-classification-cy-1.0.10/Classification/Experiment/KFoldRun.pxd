from Sampling.CrossValidation cimport CrossValidation
from Classification.Model.Model cimport Model
from Classification.Experiment.Experiment cimport Experiment
from Classification.Experiment.MultipleRun cimport MultipleRun
from Classification.Parameter.Parameter cimport Parameter
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance


cdef class KFoldRun(MultipleRun):

    cdef int K

    cpdef runExperiment(self, Model classifier, Parameter parameter, ExperimentPerformance experimentPerformance,
                      CrossValidation crossValidation)
    cpdef ExperimentPerformance execute(self, Experiment experiment)
