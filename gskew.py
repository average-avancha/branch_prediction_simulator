"""
Gskew Predictor

Please refer to the HW PDF for description of this task.
"""

from base import *

class GskewPredictor(AbstractPredictor):
    _BHR_LEN = 4
    _PHT_SIZE = 1 << 4

    def Initialize(self):
        self.pht = MultiTable(3, self._PHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        # iterate through all three tables and each pht and set correct values

    def MajorityVote(self, val_1, val_2, val_3):
        # this function might seem complex but remember that if any two values here equal each other, then you have a majority vote!
        pass
        
    def ParseCounter(self, counter : int) -> BranchResult:
        # check if counter is above the specific limit

        # issue prediction

        pass
    
    def UpdateCounter(self, counter : int, predicted_result : BranchResult, actual_result : BranchResult) -> int:
        # refer to lecture slides on how to update the counter

        # you can use predicted_result == BranchResult.TAKEN to compare values

        pass

    def f0(self, t_addr : int, bhr : int):
        # compute xor on first 4 bits of the target address (t_addr) ignoring the least significant bit
        pass
    
    def f1(self, t_addr : int, bhr : int):
        # compute xor on second 4 bits of the target address (t_addr) ignoring the least significant bit
        pass

    def f2(self, t_addr : int, bhr : int):
        # compute xor on third 4 bits of the target address (t_addr) ignoring the least significant bit
        pass

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        # you can access BHR register using Reg.BHR (example, self.GetRegVal(Reg.BHR))

        # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.GetTableVal(table ID, row number within a table)

        # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.SetTableVal(table ID, row number within a table, new data)

        # update BHR using self.SetRegVal(Reg.BHR, new value), make sure that BHR does not overflow as this will lead to incorrect predictions

        pass

    def Predict(self, target_address : int) -> BranchResult:
        # get bhr and get values from each function f0, f1 and f2

        # do majority vote
       
       pass