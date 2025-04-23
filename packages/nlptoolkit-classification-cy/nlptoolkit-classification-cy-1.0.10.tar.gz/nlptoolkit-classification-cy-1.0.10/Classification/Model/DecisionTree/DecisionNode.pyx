import random
from io import TextIOWrapper

from Classification.InstanceList.Partition cimport Partition
from Classification.Model.Model cimport Model
from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.Instance.CompositeInstance cimport CompositeInstance

cdef class DecisionNode(object):

    EPSILON = 0.0000000001

    def __init__(self,
                 data: object,
                 condition=None,
                 parameter=None,
                 isStump=False):
        if isinstance(data, InstanceList):
            self.constructor1(data, condition, parameter, isStump)
        elif isinstance(data, TextIOWrapper):
            self.constructor2(data)

    cpdef constructor1(self,
                 InstanceList data,
                 object condition,
                 object parameter,
                 bint isStump):
        """
        The DecisionNode method takes InstanceList data as input and then it sets the class label parameter by finding
        the most occurred class label of given data, it then gets distinct class labels as class labels ArrayList.
        Later, it adds ordered indices to the indexList and shuffles them randomly. Then, it gets the class distribution
        of given data and finds the best entropy value of these class distribution.

        If an attribute of given data is DiscreteIndexedAttribute, it creates a Distribution according to discrete
        indexed attribute class distribution and finds the entropy. If it is better than the last best entropy it
        reassigns the best entropy, best attribute and best split value according to the newly founded best entropy's
        index. At the end, it also add new distribution to the class distribution.

        If an attribute of given data is DiscreteAttribute, it directly finds the entropy. If it is better than the last
        best entropy it reassigns the best entropy, best attribute and best split value according to the newly founded
        best entropy's index.

        If an attribute of given data is ContinuousAttribute, it creates two distributions; left and right according
        to class distribution and discrete distribution respectively, and finds the entropy. If it is better than the
        last best entropy it reassigns the best entropy, best attribute and best split value according to the newly
        founded best entropy's index. At the end, it also add new distribution to the right distribution and removes
        from left distribution.

        PARAMETERS
        ----------
        data : InstanceList
            InstanceList input.
        condition : DecisionCondition
            DecisionCondition to check.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef int best_attribute, size, j, index, k
        cdef double best_entropy, entropy, previous_value
        cdef list class_labels, index_list
        cdef DiscreteDistribution class_distribution, distribution, left_distribution, right_distribution
        cdef Instance instance
        best_attribute = -1
        best_split_value = 0
        self.__condition = condition
        self.__classLabelsDistribution = DiscreteDistribution()
        labels = data.getClassLabels()
        for label in labels:
            self.__classLabelsDistribution.addItem(label)
        self.__class_label = InstanceList.getMaximum(labels)
        self.leaf = True
        self.children = []
        class_labels = data.getDistinctClassLabels()
        if len(class_labels) == 1:
            return
        if isStump and condition is not None:
            return
        index_list = [i for i in range(data.get(0).attributeSize())]
        if parameter is not None and parameter.getAttributeSubsetSize() < data.get(0).attributeSize():
            random.seed(parameter.getSeed())
            random.shuffle(index_list)
            size = parameter.getAttributeSubsetSize()
        else:
            size = data.get(0).attributeSize()
        class_distribution = data.classDistribution()
        best_entropy = data.classDistribution().entropy()
        for j in range(size):
            index = index_list[j]
            if isinstance(data.get(0).getAttribute(index), DiscreteIndexedAttribute):
                for k in range(data.get(0).getAttribute(index).getMaxIndex()):
                    distribution = data.discreteIndexedAttributeClassDistribution(index, k)
                    if distribution.getSum() > 0:
                        class_distribution.removeDistribution(distribution)
                        entropy = (class_distribution.entropy() * class_distribution.getSum() + distribution.entropy() * distribution.getSum()) / data.size()
                        if entropy + self.EPSILON < best_entropy:
                            best_entropy = entropy
                            best_attribute = index
                            best_split_value = k
                        class_distribution.addDistribution(distribution)
            elif isinstance(data.get(0).getAttribute(index), DiscreteAttribute):
                entropy = self.__entropyForDiscreteAttribute(data, index)
                if entropy + self.EPSILON < best_entropy:
                    best_entropy = entropy
                    best_attribute = index
            elif isinstance(data.get(0).getAttribute(index), ContinuousAttribute):
                data.sortWrtAttribute(index)
                previous_value = -100000000
                left_distribution = data.classDistribution()
                right_distribution = DiscreteDistribution()
                for k in range(data.size()):
                    instance = data.get(k)
                    if k == 0:
                        previous_value = instance.getAttribute(index).getValue()
                    elif instance.getAttribute(index).getValue() != previous_value:
                        split_value = (previous_value + instance.getAttribute(index).getValue()) / 2
                        previous_value = instance.getAttribute(index).getValue()
                        entropy = (left_distribution.getSum() / data.size()) * left_distribution.entropy() + \
                                  (right_distribution.getSum() / data.size()) * right_distribution.entropy()
                        if entropy + self.EPSILON < best_entropy:
                            best_entropy = entropy
                            best_split_value = split_value
                            best_attribute = index
                    left_distribution.removeItem(instance.getClassLabel())
                    right_distribution.addItem(instance.getClassLabel())
        if best_attribute != -1:
            self.leaf = False
            if isinstance(data.get(0).getAttribute(best_attribute), DiscreteIndexedAttribute):
                self.__createChildrenForDiscreteIndexed(data=data,
                                                        attributeIndex=best_attribute,
                                                        attributeValue=best_split_value,
                                                        parameter=parameter,
                                                        isStump=isStump)
            elif isinstance(data.get(0).getAttribute(best_attribute), DiscreteAttribute):
                self.__createChildrenForDiscrete(data=data,
                                                 attributeIndex=best_attribute,
                                                 parameter=parameter,
                                                 isStump=isStump)
            elif isinstance(data.get(0).getAttribute(best_attribute), ContinuousAttribute):
                self.__createChildrenForContinuous(data=data,
                                                   attributeIndex=best_attribute,
                                                   splitValue=best_split_value,
                                                   parameter=parameter,
                                                   isStump=isStump)

    cpdef constructor2(self, object inputFile):
        cdef str line
        cdef list items
        cdef int i, number_of_children
        line = inputFile.readline().strip()
        items = line.split(" ")
        if items[0] != "-1":
            if items[1][0] == '=':
                self.__condition = DecisionCondition(int(items[0]), DiscreteAttribute(items[2]), items[1][0])
            elif items[1][0] == ':':
                self.__condition = DecisionCondition(int(items[0]), DiscreteIndexedAttribute("", int(items[2]), int(items[3])), '=')
            else:
                self.__condition = DecisionCondition(int(items[0]), ContinuousAttribute(float(items[2])), items[1][0])
        else:
            self.__condition = None
        number_of_children = int(inputFile.readline().strip())
        if number_of_children != 0:
            self.leaf = False
            self.children = []
            for i in range(number_of_children):
                self.children.append(DecisionNode(inputFile))
        else:
            self.leaf = True
            self.__class_label = inputFile.readline().strip()
            self.__classLabelsDistribution = Model.loadClassDistribution(inputFile)

    cpdef __entropyForDiscreteAttribute(self, InstanceList data, int attributeIndex):
        """
        The entropyForDiscreteAttribute method takes an attributeIndex and creates an ArrayList of DiscreteDistribution.
        Then loops through the distributions and calculates the total entropy.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.

        RETURNS
        -------
        float
            Total entropy for the discrete attribute.
        """
        cdef double total
        cdef list distributions
        cdef DiscreteDistribution distribution
        total = 0.0
        distributions = data.attributeClassDistribution(attributeIndex)
        for distribution in distributions:
            total += (distribution.getSum() / data.size()) * distribution.entropy()
        return total

    cpdef __createChildrenForDiscreteIndexed(self,
                                             InstanceList data,
                                             int attributeIndex,
                                             int attributeValue,
                                             RandomForestParameter parameter,
                                             bint isStump):
        """
        The createChildrenForDiscreteIndexed method creates an list of DecisionNodes as children and a partition with
        respect to indexed attribute.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        attributeValue : int
            Value of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef Partition children_data
        children_data = Partition(data, attributeIndex, attributeValue)
        self.children.append(
            DecisionNode(data=children_data.get(0),
                         condition=DecisionCondition(attributeIndex,
                                           DiscreteIndexedAttribute("",
                                                                    attributeValue,
                                                                    data.get(0).getAttribute(attributeIndex).getMaxIndex())),
                         parameter=parameter,
                         isStump=isStump))
        self.children.append(
            DecisionNode(data=children_data.get(1),
                         condition=DecisionCondition(attributeIndex,
                                           DiscreteIndexedAttribute("",
                                                                    -1,
                                                                    data.get(0).getAttribute(attributeIndex).getMaxIndex())),
                         parameter=parameter,
                         isStump=isStump))

    cpdef __createChildrenForDiscrete(self,
                                      InstanceList data,
                                      int attributeIndex,
                                      RandomForestParameter parameter,
                                      bint isStump):
        """
        The createChildrenForDiscrete method creates an ArrayList of values, a partition with respect to attributes and
        a list of DecisionNodes as children.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        """
        cdef list value_list
        cdef Partition children_data
        cdef int i
        value_list = data.getAttributeValueList(attributeIndex)
        children_data = Partition(data, attributeIndex)
        for i in range(len(value_list)):
            self.children.append(DecisionNode(data=children_data.get(i),
                                              condition=DecisionCondition(attributeIndex, DiscreteAttribute(value_list[i])),
                                              parameter=parameter,
                                              isStump=isStump))

    cpdef __createChildrenForContinuous(self,
                                        InstanceList data,
                                        int attributeIndex,
                                        double splitValue,
                                        RandomForestParameter parameter,
                                        bint isStump):
        """
        The createChildrenForContinuous method creates a list of DecisionNodes as children and a partition with respect
        to continuous attribute and the given split value.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        parameter : RandomForestParameter
            RandomForestParameter like seed, ensembleSize, attributeSubsetSize.
        isStump : bool
            Refers to decision trees with only 1 splitting rule.
        splitValue : float
            Split value is used for partitioning.
        """
        cdef Partition children_data
        children_data = Partition(data, attributeIndex, splitValue)
        self.children.append(DecisionNode(children_data.get(0),
                                          DecisionCondition(attributeIndex, ContinuousAttribute(splitValue), "<"),
                                          parameter, isStump))
        self.children.append(DecisionNode(children_data.get(1),
                                          DecisionCondition(attributeIndex, ContinuousAttribute(splitValue), ">"),
                                          parameter, isStump))

    cpdef str predict(self, Instance instance):
        """
        The predict method takes an Instance as input and performs prediction on the DecisionNodes and returns the
        prediction for that instance.

        PARAMETERS
        ----------
        instance : Instance
            Instance to make prediction.

        RETURNS
        -------
        str
            The prediction for given instance.
        """
        cdef list possible_class_labels
        cdef DiscreteDistribution distribution
        cdef str predicted_class, child_prediction
        cdef DecisionNode node
        if isinstance(instance, CompositeInstance):
            possible_class_labels = instance.getPossibleClassLabels()
            distribution = self.__classLabelsDistribution
            predicted_class = distribution.getMaxItemIncludeTheseOnly(possible_class_labels)
            if self.leaf:
                return predicted_class
            else:
                for node in self.children:
                    if node.__condition.satisfy(instance):
                        child_prediction = node.predict(instance)
                        if child_prediction is not None:
                            return child_prediction
                        else:
                            return predicted_class
                return predicted_class
        elif self.leaf:
            return self.__class_label
        else:
            for node in self.children:
                if node.__condition.satisfy(instance):
                    return node.predict(instance)
            return self.__class_label

    cpdef dict predictProbabilityDistribution(self, Instance instance):
        cdef DecisionNode node
        if self.leaf:
            return self.__classLabelsDistribution.getProbabilityDistribution()
        else:
            for node in self.children:
                if node.__condition.satisfy(instance):
                    return node.predictProbabilityDistribution(instance)
            return self.__classLabelsDistribution.getProbabilityDistribution()
