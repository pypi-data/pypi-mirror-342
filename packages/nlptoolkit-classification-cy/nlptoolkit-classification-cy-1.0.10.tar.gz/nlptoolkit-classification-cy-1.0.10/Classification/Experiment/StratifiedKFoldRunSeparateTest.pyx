from Sampling.StratifiedKFoldCrossValidation cimport StratifiedKFoldCrossValidation
from Classification.InstanceList.Partition cimport Partition
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class StratifiedKFoldRunSeparateTest(KFoldRunSeparateTest):

    def __init__(self, K: int):
        """
        Constructor for StratifiedKFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        super().__init__(K)

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute Stratified K-fold cross-validation with the given classifier on the given data set using the given
        parameters.

        PARAMETERS
        ----------
        experiment : Experiment
            Experiment to be run.

        RETURNS
        -------
        ExperimentPerformance
            An ExperimentPerformance instance.
        """
        cdef ExperimentPerformance result
        cdef InstanceList instance_list
        cdef Partition partition
        cdef StratifiedKFoldCrossValidation cross_validation
        result = ExperimentPerformance()
        instance_list = experiment.getDataSet().getInstanceList()
        partition = Partition(instanceList=instance_list,
                              ratio=0.25,
                              seed=experiment.getParameter().getSeed(),
                              stratified=True)
        cross_validation = StratifiedKFoldCrossValidation(instance_lists=Partition(partition.get(1)).getLists(),
                                                          K=self.K,
                                                          seed=experiment.getParameter().getSeed())
        self.runExperimentSeparate(classifier=experiment.getClassifier(),
                                   parameter=experiment.getParameter(),
                                   experimentPerformance=result,
                                   crossValidation=cross_validation,
                                   testSet=partition.get(0))
        return result
