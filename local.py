"""
Local Predictor 

Please refer to the HW PDF for description of this task.
"""

from base import *

class LocalPredictor(AbstractPredictor):
    def Initialize(self):
        PHT_SIZE = 1 << 7
        self.pht = Table(PHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        # initialize pht here
        for i in range(PHT_SIZE):
            self.pht.SetTableVal(i, 0b0111)
        self.pht_idx_mask = 0b01111111

        BHT_SIZE = 1 << 6
        self.bht = Table(BHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        for i in range(BHT_SIZE):
            self.bht.SetTableVal(i, 0)
        self.bht_idx_mask = 0b11111100
        self.bht_idx_shift = 2
        # initialize bht here

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        bht_idx = (target_address & self.bht_idx_mask ) >> self.bht_idx_shift
        # bht_idx = (self.GetRegVal(Reg.PC) & self.bht_idx_mask ) >> 2
        bht_val = self.bht.GetTableVal(bht_idx)

        pht_idx = bht_val & self.pht_idx_mask
        pht_val = self.pht.GetTableVal(pht_idx) & self.pht_idx_mask
        
        if actual_result == BranchResult.TAKEN:
            pht_state_update = min(pht_val + 1, 0b1111)
            self.pht.SetTableVal(pht_idx, pht_state_update)
            bht_state_update = (bht_val << 1) | BranchResult.TAKEN.value
            self.bht.SetTableVal(bht_idx, bht_state_update)
        
        elif actual_result == BranchResult.NOT_TAKEN:
            pht_state_update = max(pht_val - 1, 0b0000)
            self.pht.SetTableVal(pht_idx, pht_state_update)
            bht_state_update = (bht_val << 1) | BranchResult.NOT_TAKEN.value
            self.bht.SetTableVal(bht_idx, bht_state_update)


    def Predict(self, target_address : int) -> BranchResult:
        bht_idx = (target_address & self.bht_idx_mask) >> self.bht_idx_shift
        # print(f"bht_val: {bin(bht_val)}, pht_idx: {bin(pht_idx)}")
        # bht_idx = (self.GetRegVal(Reg.PC) & self.bht_idx_mask ) >> 2
        
        bht_val = self.bht.GetTableVal(bht_idx)

        pht_idx = bht_val & self.pht_idx_mask
        # print(f"bht_val: {bin(bht_val)}, pht_idx: {bin(pht_idx)}")
        pht_val = self.pht.GetTableVal(pht_idx)

        if pht_val > 0b0111:
            return BranchResult.TAKEN
        return BranchResult.NOT_TAKEN