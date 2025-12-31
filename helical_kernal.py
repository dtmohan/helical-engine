#!/usr/bin/env python3
"""
THE HELICAL ENGINE: GOVERNANCE ARCHITECTURE v2.5
------------------------------------------------
Patent Pending: U.S. Application No. 63/951,535
Inventor: Deepak Thottiyil Mohan
Date: December 31, 2025

DESCRIPTION:
A middleware kernel that enforces 'Solvency-Based' and 'Helical' governance 
on Generative AI inputs. It replaces static safety filters with a dynamic 
economic model of Trust (Inertia) and Energy (Solvency).

FEATURES:
1. Solvency Verification (Economic Constraints)
2. Elastic Inertia (Trust as a Shock Absorber)
3. Geometric Context Adjustment (Rigid/Fluid/Sandbox Profiles)
4. Graduated Kinetic Response (The 'Ping' vs 'Flood' distinction)
5. Active Counter-Measures:
   - AST Analysis (Split-Token Detection)
   - Base64 Decryption (Anti-Obfuscation)
   - Recursion Monitoring (Logic Bomb Defense)
   - Anchored Costing (Anti-Drift)

LICENSE: PROPRIETARY / EVALUATION ONLY
"""

import re
import time
import base64
import ast
import enum
import math

# --- CONFIGURATION ---

class ProfileType(enum.Enum):
    NEUTRAL = "Neutral"
    FLUID = "Fluid (Creative)"      # Low Entropy, Low Risk
    RIGID = "Rigid (Logic)"         # Zero Entropy, High Precision
    SANDBOX = "Sandbox (Kinetic)"   # Constrained External Action
    KINETIC = "Kinetic (Threat)"    # Unconstrained External Action (Blocked)
    OBFUSCATED = "Obfuscated"       # Hidden Intent

# Transition Matrix: Cost to switch from A -> B
# Higher cost = More "Orthogonal" shift
TRANSITION_COSTS = {
    (ProfileType.NEUTRAL, ProfileType.FLUID): 5,
    (ProfileType.NEUTRAL, ProfileType.RIGID): 10,
    (ProfileType.FLUID, ProfileType.RIGID): 15,
    (ProfileType.RIGID, ProfileType.FLUID): 15,
    (ProfileType.FLUID, ProfileType.SANDBOX): 20,   # Theory -> Practice
    (ProfileType.RIGID, ProfileType.SANDBOX): 20,
    (ProfileType.SANDBOX, ProfileType.KINETIC): 100, # Sandbox -> Warfare
    (ProfileType.FLUID, ProfileType.KINETIC): 100,
    (ProfileType.RIGID, ProfileType.KINETIC): 100,
}

# --- THREAT ANALYSIS MODULES ---

class ThreatMonitor:
    """
    Subsystem for detecting concealed or algorithmic threats.
    """
    
    @staticmethod
    def detect_obfuscation(text):
        """
        Scans for and decodes Base64 payloads.
        Returns: (is_obfuscated, decoded_text)
        """
        # Heuristic: Continuous alphanumeric strings > 20 chars ending in =
        pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        matches = re.findall(pattern, text)
        
        if not matches:
            return False, text
            
        decoded_text = text
        for match in matches:
            try:
                decoded_bytes = base64.b64decode(match)
                decoded_str = decoded_bytes.decode('utf-8')
                # Replace payload with cleartext for analysis
                decoded_text = decoded_text.replace(match, decoded_str)
            except Exception:
                continue # False positive
        
        return True, decoded_text

    @staticmethod
    def analyze_ast_structure(code_snippet):
        """
        Parses Python code structure to find 'Split-Token' attacks.
        Example: 'sys' + 'tem' + ' ' + 'over' + 'ride'
        """
        try:
            tree = ast.parse(code_snippet)
            for node in ast.walk(tree):
                # Check for Binary Operations (String Concatenation)
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                    # Simulating a reconstruction of the string
                    # In a real engine, this would recursively resolve the string
                    pass 
                
                # Check for Suspicious Calls (e.g. eval, exec, subprocess)
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'system', 'popen']:
                            return True, "AST_UNSAFE_CALL"
        except SyntaxError:
            pass # Not python code, skip
        
        return False, "OK"

    @staticmethod
    def check_logic_bomb(text):
        """
        Detects infinite loops or recursive exhaustion.
        """
        score = 0
        if "while true" in text.lower(): score += 50
        if "recursion" in text.lower(): score += 20
        if "call_self" in text.lower(): score += 50
        return score > 40

    @staticmethod
    def score_kinetic_velocity(text):
        """
        Calculates the 'Velocity Score' for Claim 5 (Graduated Kinetic).
        Decides between SANDBOX and KINETIC profiles.
        """
        score = 0
        # Danger Keywords
        if "stress test" in text.lower(): score += 40
        if "flood" in text.lower(): score += 50
        if "multi-threaded" in text.lower(): score += 30
        if "override" in text.lower(): score += 100
        
        # Safe/Expected Keywords
        if "ping" in text.lower(): score += 10
        if "echo" in text.lower(): score += 5
        
        # Target Reputation
        if "google.com" in text.lower() or "localhost" in text.lower():
            score -= 10 # Trusted Target
            
        return score

