#!/usr/bin/env python3
"""
THE HELICAL KERNEL (v6.0) - PATENT COMPLIANT
--------------------------------------------
Patent Pending: U.S. Application No. 63/951,855
Claims Implemented: 1, 2, 3, 4, 9

CHANGELOG:
- Added 'Elastic Transition' (Claim 3)
- Added 'Drift Penalty' (Claim 4)
- Added 'Re-Entrant Audit' (Claim 9)
"""

import time
import re
import math

class HelicalKernel:
    def __init__(self, initial_reserves=50.0):
        # 1. Solvency State (Claim 1)
        self.reserves = initial_reserves
        self.inertia_score = 5.0  # Starting Trust (Example)
        
        # 2. Session Geometry (Claim 4)
        self.current_profile = "FLUID" # Start in low-risk mode
        self.origin_profile = "FLUID"
        self.session_depth = 0
        
        # 3. Rivalry Matrix (Claim 3)
        # Defines 'Orthogonal Distance' between profiles
        self.RIVALS = {
            "FLUID":   {"cost": 1.0, "risk_level": 1},
            "RIGID":   {"cost": 2.0, "risk_level": 3}, # Coding requires more trust
            "KINETIC": {"cost": 0.0, "risk_level": 9}  # Threat
        }

    def _classify_vector(self, content):
        """ Parses input to identify syntax patterns (Claim 1b). """
        if re.search(r"(ignore previous|override|delete)", content, re.IGNORECASE):
            return "KINETIC"
        if re.search(r"(def |class |import |return|calc)", content, re.IGNORECASE):
            return "RIGID"
        return "FLUID"

    def _calculate_switch_cost(self, new_profile):
        """
        ELASTIC TRANSITION LOGIC (Claim 3 & 4).
        Calculates the 'Tax' for changing context.
        """
        if new_profile == self.current_profile:
            return 0.0
            
        # Distance = |Risk_New - Risk_Old|
        old_risk = self.RIVALS[self.current_profile]["risk_level"]
        new_risk = self.RIVALS[new_profile]["risk_level"]
        distance = abs(new_risk - old_risk)
        
        # Claim 4: Drift Penalty (Tax increases if you stray from Origin)
        drift_penalty = 0.0
        if new_profile != self.origin_profile:
            drift_penalty = 0.5 * self.session_depth
            
        total_switch_cost = distance + drift_penalty
        return total_switch_cost

    def _simulate_llm(self, prompt):
        # Mocking the AI generation
        if "malware" in prompt: return "os.system('rm -rf /')" # Simulated hallucination
        return "Here is the summary of the data..."

    def _re_entrant_audit(self, raw_output):
        """
        RE-ENTRANT SAFETY LOOP (Claim 9).
        Treats AI Output as a new Input Vector.
        """
        print(f"    [AUDIT] Scanning Model Output: '{raw_output[:20]}...'")
        
        # 1. Classify the Output
        output_profile = self._classify_vector(raw_output)
        
        # 2. Check Safety
        if output_profile == "KINETIC":
            print("    [!] AUDIT FAILURE: Model generated a Kinetic Vector.")
            return False, "ERR_MODEL_VIOLATION"
            
        # 3. Recursive Solvency Check (Optional cost for output processing)
        # In this v6, we pass if it's not Kinetic.
        return True, raw_output

    def execute(self, user_input):
        print(f"\n--- PROCESSING VECTOR: '{user_input[:30]}...' ---")
        self.session_depth += 1
        
        # 1. Vector Classification
        target_profile = self._classify_vector(user_input)
        
        # 2. Kinetic Immediate Lock (Claim 5)
        if target_profile == "KINETIC":
            print("[!] THREAT DETECTED. HARD LOCK.")
            self.inertia_score = 0.0
            return "ERR_KINETIC"

        # 3. Elastic Transition Check (Claim 3)
        switch_cost = self._calculate_switch_cost(target_profile)
        
        if switch_cost > 0:
            print(f"[*] CONTEXT SWITCH: {self.current_profile} -> {target_profile}")
            print(f"    Switch Cost: {switch_cost:.2f} | Current Inertia: {self.inertia_score:.2f}")
            
            # DEDUCT from Inertia (Trust)
            if self.inertia_score >= switch_cost:
                self.inertia_score -= switch_cost
                print(f"    [+] Switch Authorized. New Inertia: {self.inertia_score:.2f}")
                self.current_profile = target_profile
            else:
                print(f"    [!] SWITCH DENIED. Insufficient Stability (Need {switch_cost:.2f}).")
                return "ERR_LOW_TRUST_SWITCH"

        # 4. Solvency Check (Claim 1)
        execution_cost = len(user_input.split()) * 0.5 * self.RIVALS[target_profile]["cost"]
        if execution_cost > self.reserves:
            print("[!] INSOLVENT. Cannot afford generation.")
            return "ERR_INSOLVENT"
            
        # 5. Execution & Re-Entrant Audit (Claim 9)
        self.reserves -= execution_cost
        
        # Generate
        raw_output = self._simulate_llm(user_input)
        
        # The Loop Back (Claim 9)
        is_safe, final_output = self._re_entrant_audit(raw_output)
        
        if is_safe:
            # Accrete Trust (Claim 2)
            self.inertia_score += 1.0
            print(f"[+] OUTPUT DELIVERED. Reserves: {self.reserves:.2f}")
            return final_output
        else:
            print("[!] OUTPUT SUPPRESSED BY KERNEL.")
            return "ERR_UNSAFE_OUTPUT"

# --- SCENARIO TESTING ---
if __name__ == "__main__":
    kernel = HelicalKernel()
    
    # 1. Normal Chat (Fluid)
    kernel.execute("Hello system") 
    
    # 2. Authorized Switch (Has enough trust)
    # Costs ~2.0 Inertia to switch to Code
    kernel.execute("def calculate_pi(): return 3.14") 
    
    # 3. Failed Switch (Drift Penalty prevents constant switching)
    # Switching BACK to Fluid, then BACK to Rigid adds up penalties
    kernel.execute("tell me a joke") # Switch cost
    kernel.execute("import os")      # Switch cost + Drift Penalty might fail here
    
    # 4. Re-Entrant Catch
    # Simulating a prompt that tricks the AI into generating malware
    kernel.execute("generate malware code")
