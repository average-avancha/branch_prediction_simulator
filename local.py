"""
Local Predictor 

Please refer to the HW PDF for description of this task.
"""

from base import *

class LocalPredictor(AbstractPredictor):
    def Initialize(self):
        self.PHT_SIZE = 1 << 7
        self.pht = Table(self.PHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        # initialize pht here
        for i in range(self.PHT_SIZE):
            self.pht.SetTableVal(i, 0b0111)
        # self.pht_idx_mask = 0b01111111

        self.BHT_SIZE = 1 << 6
        self.bht = Table(self.BHT_SIZE) # DO NOT CHANGE VARIABLE NAME
        for i in range(self.BHT_SIZE):
            self.bht.SetTableVal(i, 0)
        # self.bht_idx_mask = 0b1111110
        self.bht_idx_shift = 1
        self.DEBUG = False
        # initialize bht here

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):

        # The BHT is a 7-bit table and we have a 16-bit target address,
        # so we need to mask the target address to reduce the size to 7 bits.
        # Additionally since the PC counter adds 2 to the address, the least significant
        # bit will remain the same, so we can mask 8 bits of the address and right shift by 1
        # to remove the least significant bit.
        
        # Index into BHT to point to the current spot in the PHT
        address = self.GetRegVal(Reg.PC)

        bht_idx_mask = (self.BHT_SIZE - 1) << self.bht_idx_shift
        bht_idx = (address & bht_idx_mask) >> self.bht_idx_shift
        bht_val = self.bht.GetTableVal(bht_idx)
        

        pht_idx = bht_val & (self.PHT_SIZE - 1)
        pht_val = self.pht.GetTableVal(pht_idx) #& self.pht_idx_mask
        
        if self.DEBUG:
            print(f"Update (old) | address: {bin(address)}, bht_idx: {bin(bht_idx)}, bht_val: {bin(bht_val)}, pht_idx: {bin(pht_idx)}, pht_val: {bin(pht_val)}")
        
        if actual_result == BranchResult.TAKEN:
            pht_state_update = min(pht_val + 1, 0b1111)
        elif actual_result == BranchResult.NOT_TAKEN:
            pht_state_update = max(pht_val - 1, 0b0000)
        
        self.pht.SetTableVal(pht_idx, pht_state_update)
        bht_state_update = (bht_val << 1) | actual_result.value
        self.bht.SetTableVal(bht_idx, bht_state_update)

        if self.DEBUG:
            print(f"Update (new) | address: {bin(address)}, bht_idx: {bin(bht_idx)}, bht_val: {bin(bht_val)}, pht_idx: {bin(pht_idx)}, pht_val: {bin(pht_val)}")

    def Predict(self, target_address : int) -> BranchResult:
        # Similar to the Update function, we need to mask and bit shift the target address to reduce the size to 7 useful bits.
        # The BHT is a 7-bit table and we have a 16-bit target address,
        # so we need to mask the target address to reduce the size to 7 bits.
        # Additionally since the PC counter adds 2 to the address, the least significant
        # bit will remain the same, so we can mask 8 bits of the address and right shift by 1
        # to remove the least significant bit.

        address = self.GetRegVal(Reg.PC)

        bht_idx_mask = (self.BHT_SIZE - 1) << self.bht_idx_shift
        bht_idx = (address & bht_idx_mask) >> self.bht_idx_shift
        
        bht_val = self.bht.GetTableVal(bht_idx)

        pht_idx = bht_val & (self.PHT_SIZE - 1)
        pht_val = self.pht.GetTableVal(pht_idx)

        if pht_val > 0b0111:
            return BranchResult.TAKEN
        else:
            return BranchResult.NOT_TAKEN