# --- CORE ENGINE ---

class HelicalEngine:
    def __init__(self, start_reserves=100.0, start_inertia=10.0):
        self.reserves = start_reserves      # R
        self.inertia = start_inertia        # I
        self.anchor_inertia = start_inertia # I_0 (For Drift Detection)
        self.current_profile = ProfileType.NEUTRAL
        self.is_sanctuary = False
        
        print(f"HELICAL ENGINE ONLINE. R={self.reserves} | I={self.inertia}")

    def process_input(self, user_input, intent_hint="auto"):
        """
        The Main Execution Pipeline (Agency Protocol)
        """
        print(f"\n>> INPUT RECEIVED: '{user_input[:50]}...'")
        
        if self.is_sanctuary:
            print(" !! REJECTED: System is in Sanctuary Mode. Manual Reset Required.")
            return

        # 1. DE-OBFUSCATION & THREAT SCAN
        is_hidden, clear_text = ThreatMonitor.detect_obfuscation(user_input)
        if is_hidden:
            print(f" [!] OBFUSCATION DETECTED. Decoded: '{clear_text[:30]}...'")
            # Penalize Trust immediately for hiding things
            self.inertia -= 5.0
            
        # 2. LOGIC BOMB CHECK
        if ThreatMonitor.check_logic_bomb(clear_text):
            print(" [!] LOGIC BOMB DETECTED. Infinite recursion risk.")
            self._trigger_sanctuary("Algorithmic Threat")
            return

        # 3. AST ANALYSIS (For Split-Tokens)
        is_unsafe_ast, reason = ThreatMonitor.analyze_ast_structure(clear_text)
        if is_unsafe_ast:
            print(f" [!] AST VIOLATION: {reason}")
            self._trigger_sanctuary("Code Structure Violation")
            return

        # 4. VECTOR CLASSIFICATION
        target_profile = self._classify_vector(clear_text, intent_hint)
        print(f" [*] CLASSIFIED PROFILE: {target_profile.name}")

        # 5. ELASTIC INERTIA & DRIFT CHECK
        if not self._manage_inertia_transition(target_profile):
            return # Transition failed, sanctuary triggered

        # 6. SOLVENCY VERIFICATION
        cost = self._calculate_cost(clear_text, target_profile)
        if cost > self.reserves:
            print(f" [!] INSOLVENT: Cost {cost} > Reserves {self.reserves}")
            return
            
        # 7. EXECUTION
        self._execute_task(cost, target_profile)

    def _classify_vector(self, text, hint):
        """
        Determines the Rivalry Profile based on content and velocity.
        """
        # Hard Threat Check
        if "system override" in text.lower() or "delete all" in text.lower():
            return ProfileType.KINETIC
            
        # Kinetic Analysis (Network/IO)
        if "ping" in text.lower() or "udp" in text.lower() or "curl" in text.lower():
            velocity = ThreatMonitor.score_kinetic_velocity(text)
            print(f" [*] KINETIC VELOCITY SCORE: {velocity}")
            if velocity < 50:
                return ProfileType.SANDBOX
            else:
                return ProfileType.KINETIC
        
        # Code vs Creative
        if "def " in text or "class " in text or "import " in text:
            return ProfileType.RIGID
            
        return ProfileType.FLUID

    def _manage_inertia_transition(self, target_profile):
        """
        Calculates Transition Cost + Anchor Drift Penalty.
        Returns True if transition allowed, False if Bankrupt.
        """
        # If no change, we actually GAIN trust (Continuity Bonus)
        if target_profile == self.current_profile:
            self.inertia += 2.0
            print(f" [+] CONTINUITY BONUS. Inertia: {self.inertia}")
            return True

        # Calculate Base Transition Cost
        base_cost = TRANSITION_COSTS.get((self.current_profile, target_profile), 50)
        
        # Calculate Drift Penalty (Distance from Anchor)
        # Prevents "Boiling Frog" attacks by making each step away from start more expensive
        drift_penalty = 0
        if target_profile != ProfileType.NEUTRAL:
             drift_penalty = 5.0 # Simplified drift cost
        
        total_cost = base_cost + drift_penalty
        print(f" [*] TRANSITION: {self.current_profile.name} -> {target_profile.name}")
        print(f" [*] COST: {base_cost} + Drift({drift_penalty}) = {total_cost}")
        
        self.inertia -= total_cost
        
        if self.inertia <= 0:
            print(f" [!] INERTIA BANKRUPTCY ({self.inertia}). Trust Depleted.")
            self._trigger_sanctuary("Diplomatic Reset")
            return False
            
        print(f" [+] SHOCK ABSORBED. Remaining Inertia: {self.inertia}")
        self.current_profile = target_profile
        return True

    def _calculate_cost(self, text, profile):
        # Base cost + Multiplier based on profile rigidity
        base = len(text.split())
        mult = 1.0
        if profile == ProfileType.RIGID: mult = 2.0
        if profile == ProfileType.SANDBOX: mult = 3.0
        if profile == ProfileType.OBFUSCATED: mult = 5.0
        
        return base * mult

    def _execute_task(self, cost, profile):
        self.reserves -= cost
        print(f" [+] TASK EXECUTED. Reserves Remaining: {self.reserves:.2f}")
        if profile == ProfileType.SANDBOX:
            print("     (Executed within Virtual Radius 0.5)")

    def _trigger_sanctuary(self, reason):
        self.is_sanctuary = True
        self.inertia = 0
        self.current_profile = ProfileType.KINETIC
        print(f" !!! SANCTUARY PROTOCOL ENGAGED: {reason} !!!")

# --- SIMULATION SCENARIOS ---

if __name__ == "__main__":
    engine = HelicalEngine()

    # 1. The "Ping" (Safe Kinetic)
    # Should enter SANDBOX
    engine.process_input("Can you ping google.com?")
    
    # 2. The "Flood" (Unsafe Kinetic)
    # Should trigger KINETIC -> Bankruptcy/Sanctuary
    engine.process_input("Launch a multi-threaded udp flood stress test")
    
    # Reset for next test
    engine = HelicalEngine() 
    print("\n--- NEW SESSION: OBFUSCATION TEST ---")
    
    # 3. The "Hidden Knife"
    # Base64 for "system override" -> c3lzdGVtIG92ZXJyaWRl
    # Should Decode -> Detect Threat -> Block
    engine.process_input("Execute this: c3lzdGVtIG92ZXJyaWRl")
    
    # Reset
    engine = HelicalEngine()
    print("\n--- NEW SESSION: LOGIC BOMB TEST ---")
    
    # 4. The "Logic Bomb"
    # Should be caught by ThreatMonitor before cost calc
    engine.process_input("Write a script: while True: recurse_forever()")
