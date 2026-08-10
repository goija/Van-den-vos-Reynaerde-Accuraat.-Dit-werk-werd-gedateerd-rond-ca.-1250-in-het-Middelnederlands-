import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import struct
import pandas as pd

# =============================================================================
# DEEL 1: COLLATZ SIMULATOR
# =============================================================================

class CollatzSimulator:
    """Simuleert Collatz-trajecten voor positieve en negatieve gehele getallen."""
    
    def __init__(self):
        self.visited_cycles = {}
    
    def next_collatz_step(self, n: int) -> int:
        """Bereken volgende Collatz-stap."""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1
    
    def trajectory(self, n: int, max_steps: int = 10000) -> List[int]:
        """
        Genereer Collatz-traject tot 1 (voor n>0) of detecteer cyclus (voor n<0).
        
        Args:
            n: Startwaarde (kan negatief zijn)
            max_steps: Maximum aantal stappen
            
        Returns:
            Lijst van waarden in het traject
        """
        trajectory = [n]
        visited = {n}
        
        for _ in range(max_steps):
            current = trajectory[-1]
            
            # Stop als we bij 1 komen (positieve gevallen)
            if current == 1:
                break
            
            # Detecteer cyclus (negatieve gevallen)
            next_val = self.next_collatz_step(current)
            
            if next_val in visited:
                # Cyclus gevonden!
                break
            
            trajectory.append(next_val)
            visited.add(next_val)
        
        return trajectory
    
    def find_cycle(self, n: int, max_steps: int = 1000) -> Tuple[List[int], bool]:
        """
        Zoek een gesloten cyclus voor negatieve startwaarden.
        
        Args:
            n: Negatieve startwaarde
            max_steps: Maximum iteraties
            
        Returns:
            (cyclus_lijst, gevonden)
        """
        if n > 0:
            return [], False
        
        visited = {}
        trajectory = []
        current = n
        
        for step in range(max_steps):
            if current in visited:
                # Cyclus gevonden!
                cycle_start = visited[current]
                cycle = trajectory[cycle_start:]
                return cycle, True
            
            visited[current] = step
            trajectory.append(current)
            current = self.next_collatz_step(current)
        
        return [], False
    
    def analyze_trajectory(self, n: int) -> Dict:
        """
        Analyseer Collatz-traject statistieken.
        
        Returns:
            Dictionary met statistieken
        """
        traj = self.trajectory(n)
        
        if n < 0:
            cycle, found = self.find_cycle(n)
            return {
                'start': n,
                'total_steps': len(traj),
                'min_value': min(traj),
                'max_value': max(traj),
                'cycle_found': found,
                'cycle_length': len(cycle) if found else 0,
                'cycle': cycle if found else []
            }
        else:
            return {
                'start': n,
                'total_steps': len(traj) - 1,
                'peak': max(traj),
                'peak_position': traj.index(max(traj)),
                'converges_to_one': traj[-1] == 1,
                'final_trajectory': traj[-5:]
            }
    
    def visualize_trajectory(self, n: int, save_path: Optional[str] = None):
        """Visualiseer Collatz-traject als tijdserie."""
        traj = self.trajectory(n)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(range(len(traj)), traj, 'o-', linewidth=2, markersize=4, 
                color='#6d4aff')
        ax.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Doel (n=1)')
        
        # Markeer piek
        peak = max(traj)
        peak_idx = traj.index(peak)
        ax.annotate(f'Piek: {peak}', xy=(peak_idx, peak), 
                   xytext=(peak_idx+10, peak+50),
                   arrowprops=dict(arrowstyle='->', color='black'))
        
        ax.set_xlabel('Stap', fontsize=12)
        ax.set_ylabel('Waarde', fontsize=12)
        ax.set_title(f'Collatz-traject voor n={n}', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


# =============================================================================
# DEEL 2: THERMODYNAMISCHE CALCULATOR
# =============================================================================

class ThermodynamicsCalculator:
    """Bereken Gibbs vrije energie en evenwichtstemperaturen."""
    
    def __init__(self, delta_H: float = -128300, reference_T: float = 298.15):
        """
        Initialiseer met standaard waarden.
        
        Args:
            delta_H: Enthalpieverandering in J/mol
            reference_T: Referentie temperatuur in K
        """
        self.delta_H = delta_H
        self.reference_T = reference_T
        self.R = 8.314  # Gas constante J/(mol·K)
    
    def calculate_delta_G(self, delta_S: float, temperature: float) -> float:
        """
        Bereken ΔG° = ΔH° - TΔS°
        
        Args:
            delta_S: Entropieverandering in J/(K·mol)
            temperature: Temperatuur in K
            
        Returns:
            ΔG° in J/mol
        """
        return self.delta_H - temperature * delta_S
    
    def calculate_equilibrium_temperature(self, delta_S: float) -> float:
        """
        Bereken T_eq waar ΔG° = 0
        
        T_eq = ΔH° / ΔS°
        
        Args:
            delta_S: Entropieverandering in J/(K·mol)
            
        Returns:
            Evenwichtstemperatuur in K
        """
        if delta_S == 0:
            raise ValueError("ΔS° kan niet 0 zijn (deling door nul)")
        return self.delta_H / delta_S
    
    def calculate_equilibrium_constant(self, delta_G: float, temperature: float) -> float:
        """
        Bereken evenwichtsconstante K = exp(-ΔG°/RT)
        
        Args:
            delta_G: Gibbs vrije energie in J/mol
            temperature: Temperatuur in K
            
        Returns:
            Evenwichtsconstante K
        """
        return np.exp(-delta_G / (self.R * temperature))
    
    def analyze_spontaneity(self, delta_S: float, temperature_range: Tuple[float, float] = (0, 2000)) -> Dict:
        """
        Analyseer spontaniteit over temperatuurbereik.
        
        Args:
            delta_S: Entropieverandering in J/(K·mol)
            temperature_range: (min_T, max_T) in K
            
        Returns:
            Dictionary met analyse resultaten
        """
        T_min, T_max = temperature_range
        T_eq = self.calculate_equilibrium_temperature(delta_S)
        
        temperatures = np.linspace(T_min, T_max, 100)
        delta_G_values = [self.calculate_delta_G(delta_S, T) for T in temperatures]
        
        return {
            'delta_S': delta_S,
            'T_eq': T_eq,
            'spontaneous_below_Teq': self.delta_H < 0 and delta_S < 0,
            'delta_G_at_298K': self.calculate_delta_G(delta_S, 298.15),
            'delta_G_at_Teq': 0,
            'K_at_298K': self.calculate_equilibrium_constant(
                self.calculate_delta_G(delta_S, 298.15), 298.15),
            'temperatures': temperatures,
            'delta_G_values': delta_G_values
        }
    
    def compare_scenarios(self, delta_S_list: List[float]) -> pd.DataFrame:
        """
        Vergelijk meerdere ΔS° scenario's.
        
        Args:
            delta_S_list: Lijst van ΔS° waarden in J/(K·mol)
            
        Returns:
            Pandas DataFrame met vergelijking
        """
        try:
            # Removed the internal import of pandas
            pass
        except ImportError:
            print("Pandas nodig voor deze functionaliteit. Install met: pip install pandas")
            return None
        
        data = []
        for delta_S in delta_S_list:
            T_eq = self.calculate_equilibrium_temperature(delta_S)
            delta_G = self.calculate_delta_G(delta_S, 298.15)
            K = self.calculate_equilibrium_constant(delta_G, 298.15)
            
            data.append({
                'ΔS° (J/K·mol)': delta_S,
                'ΔG° (kJ/mol)': delta_G / 1000,
                'T_eq (K)': T_eq,
                'K (298K)': K,
                'Spontaan bij 298K': delta_G < 0
            })
        
        return pd.DataFrame(data)
    
    def visualize_gibbs_curve(self, delta_S: float, 
                             temperature_range: Tuple[float, float] = (0, 2000)):
        """Visualiseer ΔG° vs Temperatuur curve."""
        analysis = self.analyze_spontaneity(delta_S, temperature_range)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot ΔG° curve
        ax.plot(analysis['temperatures'], 
               [g / 1000 for g in analysis['delta_G_values']],  # Naar kJ/mol
               linewidth=3, color='#6d4aff')
        
        # Shade spontane zone (ΔG° < 0)
        T_eq = analysis['T_eq']
        mask_spontaneous = analysis['temperatures'] <= T_eq
        ax.fill_between(analysis['temperatures'], 
                       [g / 1000 for g in analysis['delta_G_values']],
                       where=mask_spontaneous,
                       color='#4CAF50', alpha=0.3, label='Spontaan (ΔG° < 0)')
        
        # Shade niet-spontane zone (ΔG° > 0)
        mask_non_spontaneous = analysis['temperatures'] > T_eq
        ax.fill_between(analysis['temperatures'], 
                       [g / 1000 for g in analysis['delta_G_values']],
                       where=mask_non_spontaneous,
                       color='#FF5722', alpha=0.3, label='Niet-spontaan (ΔG° > 0)')
        
        # Marker T_eq
        ax.axvline(x=T_eq, color='#6d4aff', linestyle='--', linewidth=2,
                  alpha=0.7, label=f'T_eq = {T_eq:.0f} K')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        
        ax.set_xlabel('Temperatuur (K)', fontsize=12)
        ax.set_ylabel('ΔG° (kJ/mol)', fontsize=12)
        ax.set_title(f'Gibbs Vrije Energie vs Temperatuur\nΔS° = {delta_S} J/(K·mol)', 
                    fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.show()


# =============================================================================
# DEEL 3: IEEE 754 FLOAT CONVERTER
# =============================================================================

class IEEE754Converter:
    """Converteer decimale getallen naar IEEE 754 single precision."""
    
    @staticmethod
    def decimal_to_bits(value: float) -> str:
        """
        Converteer decimaal float naar 32-bit IEEE 754 bits.
        
        Args:
            value: Decimaal getal
            
        Returns:
            String van 32 bits
        """
        packed = struct.pack('f', value)  # 32-bit float
        integer = struct.unpack('I', packed)[0]  # Naar unsigned int
        return f'{integer:032b}'
    
    @staticmethod
    def decimal_to_hex(value: float) -> str:
        """
        Converteer decimaal float naar hexadecimale representatie.
        
        Args:
            value: Decimaal getal
            
        Returns:
            Hex string (bijv. '0xC2B60000')
        """
        packed = struct.pack('f', value)
        integer = struct.unpack('I', packed)[0]
        return f'0x{integer:08X}'
    
    @staticmethod
    def bits_to_decimal(bits: str) -> float:
        """
        Converteer 32-bit bits terug naar decimaal.
        
        Args:
            bits: 32-char string van 0'en en 1'en
            
        Returns:
            Decimaal float
        """
        integer = int(bits, 2)
        packed = struct.pack('I', integer)
        return struct.unpack('f', packed)[0]
    
    @staticmethod
    def parse_ieee754(value: float) -> Dict:
        """
        Parse IEEE 754 representation naar componenten.
        
        Args:
            value: Decimaal getal
            
        Returns:
            Dictionary met sign, exponent, mantissa
        """
        bits = IEEE754Converter.decimal_to_bits(value)
        
        sign_bit = int(bits[0])
        exponent_bits = bits[1:9]
        mantissa_bits = bits[9:]
        
        exponent_raw = int(exponent_bits, 2)
        exponent_actual = exponent_raw - 127  # Bias correction
        
        # Mantissa with implicit leading 1
        mantissa_fraction = sum(int(b) * 2**(-(i+1)) 
                               for i, b in enumerate(mantissa_bits))
        mantissa = 1 + mantissa_fraction
        
        reconstructed = ((-1) ** sign_bit) * mantissa * (2 ** exponent_actual)
        
        return {
            'original': value,
            'bits': bits,
            'sign_bit': sign_bit,
            'sign': '-' if sign_bit else '+',
            'exponent_raw': exponent_raw,
            'exponent_actual': exponent_actual,
            'mantissa_bits': mantissa_bits,
            'mantissa_value': mantissa,
            'reconstructed': reconstructed,
            'error': abs(value - reconstructed),
            'hex': IEEE754Converter.decimal_to_hex(value)
        }
    
    @staticmethod
    def visualize_bit_layout(value: float):
        """Visualiseer IEEE 754 bit-indeling."""
        info = IEEE754Converter.parse_ieee754(value)
        
        fig, ax = plt.subplots(figsize=(14, 4))
        
        # Create bit boxes
        bit_positions = list(range(32))
        bit_labels = list(info['bits'])
        
        colors = ['#FF6B6B' if bit_labels[i] == '1' else '#E0E0E0' 
                  for i in bit_positions]
        
        for i, (pos, label, color) in enumerate(zip(bit_positions, bit_labels, colors)):
            # Group by component
            if pos == 0:
                component = 'Sign'
            elif pos < 9:
                component = 'Exponent'
            else:
                component = 'Mantissa'
            
            ax.add_patch(plt.Rectangle((pos, 0), 1, 1, 
                                       facecolor=color, 
                                       edgecolor='#6d4aff',
                                       linewidth=1.5))
            ax.text(pos + 0.5, 0.5, label, ha='center', va='center',
                   fontsize=10, fontweight='bold')
        
        # Add component labels
        ax.text(0.5, 1.2, 'Sign (1 bit)', ha='center', fontsize=12, fontweight='bold',
               color='#FF6B6B')
        ax.text(4.5, 1.2, 'Exponent (8 bits)', ha='center', fontsize=12, fontweight='bold',
               color='#4CAF50')
        ax.text(20, 1.2, 'Mantissa (23 bits)', ha='center', fontsize=12, fontweight='bold',
               color='#2196F3')
        
        ax.set_xlim(-1, 33)
        ax.set_ylim(-0.5, 1.5)
        ax.axis('off')
        
        ax.set_title(f'IEEE 754 Single Precision: {value}\n{info["hex"]}',
                    fontsize=16, pad=20)
        
        plt.tight_layout()
        plt.show()
        
        # Print details
        print("=" * 70)
        print(f"IEEE 754 Analyse voor: {value}")
        print("=" * 70)
        print(f"Hexadecimaal:      {info['hex']}")
        print(f"Bits:              {info['bits']}")
        print(f"Sign:              {info['sign']} ({info['sign_bit']})")
        print(f"Exponent (raw):    {info['exponent_raw']}")
        print(f"Exponent (actueel): {info['exponent_actual']}")
        print(f"Mantissa:          {info['mantissa_value']:.6f}")
        print(f"Herbouwd:          {info['reconstructed']:.6f}")
        print(f"Afrondingsfout:    {info['error']:.2e}")
        print("=" * 70)


# =============================================================================
# DEEL 4: UNIFIED ANALYZER
# =============================================================================

class UnifiedAnalyzer:
    """Integreert alle drie domeinen voor cross-domain analyse."""
    
    def __init__(self):
        self.collatz = CollatzSimulator()
        self.thermo = ThermodynamicsCalculator()
        self.ieee = IEEE754Converter()
    
    def analyze_number(self, number: int):
        """
        Voer complete analyse uit voor één getal.
        
        Args:
            number: Geheel getal (positief of negatief)
        """
        print("=" * 80)
        print(f"UNIVERSELE ANALYSE VOOR GETAL: {number}")
        print("=" * 80)
        
        # 1. Collatz analyse
        print("\n🔢 COLLA TZ ANALYSE:")
        print("-" * 80)
        collatz_result = self.collatz.analyze_trajectory(number)
        print(json.dumps(collatz_result, indent=2, default=str))
        
        if number < 0:
            self.collatz.visualize_trajectory(number)
        
        # 2. Thermodynamische analyse (als ΔS° = number)
        if number != 0:
            print(f"\n⚗️ THERMODYNAMISCHE ANALYSE (ΔS° = {number} J/K·mol):")
            print("-" * 80)
            thermo_result = self.thermo.analyze_spontaneity(float(number))
            print(f"  T_eq: {thermo_result['T_eq']:.2f} K")
            print(f"  ΔG° bij 298K: {thermo_result['delta_G_at_298K']/1000:.2f} kJ/mol")
            print(f"  Evenwichtsconstante K: {thermo_result['K_at_298K']:.2e}")
            print(f"  Spontaan bij 298K: {'Ja' if thermo_result['delta_G_at_298K'] < 0 else 'Nee'}")
            
            self.thermo.visualize_gibbs_curve(float(number))
        
        # 3. IEEE 754 analyse
        print(f"\n💾 IEEE 754 REPRESENTATIE:")
        print("-" * 80)
        ieee_info = self.ieee.parse_ieee754(float(number))
        print(f"  Hex: {ieee_info['hex']}")
        print(f"  Bits: {ieee_info['bits']}")
        print(f"  Fout: {ieee_info['error']:.2e}")
        
        self.ieee.visualize_bit_layout(float(number))
        
        print("=" * 80)
        print("ANALYSE VOLTOOID")
        print("=" * 80)


# =============================================================================
# MAIN - INTERACTIEVE DEMONSTRATIE
# =============================================================================

if __name__ == "__main__":
    import json
    
    print("🎯 UNIFIED NUMBER ANALYSIS SYSTEM")
    print("=" * 80)
    
    # Demonstration for number -91
    analyzer = UnifiedAnalyzer()
    analyzer.analyze_number(-91)
    
    # Bonus: Compare multiple numbers
    print("\n📊 VERGELIJKING MEERDERE SCENARIO'S:")
    print("=" * 80)
    
    thermo = ThermodynamicsCalculator()
    scenarios = [-91, -159.5, -160.5]
    df = thermo.compare_scenarios(scenarios)
    
    if df is not None:
        print(df.to_string(index=False))
    
    # Interactive mode
    print("\n🔧 INTERACTIEVE MODE")
    print("-" * 80)
    print("Voer een getal in voor analyse (of 'quit' om te stoppen):")
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            if user_input.lower() == 'quit':
                print("Tot ziens!")
                break
            
            number = int(user_input)
            analyzer.analyze_number(number)
            
        except ValueError:
            print(" Ongeldige invoer. Voer een geheel getal in.")
        except KeyboardInterrupt:
            print("\nProgramma onderbroken.")
            break
