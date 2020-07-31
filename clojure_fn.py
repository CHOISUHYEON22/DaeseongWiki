def group_by(f, coll) -> dict: return {j : tuple(k for k in coll if f(k) == j) for j in {f(i) for i in coll}}
