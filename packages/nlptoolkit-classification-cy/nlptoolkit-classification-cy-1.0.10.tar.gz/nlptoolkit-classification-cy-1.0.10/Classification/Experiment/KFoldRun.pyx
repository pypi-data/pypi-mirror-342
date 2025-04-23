from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
from Classification.InstanceList.InstanceList cimport InstanceList


cdef class KFoldRun(MultipleRun):

    def __init__(self, K: int):
        """
        Constructor for KFoldRun class. Basically sets K parameter of the K-fold cross-validation.

        PARAMETERS
        ----------
        K : int
            K of the K-fold cross-validation.
        """
        self.K = K

    cpdef runExperiment(self,
                        Model classifier,
                        Parameter parameter,
                        ExperimentPerformance experimentPerformance,
                        CrossValidation crossValidation):
        """
        Runs a K fold cross-validated experiment for the given classifier with the given parameters. The experiment
        results will be added to the experimentPerformance.
        :param classifier: Classifier for the experiment
        :param parameter: Hyperparameters of the classifier of the experiment
        :param experimentPerformance: Storage to add experiment results
        :param crossValidation: K-fold crossvalidated dataset.
        """
        cdef int i
        cdef InstanceList train_set, test_set
        for i in range(self.K):
            train_set = InstanceList(crossValidation.getTrainFold(i))
            test_set = InstanceList(crossValidation.getTestFold(i))
            classifier.train(train_set, parameter)
            experimentPerformance.add(classifier.test(test_set))

    cpdef ExperimentPerformance execute(self, Experiment experiment):
        """
        Execute K-fold cross-validation with the given classifier on the given data set using the given parameters.

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
        cdef KFoldCrossValidation crossValidation
        result = ExperimentPerformance()
        crossValidation = KFoldCrossValidation(instance_list=experiment.getDataSet().getInstances(),
                                               K=self.K,
                                               seed=experiment.getParameter().getSeed())
        self.runExperiment(classifier=experiment.getClassifier(),
                           parameter=experiment.getParameter(),
                           experimentPerformance=result,
                           crossValidation=crossValidation)
        return result
