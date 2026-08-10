Hier is de overzichtelijke studiegids met de theorie, uitdagende opgaven en programmeervoorbeelden in Python en Buildroot-compatibele C.

---

# Studiegids: Recursie, Torens van Hanoi en de Fibonacci-rij

> **Inhoudsopgave**
> 1. Inleiding & Fundamenten van Recursie
> 2. Klassieker 1: De Torens van Hanoi
> 3. Klassieker 2: De Fibonacci-rij & Binet's Formule
> 4. Cheat-sheet: Wiskundige Notatie in Code
> 5. Uitdagende Opgaven
> 
> 

---

## 1. Inleiding & Fundamenten van Recursie

Recursie is een techniek waarbij een probleem wordt opgelost door het op te splitsen in kleinere instanties van hetzelfde probleem. Een correcte recursieve definitie bestaat altijd uit twee componenten:

1. **De Base Case (Beginvoorwaarde):** Het stoppersmechanisme dat voorkomt dat de functie oneindig doorloopt (infinite recursion / stack overflow).
2. **De Recurrence Relation (Recursieve Stap):** De regel die de huidige staat uitdrukt in kleinere subtaken.

---

## 2. Klassieker 1: De Torens van Hanoi

Voor $n$ schijven is de recursieve formule:


$$T_n = 2T_{n-1} + 1 \quad \text{met } T_1 = 1$$

De expliciete (gesloten) formule is:


$$T_n = 2^n - 1$$

### Programmeervoorbeeld (C / Python)

In een minimalistische embedded of UNIX-omgeving wil je iteratieve of recursieve routines efficiënt schrijven. Hier is de C-implementatie om de daadwerkelijke zetten te genereren:

```c
#include <stdio.h>

void hanoi(int n, char van, char naar, char hulp) {
    if (n == 1) {
        printf("Verplaats schijf 1 van pin %c naar pin %c\n", van, naar);
        return;
    }
    hanoi(n - 1, van, hulp, naar);
    printf("Verplaats schijf %d van pin %c naar pin %c\n", n, van, naar);
    hanoi(n - 1, hulp, naar, van);
}

int main() {
    int n = 3;
    hanoi(n, 'A', 'C', 'B');
    return 0;
}

```

---

## 3. Klassieker 2: De Fibonacci-rij & Binet's Formule

De lineaire homogene differentievergelijking van graad 2:


$$f_n = f_{n-1} + f_{n-2} \quad \text{met } f_0 = 0, f_1 = 1$$

De karakteristieke vergelijking $x^2 - x - 1 = 0$ leidt via de wortels $\alpha = \frac{1+\sqrt{5}}{2}$ en $\beta = \frac{1-\sqrt{5}}{2}$ tot de **Binet-formule**:


$$f_n = \frac{1}{\sqrt{5}} \left[ \left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n \right]$$

### Programmeervoorbeeld (Python met memoortisatie / iteratie)

Zuivere recursie voor Fibonacci is inefficiënt ($O(2^n)$) vanwege dubbele berekeningen. Een iteratieve aanpak of matrix-exponentiatie verdient de voorkeur:

```python
def fibonacci_binet(n: int) -> int:
    import math
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    return round((phi**n - psi**n) / sqrt5)

# Test voor n = 10
print(f"Fibonacci(10) via Binet = {fibonacci_binet(10)}")  # Output: 55

```

---

## 4. Cheat-sheet: Wiskundige Notatie in Code

| Wiskundig Symbool / Notatie | LaTeX / Expressie | Python / Programmeerequivalent |
| --- | --- | --- |
| **Sommatie** | $\sum_{i=1}^{n} i$ | `sum(range(1, n + 1))` |
| **Machtsverheffing** | $x^n$ | `x ** n` of `math.pow(x, n)` |
| **Vierkantswortel** | $\sqrt{x}$ | `math.sqrt(x)` of `x ** 0.5` |
| **Vloerfunctie (Floor)** | $\lfloor x \rfloor$ | `math.floor(x)` of `int(x)` |
| **Modulus / Rest** | $a \pmod b$ | `a % b` |

---

## 5. Uitdagende Opgaven

1. **Opgave 1 (Hanoi uitbreiding):** Pas de recursieve formule van de Torens van Hanoi aan voor het geval er **vier** pinnen in plaats van drie pinnen beschikbaar zijn (het Frame-Stewart-algoritme). Wat gebeurt er met de efficiëntie?
2. **Opgave 2 (Inhomogene recursie):** Los de volgende recurrenierelatie op via backtracking:

$$S_n = 3S_{n-1} + 2 \quad \text{met } S_0 = 1$$


3. **Opgave 3 (Fibonacci complexiteit):** Schrijf een recursieve functie in C voor Fibonacci zonder memoortisatie en bewijs via een boomdiagram waarom de tijdscomplexiteit exponentieel ($O(2^n)$) groeit.
