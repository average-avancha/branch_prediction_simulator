"""
Static Predictor

Please refer to the HW PDF for description of this task.
"""

from base import *

class StaticPredictor(AbstractPredictor):
    def Initialize(self):
        pass

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        pass

    def Predict(self, target_address : int) -> BranchResult:
        if target_address > self.GetRegVal(Reg.PC):
            return BranchResult.TAKEN
        return BranchResult.NOT_TAKEN