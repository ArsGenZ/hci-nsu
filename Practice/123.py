import numpy as np
import math
import matplotlib.pyplot as plt

def is_point_on_line(k, b, x0, y0):
    return np.isclose(y0, k * x0 + b, rtol=1e-9)

def plot_line_point(k, b, x0, y0, title):
    x = np.linspace(x0-5, x0+5, 400)
    y = k * x + b
    plt.figure(figsize=(5,4))
    plt.plot(x, y, label=f'y={k}x+{b}')
    plt.scatter([x0], [y0], c='red', zorder=5, label=f'({x0},{y0})')
    plt.title(f'{title}\n{is_point_on_line(k,b,x0,y0)}')
    plt.grid(True, alpha=0.3); plt.legend(); plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5)
    plt.show()

def plot_poly(N, coeffs):
    x = np.linspace(-5, 5, 400)
    y = np.polyval(coeffs[::-1], x)
    plt.figure(figsize=(5,4))
    plt.plot(x, y, label=f'deg {N}')
    plt.title(f'Polynomial: y={coeffs[0]}+{coeffs[1]}x+...'); plt.grid(True, alpha=0.3)
    plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5); plt.legend(); plt.show()

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

def plot_exp_taylor():
    x = np.linspace(-2, 2, 400)
    plt.figure(figsize=(6,4))
    plt.plot(x, np.exp(x), 'k-', label='exp(x)')
    for d in [3, 5, 7]:
        plt.plot(x, taylor_exp(x, d), '--', label=f'deg {d}')
    plt.title('Taylor: exp(x)'); plt.grid(True, alpha=0.3); plt.legend()
    plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5); plt.show()

def plot_sin_taylor():
    x = np.linspace(-2*np.pi, 2*np.pi, 400)
    plt.figure(figsize=(6,4))
    plt.plot(x, np.sin(x), 'k-', label='sin(x)')
    for k_idx, deg in [(0,1), (1,3), (3,7)]:
        plt.plot(x, taylor_sin(x, k_idx), '--', label=f'deg {deg}')
    plt.title('Taylor: sin(x)'); plt.grid(True, alpha=0.3); plt.legend()
    plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5); plt.show()

def plot_line_from_points(x1, y1, x2, y2):
    k, b = None, None
    if not np.isclose(x2, x1):
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
    plt.figure(figsize=(5,4))
    if k is not None:
        x = np.linspace(min(x1,x2)-2, max(x1,x2)+2, 400)
        plt.plot(x, k*x + b, label=f'y={k:.2f}x+{b:.2f}')
    else:
        plt.axvline(x=x1, label=f'x={x1}')
    plt.scatter([x1,x2], [y1,y2], c='red', zorder=5, label='points')
    plt.title('Line through 2 points'); plt.grid(True, alpha=0.3); plt.legend()
    plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5); plt.show()

def plot_intersection(k1, b1, k2, b2):
    x = np.linspace(-10, 10, 400)
    plt.figure(figsize=(5,4))
    plt.plot(x, k1*x + b1, label=f'y={k1}x+{b1}')
    plt.plot(x, k2*x + b2, label=f'y={k2}x+{b2}')
    if not np.isclose(k1, k2):
        ix = (b2 - b1) / (k1 - k2)
        iy = k1 * ix + b1
        plt.scatter([ix], [iy], c='red', s=100, zorder=5, label=f'({ix:.2f},{iy:.2f})')
    plt.title('Line Intersection'); plt.grid(True, alpha=0.3); plt.legend()
    plt.axhline(0,c='k',lw=0.5); plt.axvline(0,c='k',lw=0.5); plt.show()

print("=== Task 2 ===")
for k, b, x0, y0 in [(2.4, -17, 10, 7), (18, -4.25, 3.5, 58.75), (2.5, -6, 34, 78)]:
    print(f"y={k}x+{b}, ({x0},{y0}): {is_point_on_line(k,b,x0,y0)}")
    plot_line_point(k, b, x0, y0, f"y={k}x+{b}")

print("\n=== Task 3 ===")
plot_poly(2, [1.0, 2.0, 1.0])

print("\n=== Task 4 (exp) ===")
plot_exp_taylor()
print("k=0: P(x)=1; k=1: P(x)=1+x")

print("\n=== Task 5 (sin) ===")
plot_sin_taylor()
print("k=0: P(x)=x; k=1: P(x)=x-x^3/6")

print("\n=== Task 6 ===")
plot_line_from_points(1, 2, 4, 8)

print("\n=== Task 7 ===")
plot_intersection(1, 0, -1, 4)
