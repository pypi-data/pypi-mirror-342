from Classification.Attribute.AttributeType import AttributeType


cdef class DataDefinition(object):

    def __init__(self, attributeTypes=None, attributeValueList=None):
        """
        Constructor for creating a new DataDefinition with given attribute types.

        PARAMETERS
        ----------
        attributeTypes : list
            Attribute types of the data definition.
        """
        if attributeTypes is None:
            attributeTypes = []
        if attributeValueList is not None:
            self.__attributeValueList = attributeValueList
        self.__attributeTypes = attributeTypes

    cpdef int numberOfValues(self, int attributeIndex):
        """
        Returns number of distinct values for a given discrete attribute with index attributeIndex.
        :param attributeIndex: Index of the discrete attribute.
        :return: Number of distinct values for a given discrete attribute
        """
        return len(self.__attributeValueList[attributeIndex])

    cpdef int featureValueIndex(self,
                          int attributeIndex,
                          str value: str):
        """
        Returns the index of the given value in the values list of the attributeIndex'th discrete attribute.
        :param attributeIndex: Index of the discrete attribute.
        :param value: Value of the discrete attribute
        :return: Index of the given value in the values list of the discrete attribute.
        """
        cdef int i
        for i in range(len(self.__attributeValueList[attributeIndex])):
            if self.__attributeValueList[attributeIndex][i] == value:
                return i
        return -1

    cpdef int attributeCount(self):
        """
        Returns the number of attribute types.

        RETURNS
        -------
        int
            Number of attribute types.
        """
        return len(self.__attributeTypes)

    cpdef int discreteAttributeCount(self):
        """
        Counts the occurrences of binary and discrete type attributes.

        RETURNS
        -------
        int
            Count of binary and discrete type attributes.
        """
        cdef int count
        count = 0
        for attributeType in self.__attributeTypes:
            if attributeType is AttributeType.DISCRETE or attributeType is AttributeType.BINARY:
                count = count + 1
        return count

    cpdef int continuousAttributeCount(self):
        """
        Counts the occurrences of binary and continuous type attributes.

        RETURNS
        -------
        int
            Count of of binary and continuous type attributes.
        """
        cdef int count
        count = 0
        for attributeType in self.__attributeTypes:
            if attributeType is AttributeType.CONTINUOUS:
                count = count + 1
        return count

    cpdef object getAttributeType(self, int index):
        """
        Returns the attribute type of the corresponding item at given index.

        PARAMETERS
        ----------
        index : int
            Index of the attribute type.

        RETURNS
        -------
        AttributeType
            Attribute type of the corresponding item at given index.
        """
        return self.__attributeTypes[index]

    cpdef addAttribute(self, object attributeType):
        """
        Adds an attribute type to the list of attribute types.

        PARAMETERS
        ----------
        attributeType : AttributeType
            Attribute type to add to the list of attribute types.
        """
        self.__attributeTypes.append(attributeType)

    cpdef removeAttribute(self, int index):
        """
        Removes the attribute type at given index from the list of attributes.

        PARAMETERS
        ----------
        index : int
            Index to remove attribute type from list.
        """
        self.__attributeTypes.pop(index)

    cpdef removeAllAtrributes(self):
        """
        Clears all the attribute types from list.
        """
        self.__attributeTypes.clear()

    cpdef DataDefinition getSubSetOfFeatures(self, FeatureSubSet featureSubSet):
        """
        Generates new subset of attribute types by using given feature subset.

        PARAMETERS
        ----------
        featureSubSet : FeatureSubSet
            FeatureSubSet input.

        RETURNS
        -------
        DataDefinition
            DataDefinition with new subset of attribute types.
        """
        cdef list new_attribute_types
        cdef int i
        new_attribute_types = []
        for i in range(featureSubSet.size()):
            new_attribute_types.append(self.__attributeTypes[featureSubSet.get(i)])
        return DataDefinition(new_attribute_types)
