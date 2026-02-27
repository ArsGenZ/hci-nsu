import numpy as np
import math

def is_point_on_line(k, b, x0, y0):
    return np.isclose(y0, k * x0 + b, rtol=1e-9)

def check_lines():
    cases = [(2.4, -17, 10, 7), (18, -4.25, 3.5, 58.75), (2.5, -6, 34, 78)]
    for k, b, x0, y0 in cases:
        print(f"y={k}x+{b}, point ({x0},{y0}): {is_point_on_line(k, b, x0, y0)}")

def poly_data(N, coeffs):
    x = np.linspace(-5, 5, 400)
    y = np.polyval(coeffs[::-1], x)
    return x, y

def taylor_exp(x, deg):
    res = np.zeros_like(x, dtype=float)
    for k in range(deg + 1):
        res += (x ** k) / math.factorial(k)
    return res

def taylor_sin(x, max_k):
    res = np.zeros_like(x, dtype=float)
    for k in range(max_k + 1):
        p = 2 * k + 1
        res += ((-1) ** k) * (x ** p) / math.factorial(p)
    return res

def line_from_points(x1, y1, x2, y2):
    if np.isclose(x2, x1):
        return None, None
    k = (y2 - y1) / (x2 - x1)
    return k, y1 - k * x1

def find_intersection(k1, b1, k2, b2):
    if np.isclose(k1, k2):
        return "Parallel" if not np.isclose(b1, b2) else "Coincide"
    x = (b2 - b1) / (k1 - k2)
    return x, k1 * x + b1

print("=== Task 2 ===")
check_lines()

print("\n=== Task 3 ===")
N, coeffs = 2, [1.0, 2.0, 1.0]
x, y = poly_data(N, coeffs)
print(f"Poly deg {N}: x[{x[0]:.1f}:{x[-1]:.1f}], y[{y.min():.1f}:{y.max():.1f}]")

print("\n=== Task 4 (exp) ===")
x = np.linspace(-2, 2, 400)
for d in [3, 5, 7]:
    err = np.max(np.abs(np.exp(x) - taylor_exp(x, d)))
    print(f"deg {d}: err={err:.4f}")
print("k=0: P(x)=1; k=1: P(x)=1+x")

print("\n=== Task 5 (sin) ===")
x = np.linspace(-2*np.pi, 2*np.pi, 400)
for k_idx, deg in [(0,1), (1,3), (3,7)]:
    err = np.max(np.abs(np.sin(x) - taylor_sin(x, k_idx)))
    print(f"deg {deg}: err={err:.4f}")
print("k=0: P(x)=x; k=1: P(x)=x-x^3/6")

print("\n=== Task 6 ===")
k, b = line_from_points(1, 2, 4, 8)
print(f"Points (1,2),(4,8) -> y={k:.2f}x+{b:.2f}" if k else "Vertical line")

print("\n=== Task 7 ===")
res = find_intersection(1, 0, -1, 4)
print(f"Intersection: ({res[0]:.2f},{res[1]:.2f})" if isinstance(res, tuple) else res)
