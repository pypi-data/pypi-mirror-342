from Classification.StatisticalTest.PairedTest cimport PairedTest
from Classification.Performance.ExperimentPerformance cimport ExperimentPerformance
from Classification.StatisticalTest.StatisticalTestNotApplicable import StatisticalTestNotApplicable
from Classification.StatisticalTest.StatisticalTestResult cimport StatisticalTestResult
from Math.Distribution cimport Distribution


cdef class Combined5x2F(PairedTest):

    cpdef __testStatistic(self,
                          ExperimentPerformance classifier1,
                          ExperimentPerformance classifier2):
        """
        Calculates the test statistic of the combined 5x2 cv F test.
        :param classifier1: Performance (error rate or accuracy) results of the first classifier.
        :param classifier2: Performance (error rate or accuracy) results of the second classifier.
        :return: Given the performances of two classifiers, the test statistic of the combined 5x2 cv F test.
        """
        cdef list difference
        cdef double numerator, denominator, mean, variance
        cdef int i
        if classifier1.numberOfExperiments() != classifier2.numberOfExperiments():
            raise StatisticalTestNotApplicable("In order to apply a paired test, you need to have the same number of "
                                               "experiments in both algorithms.")
        if classifier1.numberOfExperiments() != 10:
            raise StatisticalTestNotApplicable("In order to apply a 5x2 test, you need to have 10 experiments.")
        numerator = 0
        difference = []
        for i in range(classifier1.numberOfExperiments()):
            difference.append(classifier1.getErrorRate(i) - classifier2.getErrorRate(i))
            numerator += difference[i] * difference[i]
        denominator = 0
        for i in range(classifier1.numberOfExperiments() // 2):
            mean = (difference[2 * i] + difference[2 * i + 1]) / 2
            variance = (difference[2 * i] - mean) * (difference[2 * i] - mean) + (difference[2 * i + 1] - mean) \
                       * (difference[2 * i + 1] - mean)
            denominator += variance
        denominator *= 2
        if denominator == 0:
            raise StatisticalTestNotApplicable("Variance is 0.")
        return numerator / denominator

    cpdef StatisticalTestResult compare(self,
                                        ExperimentPerformance classifier1,
                                        ExperimentPerformance classifier2):
        """
        Compares two classification algorithms based on their performances (accuracy or error rate) using combined 5x2 cv F test.
        :param classifier1: Performance (error rate or accuracy) results of the first classifier.
        :param classifier2: Performance (error rate or accuracy) results of the second classifier.
        :return: Statistical test result of the comparison.
        """
        cdef double statistic
        cdef int degree_of_freedom1, degree_of_freedom2
        statistic = self.__testStatistic(classifier1, classifier2)
        degree_of_freedom1 = classifier1.numberOfExperiments()
        degree_of_freedom2 = classifier2.numberOfExperiments() // 2
        return StatisticalTestResult(Distribution.fDistribution(F=statistic,
                                                                freedom1=degree_of_freedom1,
                                                                freedom2=degree_of_freedom2), True)
