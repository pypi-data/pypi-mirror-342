from RFEM.initModel import Model, clearAttributes, deleteEmptyAttributes, ConvertToDlString, ConvertStrToListOfInt
from RFEM.enums import SetType, ObjectTypes

class MemberSet():
    def __init__(self,
                 no: int = 1,
                 members_no: str = '1 4 5 8 9 12 13 16 17 20 21 24',
                 member_set_type = SetType.SET_TYPE_GROUP,
                 comment: str = '',
                 params: dict = None,
                 model = Model):

        '''
        Args:
            no (int): Member Set Tag
            members_no (str): Numbers of Members Contained Within Member Set
            member_set_type (enum): Member Set Type Enumeration
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        '''

        # Client model | Member Set
        clientObject = model.clientModel.factory.create('ns0:member_set')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Member Set No.
        clientObject.no = no

        # Members number
        clientObject.members = ConvertToDlString(members_no)

        # Member Set Type
        clientObject.set_type = member_set_type.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Member Set to client model
        model.clientModel.service.set_member_set(clientObject)

    @staticmethod
    def ContinuousMembers(
                          no: int = 1,
                          members_no: str = '1 4 5 8 9 12 13 16 17 20 21 24',
                          comment: str = '',
                          params: dict = None,
                          model = Model):

        '''
        Args:
            no (int): Member Set Tag
            members_no (str): Numbers of Members Contained Within Continuous Member Set
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        '''

        # Client model | Member Set
        clientObject = model.clientModel.factory.create('ns0:member_set')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Member Set No.
        clientObject.no = no

        # Members number
        clientObject.members = ConvertToDlString(members_no)

        # Member Set Type
        clientObject.set_type = SetType.SET_TYPE_CONTINUOUS.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Member Set to client model
        model.clientModel.service.set_member_set(clientObject)

    @staticmethod
    def GroupOfmembers(
                       no: int = 1,
                       members_no: str = '1 4 5 8 9 12 13 16 17 20 21 24',
                       comment: str = '',
                       params: dict = None,
                       model = Model):

        '''
        Args:
            no (int): Member Set Tag
            members_no (str): Numbers of Members Contained Within Group of Members Member Set
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        '''

        # Client model | Member Set
        clientObject = model.clientModel.factory.create('ns0:member_set')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Member Set No.
        clientObject.no = no

        # Members number
        clientObject.members = ConvertToDlString(members_no)

        # Member Set Type
        clientObject.set_type = SetType.SET_TYPE_GROUP.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Member Set to client model
        model.clientModel.service.set_member_set(clientObject)

    @staticmethod
    def DeleteMemberSet(members_no: str = '1 2', model = Model):

        '''
        Args:
            members_no (str): Numbers of Members Sets to be deleted
            model (RFEM Class, optional): Model to be edited
        '''

        # Delete from client model
        for member in ConvertStrToListOfInt(members_no):
            model.clientModel.service.delete_object(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET.name, member)

    @staticmethod
    def GetMemberSet(object_index: int = 1, model = Model):

        '''
        Args:
            obejct_index (int): Member Set Index
            model (RFEM Class, optional): Model to be edited
        '''

        # Get Member Set from client model
        return model.clientModel.service.get_member_set(object_index)
