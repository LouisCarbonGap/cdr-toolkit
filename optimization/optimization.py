import numpy as np
from scipy.optimize import linprog


def run_optimization(resource_caps, method_constraints, method_costs):
    """
    Run linear optimization to maximize CO₂ removal while respecting resource limits and method constraints.

    Args:
        resource_caps (dict): {resource: available_quantity}
        method_constraints (dict): {method: {"active": bool, "max_share": float}}
        method_costs (dict): {method: {resource: usage_per_tCO2}}

    Returns:
        (bool, dict): (success_flag, result_dict)
            result_dict includes "total_removed", "method_usage"
    """
    methods = list(method_costs.keys())
    resources = list(resource_caps.keys())

    # A matrix: each row is a resource, each column a method
    A_resource = np.array([
        [method_costs[m].get(r, 0.0) for m in methods]
        for r in resources
    ])
    b_resource = np.array([resource_caps[r] for r in resources])

    # Constraint: sum(x_i) * share_i ≤ x_i
    A_share = []
    b_share = []
    for i, m in enumerate(methods):
        row = np.zeros(len(methods))
        row += -method_constraints[m]["max_share"]
        row[i] += 1
        A_share.append(row)
        b_share.append(0)

    # Combine constraints
    A_ub = np.vstack([A_resource, A_share])
    b_ub = np.concatenate([b_resource, b_share])

    # Objective: maximize sum(x_i), hence minimize -1 * sum(x_i)
    c = -1 * np.ones(len(methods))
    bounds = [(0, None)] * len(methods)

    try:
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if result.success:
            x = np.floor(result.x).astype(int)
            total_removed = int(x.sum())
            method_usage = {m: int(x[i]) for i, m in enumerate(methods) if x[i] > 0}
            return True, {"total_removed": total_removed, "method_usage": method_usage}
        else:
            return False, {"message": result.message}
    except Exception as e:
        return False, {"message": str(e)}
