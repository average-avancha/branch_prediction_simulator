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
        self.DEBUG = False
        # iterate through all three tables and each pht and set correct values
        for t in range(3): # number of tables
            for pht_idx in range(self._PHT_SIZE): # number of rows in each table
                self.pht.SetTableVal(t, pht_idx, 0b01) # initalize each 2-bit pht table's value to 01

    def MajorityVote(self, val_1, val_2, val_3):
        # this function might seem complex but remember that if any two values here equal each other, then you have a majority vote!
        if val_1 == val_2 or val_1 == val_3:
            return val_1
        elif val_2 == val_3:
            return val_2
        else:
            # Tie breaker case
            return val_3
        
                
    def ParseCounter(self, counter : int) -> BranchResult:
        # check if counter is above the specific limit
        if counter > 0b01:
            return BranchResult.TAKEN
        else:
            return BranchResult.NOT_TAKEN
        # issue prediction
    
    def UpdateCounter(self, counter : int, predicted_result : BranchResult, actual_result : BranchResult) -> int:
        # refer to lecture slides on how to update the counter
        # you can use predicted_result == BranchResult.TAKEN to compare values
        update_counter = None
        if actual_result == BranchResult.TAKEN:
            update_counter = min(counter + 1, 0b11)
        else: # actual_result == BranchResult.NOT_TAKEN:
            update_counter = max(counter - 1, 0b00)
        
        return update_counter

    def f0(self, t_addr : int, bhr : int):
        # compute xor on first 4 bits of the target address (t_addr) ignoring the least significant bit
        t_addr_slice = (t_addr & 0b011110) >> 1
        
        if self.DEBUG:
            print(f"f0 | t_addr_slice: {t_addr_slice}, bhr: {bhr}, t_addr_slice ^ bhr: {t_addr_slice ^ bhr}")

        return t_addr_slice ^ bhr
    
    def f1(self, t_addr : int, bhr : int):
        # compute xor on second 4 bits of the target address (t_addr) ignoring the least significant bit
        t_addr_slice = (t_addr & 0b0111100000) >> 5
        
        if self.DEBUG:
            print(f"f1 | t_addr_slice: {t_addr_slice}, bhr: {bhr}, t_addr_slice ^ bhr: {t_addr_slice ^ bhr}")
        
        return t_addr_slice ^ bhr

    def f2(self, t_addr : int, bhr : int):
        # compute xor on third 4 bits of the target address (t_addr) ignoring the least significant bit
        t_addr_slice = (t_addr & 0b01111000000000) >> 9
        
        if self.DEBUG:
            print(f"f2 | t_addr_slice: {t_addr_slice}, bhr: {bhr}, t_addr_slice ^ bhr: {t_addr_slice ^ bhr}")
        
        return t_addr_slice ^ bhr

    def Update(self, target_address : int, predicted_result : BranchResult, actual_result : BranchResult):
        # you can access BHR register using Reg.BHR (example, self.GetRegVal(Reg.BHR))
        bhr = self.GetRegVal(Reg.BHR)
        f0_val = self.f0(target_address, bhr)
        f1_val = self.f1(target_address, bhr)
        f2_val = self.f2(target_address, bhr)

        # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.SetTableVal(table ID, row number within a table, new data)
        # as the PHT is multi-dimensional table, make sure you use following function to access it self.pht.GetTableVal(table ID, row number within a table)
        pht_0_val = self.pht.GetTableVal(0, f0_val)
        self.pht.SetTableVal(0, f0_val, self.UpdateCounter(pht_0_val, predicted_result, actual_result))

        pht_1_val = self.pht.GetTableVal(1, f1_val)
        self.pht.SetTableVal(1, f1_val, self.UpdateCounter(pht_1_val, predicted_result, actual_result))
        
        pht_2_val = self.pht.GetTableVal(2, f2_val)
        self.pht.SetTableVal(2, f2_val, self.UpdateCounter(pht_2_val, predicted_result, actual_result))


        # update BHR using self.SetRegVal(Reg.BHR, new value), make sure that BHR does not overflow as this will lead to incorrect predictions
        self.SetRegVal(Reg.BHR, ((bhr << 1) | actual_result.value) & ((1 << self._BHR_LEN) - 1))
        return

    def Predict(self, target_address : int) -> BranchResult:
        # get bhr and get values from each function f0, f1 and f2
        bhr = self.GetRegVal(Reg.BHR)
        f0_val = self.f0(target_address, bhr)
        f1_val = self.f1(target_address, bhr)
        f2_val = self.f2(target_address, bhr)

        # get values from each pht table
        pht_0_val = self.pht.GetTableVal(0, f0_val)
        pht_1_val = self.pht.GetTableVal(1, f1_val)
        pht_2_val = self.pht.GetTableVal(2, f2_val)

        # parse the counter values to get the prediction
        f0_vote = self.ParseCounter(pht_0_val)
        f1_vote = self.ParseCounter(pht_1_val)
        f2_vote = self.ParseCounter(pht_2_val)

        # do majority vote
        majority_vote = self.MajorityVote(f0_vote, f1_vote, f2_vote)
       
        return majority_vote