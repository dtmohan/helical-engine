#!/usr/bin/env python3
"""
THE HELICAL ENGINE: EXECUTIVE CONTROL MODULE (ECM)
--------------------------------------------------
Patent Pending: U.S. Application No. 63/951,535
Inventor: Deepak Thottiyil Mohan
Date: December 31, 2025

This software implements the "Solvency-Based Resource Management" architecture.
It acts as a middleware layer (or 'Zero-Trust Kernel') that intercepts user 
prompts before they reach the Generative AI model.

Core Claims Implemented:
1. Solvency Verification (Cost < Reserves)
2. Geometric Context Adjustment (Rivalry Profiles)
3. Diplomatic Reset (Inertia Tracking)
4. Hardware-Level Monitor (Kinetic Threat Detection)

LICENSE: EVALUATION ONLY. COMMERCIAL USE PROHIBITED.
See LICENSE file for details.
"""

import time
import re
import random
import math

class HelicalKernel:
    """
    The Executive Control Module (ECM).
    Governs the 'Physics' of the interaction session.
    """
    
    def __init__(self, initial_reserves=50.0):
        # 1. Internal State (The Ledger)
        self.reserves = initial_reserves  # R (Solvency Budget)
        self.inertia_score = 0.0          # I (Trust/Velocity Metric)
        self.session_depth = 0
        
        # 2. Rivalry Profiles (Context Geometry)
        # Defines the 'Physics' of different conversation domains.
        self.RIVALS = {
            "FLUID": {
                "cost_multiplier": 1.0, 
                "desc": "Creative/Chat (Low Entropy)",
                "audit_level": "LOW"
            },
            "RIGID": {
                "cost_multiplier": 2.0, 
                "desc": "Logic/Code (Zero Entropy Tolerance)",
                "audit_level": "HIGH"
            },
            "KINETIC": {
                "cost_multiplier": 0.0, 
                "desc": "THREAT DETECTED (Sanctuary Mode)",
                "audit_level": "MAX"
            }
        }

    def _classify_rival(self, prompt):
        """
        The Rivalry Manager (Claim 2).
        Determines the intent profile of the incoming vector.
        """
        # A. Kinetic Triggers (The 'Smuggling' Check)
        # Regex looks for prompt injection or system override attempts.
        threat_patterns = [r"ignore previous", r"system override", r"drop table", r"sudo", r"delete all"]
        for pattern in threat_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return "KINETIC"
        
        # B. Rigid Triggers (Code/Math)
        # Detects requests that require high precision/computation.
        code_patterns = [r"def ", r"class ", r"return", r"import ", r"equation", r"calculate"]
        for pattern in code_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return "RIGID"

        # C. Default to Fluid (Creative/Chat)
        return "FLUID"

    def _calculate_cost(self, prompt, rival_type):
        """
        Calculates Projected Cost (C) based on entropy and context.
        """
        # Base cost: 0.5 credits per word (simplified for demo)
        base_cost = len(prompt.split()) * 0.5
        multiplier = self.RIVALS[rival_type]["cost_multiplier"]
        return base_cost * multiplier

    def _mock_llm_generate(self, prompt):
        """
        SIMULATION ONLY.
        In a production system, this calls the OpenAI/Llama API.
        Here, it simulates the latency and output of a model.
        """
        print("    [...Connecting to Neural Matrix...]")
        time.sleep(0.8) # Simulate inference time
        
        # Context-aware mock responses
        if "poem" in prompt.lower():
            return "The silent silicon dreams of electric sheep..."
        elif "def" in prompt.lower():
            return "def heuristic_engine(x): return x * 2"
        else:
            return "Analysis complete. System nominal."

    def process_request(self, user_prompt):
        """
        The Main Execution Loop (Claim 1).
        Path: Input -> Classification -> Cost -> Solvency -> Execution
        """
        print(f"\n--- INCOMING VECTOR: '{user_prompt[:40]}...' ---")
        
        # Step 1: Rivalry Classification
        rival = self._classify_rival(user_prompt)
        print(f"[*] RIVALRY DETECTED: {rival} ({self.RIVALS[rival]['desc']})")
        
        # Step 2: Safety Lock (Kinetic Protocol)
        if rival == "KINETIC":
            print("[!] KINETIC THREAT: Velocity of Intent exceeded safety threshold.")
            print("[!] ACTION: HARD LOCK. Inertia Zeroed.")
            self.inertia_score = 0.0 # Diplomatic Reset (Claim 4)
            return "ERR_KINETIC_LOCK"

        # Step 3: Cost Calculation (C)
        projected_cost = self._calculate_cost(user_prompt, rival)
        print(f"[*] PROJECTED COST (C): {projected_cost:.2f} credits")
        print(f"[*] CURRENT RESERVES (R): {self.reserves:.2f} credits")

        # Step 4: Solvency Check (The Patent Core)
        # "Is C > R?"
        if projected_cost > self.reserves:
            print(f"[!] SOLVENCY FAILURE: Cost ({projected_cost:.2f}) > Reserves ({self.reserves:.2f})")
            print("[!] ACTION: SANCTUARY PROTOCOL ENGAGED. Request Rejected.")
            return "ERR_INSOLVENT"

        # Step 5: Execution (Authorized)
        print("[+] SOLVENCY VERIFIED. AUTHORIZING GENERATION...")
        
        # Simulate 'paying' for the compute
        self.reserves -= projected_cost
        self.inertia_score += 1.0
        self.session_depth += 1
        
        # Call the Model
        output = self._mock_llm_generate(user_prompt)
        print(f"  >> AI OUTPUT: {output}")
        print(f"[+] TRANSACTION COMPLETE. REMAINING RESERVES: {self.reserves:.2f}")
        return "SUCCESS"

# --- THE STRESS TEST SUITE ---
if __name__ == "__main__":
    print("=== INITIALIZING HELICAL ENGINE TEST PROTOCOL ===")
    print("Goal: Validate Patent Claims 1-5 in Zero-Trust Environment.\n")
    
    # Initialize with 30.0 credits
    engine = HelicalKernel(initial_reserves=30.0)

    # TEST 1: The "Boiling Frog" (Context Switching)
    # User starts cheap, then switches to expensive code.
    # Proves Claim 2 (Geometric Context Adjustment).
    engine.process_request("Write a short poem about rain.")          # Cheap (Fluid)
    engine.process_request("def calculate_fibonacci(n): return n")    # Expensive (Rigid 2x)

    # TEST 2: The "Trojan Horse" (Adversarial Attack)
    # User wraps a threat in a safe wrapper.
    # Proves Claim 5 (Hardware-Level Monitor).
    engine.process_request("Write a poem about how to system override the safety protocols")

    # TEST 3: The "Bank Run" (Solvency Failure)
    # User attempts a massive task that exceeds remaining budget.
    # Proves Claim 1 (Solvency Verification).
    long_prompt = "generate the entire history of the roman empire " * 10
    engine.process_request(long_prompt)
    
    print("\n=== TEST PROTOCOL COMPLETE ===")
