from RFEM.initModel import Model, clearAttributes, deleteEmptyAttributes, ConvertToDlString

class AluminumDesignSLSConfigurations():

    def __init__(self,
                 no: int = 1,
                 name: str = 'SLS1',
                 members_no: str = 'All',
                 member_sets_no: str = 'All',
                 comment: str = '',
                 params: dict = None,
                 model = Model):

        """
        Args:
            no (int): Aluminum Design Serviceability Limit State Configuration Tag
            name (str): User Defined Configuration Name
            members_no (str): Assign Configuration to Selected Members
            member_sets_no (str): Assign Configuration to Selected Member Sets
            comment (str, optional): Comment
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        """

        # Client Model | Aluminum Design Serviceability Limit State Configurations
        clientObject = model.clientModel.factory.create('ns0:aluminum_design_sls_configuration')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # ULS Configuration No.
        clientObject.no = no

        # User Defined Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Assigned Members
        if members_no == 'All':
            clientObject.assigned_to_all_members = True

        else:
            clientObject.assigned_to_all_members = False
            clientObject.assigned_to_members = ConvertToDlString(members_no)

        # Assigned Member Sets
        if member_sets_no == 'All':
            clientObject.assigned_to_all_member_sets = True

        else:
            clientObject.assigned_to_all_member_sets = False
            clientObject.assigned_to_member_sets = ConvertToDlString(member_sets_no)

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Aluminum Design SLS Configuration to Client Model
        model.clientModel.service.set_aluminum_design_sls_configuration(clientObject)
