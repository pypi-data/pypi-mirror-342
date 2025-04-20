# 🧺 get_lunchbox
Easy imports in Python — simplify your workflow by dynamically importing modules with optional aliases.

## Update
- adeed `get_lazy_lunchbox()` which saves memory, by importing a module when it's used

## 🚀 Usage
```python
from get_lunchbox import get_lunchbox

lb = get_lunchbox(
    ("math",),
    ("numpy", "np"),
    ("matplotlib.pyplot", "plt")
)

print(lb.math.sqrt(25))      # 5.0
print(lb.np.array([1, 2, 3]))  # numpy array
lb.plt.plot([1, 2], [3, 4])    # matplotlib plot
lb.plt.show()
```
### Installation Process
```bash
pip install get_lunchbox