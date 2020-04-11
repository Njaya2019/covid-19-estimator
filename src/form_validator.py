# A classes to validate form keys and values


class FormValidator():

    @staticmethod
    def checkEmptyValues(**formDict):

        """ check if json values are empty"""

        for value in formDict.values():
            if not value:
                return False
        return True

    @staticmethod
    def checkFormKeys(**formDict):

        """ check if a json key exists """

        if all([formkey for formkey in formDict]):
            return True
        return False

    @staticmethod
    def checkFormValidKeys(*requiredKeys, **formDict):

        """ checks for valid json keys """

        if all(
            [requiredkey in formDict.keys() for requiredkey in requiredKeys]
        ):
            return True
        return False

    @staticmethod
    def checkValidString(*formStrings):

        """ checks if json strings are valid """

        for formString in formStrings:
            if type(formString) == int:
                return False
        return True

    @staticmethod
    def checkValidInt(*formInts):

        """ checks if json integers are valid """

        for formInt in formInts:
            if type(formInt) == str:
                return False
        return True

    @staticmethod
    def checkAbsoluteSpaceCharacters(*fromStrings):

        """ A method to check if values are space characters """

        for fromString in fromStrings:
            if fromString.isspace():
                return True
        return False
