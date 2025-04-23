from RFEM.initModel import Model, clearAttributes, deleteEmptyAttributes
from RFEM.enums import AnalysisType, ActionCategoryType, ObjectTypes
from RFEM.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RFEM.Tools.GetObjectNumbersByType import GetObjectNumbersByType


class LoadCase():

    def __init__(self,
                 no: int = 1,
                 name: str = 'Self-weight',
                 self_weight: list = [True, 0.0, 0.0, 1.0],
                 action_category=ActionCategoryType.ACTION_CATEGORY_NONE_NONE,
                 imperfection_case: int = None,
                 structure_modification: int = None,
                 comment: str = 'Comment',
                 params: dict = None,
                 model = Model):
        '''
        Args:
            no (int): Load Case Tag
            name (str): Load Case Name
            self_weight (list): Self-Weight Parameters
                self_weight = [self_weight_active, self_weight_factor_x, self_weight_factor_y, self_weight_factor_z]
            action_category (enum): Action Category Type Enumeration
            imperfection_case (int, optional): Assign Imperfection Case
            structure_modification (int,optional): Assign Structure Modification
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        '''

        # Client model | Load Case
        clientObject = model.clientModel.factory.create('ns0:load_case')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Load Case No.
        clientObject.no = no

        # Load Case Name
        clientObject.name = name

        # To Solve
        clientObject.to_solve = True

        # Analysis Type
        clientObject.analysis_type = AnalysisType.ANALYSIS_TYPE_STATIC.name
        sas = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_STATIC_ANALYSIS_SETTINGS)
        if sas:
            clientObject.static_analysis_settings = sas[0]
        else:
            StaticAnalysisSettings(1)
            clientObject.static_analysis_settings = 1

        # Action Category
        if action_category.name not in LoadCasesAndCombinations.getAvailableLoadActionCategoryTypes():
            raise ValueError('WARNING: The selected Action Category is not available under the defined Standard.')
        clientObject.action_category = action_category.name

        # Self-weight Considerations
        clientObject.self_weight_active = self_weight[0]
        if not isinstance(self_weight[0], bool):
            raise ValueError('WARNING: Entry at index 0 of Self-Weight parameter to be of type bool')
        if self_weight[0]:
            if len(self_weight) != 4:
                raise ValueError('WARNING: Self-weight is activated and therefore requires a list definition of length 4. Kindly check list inputs for completeness and correctness.')
            clientObject.self_weight_factor_x = self_weight[1]
            clientObject.self_weight_factor_y = self_weight[2]
            clientObject.self_weight_factor_z = self_weight[3]
        else:
            if len(self_weight) != 1:
                raise ValueError('WARNING: Self-weight is deactivated and therefore requires a list definition of length 1. Kindly check list inputs for completeness and correctness.')

        # Options
        if imperfection_case:
            clientObject.consider_imperfection = True
            ic = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_IMPERFECTION_CASE)
            if imperfection_case in ic:
                clientObject.imperfection_case = imperfection_case
        else:
            clientObject.consider_imperfection = False

        if structure_modification:
            clientObject.structure_modification_enabled = True
            sm = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_STRUCTURE_MODIFICATION)
            if structure_modification in sm:
                clientObject.structure_modification = structure_modification
        else:
            clientObject.structure_modification_enabled = False

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Load Case to client model
        model.clientModel.service.set_load_case(clientObject)

    @staticmethod
    def StaticAnalysis(
            no: int = 1,
            name: str = 'Self-weight',
            to_solve: bool = True,
            analysis_settings_no: int = 1,
            action_category=ActionCategoryType.ACTION_CATEGORY_NONE_NONE,
            self_weight: list =[True, 0.0, 0.0, 10.0],
            imperfection_case: int = None,
            structure_modification: int = None,
            comment: str = 'Comment',
            params: dict = None,
            model = Model):
        '''
        Args:
            no (int): Load Case Tag
            name (str): Load Case Name
            to_solve (bool): Enable/Disbale Load Case Solver Status
            analysis_settings_no (int): Analysis Settings Number
            action_category (enum): Action Category Enumeration
            self_weight (list): Self-weight Considerations
                for self-weight considerations;
                    self_weight = [True, self_weight_factor_x, self_weight_factor_y, self_weight_factor_z]
                for no self-weight considerations;
                    self_weight = [False]
            imperfection_case (int, optional): Assign Imperfection Case
            structure_modification (int,optional): Assign Structure Modification
            comment (str, optional): Comments
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RFEM Class, optional): Model to be edited
        '''

        # Client model | Load Case
        clientObject = model.clientModel.factory.create('ns0:load_case')

        # Clears object atributes | Sets all atributes to None
        clearAttributes(clientObject)

        # Load Case No.
        clientObject.no = no

        # Load Case Name
        clientObject.name = name

        # To Solve
        clientObject.to_solve = to_solve

        # Analysis Type
        clientObject.analysis_type = AnalysisType.ANALYSIS_TYPE_STATIC.name
        sas = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_STATIC_ANALYSIS_SETTINGS)
        if analysis_settings_no in sas:
            clientObject.static_analysis_settings = analysis_settings_no
        else:
            StaticAnalysisSettings(1)
            clientObject.static_analysis_settings = 1

        # Action Category
        if action_category.name not in LoadCasesAndCombinations.getAvailableLoadActionCategoryTypes():
            raise ValueError('WARNING: The selected Action Category is not available under the defined Standard.')
        clientObject.action_category = action_category.name

        # Self-weight Considerations
        clientObject.self_weight_active = self_weight[0]
        if not isinstance(self_weight[0], bool):
            raise ValueError('WARNING: Entry at index 0 of Self-Weight parameter to be of type bool')
        if self_weight[0]:
            if len(self_weight) != 4:
                raise ValueError('WARNING: Self-weight is activated and therefore requires a list definition of length 4. Kindly check list inputs for completeness and correctness.')
            clientObject.self_weight_factor_x = self_weight[1]
            clientObject.self_weight_factor_y = self_weight[2]
            clientObject.self_weight_factor_z = self_weight[3]
        else:
            if len(self_weight) != 1:
                raise ValueError('WARNING: Self-weight is deactivated and therefore requires a list definition of length 1. Kindly check list inputs for completeness and correctness.')

        # Options
        if imperfection_case:
            clientObject.consider_imperfection = True
            ic = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_IMPERFECTION_CASE)
            if imperfection_case in ic:
                clientObject.imperfection_case = imperfection_case
        else:
            clientObject.consider_imperfection = False

        if structure_modification:
            clientObject.structure_modification_enabled = True
            sm = GetObjectNumbersByType(ObjectTypes.E_OBJECT_TYPE_STRUCTURE_MODIFICATION)
            if structure_modification in sm:
                clientObject.structure_modification = structure_modification
        else:
            clientObject.structure_modification_enabled = False

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Delete None attributes for improved performance
        deleteEmptyAttributes(clientObject)

        # Add Load Case to client model
        model.clientModel.service.set_load_case(clientObject)
