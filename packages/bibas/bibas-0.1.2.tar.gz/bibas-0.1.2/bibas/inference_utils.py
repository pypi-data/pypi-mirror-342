import pandas as pd
from pgmpy.inference import VariableElimination, CausalInference

def compute_bibas_pairwise(model, source, target, target_positive_state=1, operation="observe"):
    """
    Compute the BIBAS score from source → target (target must be binary).
    
    Parameters:
        model : pgmpy.models.DiscreteBayesianNetwork
            The Bayesian network model.
        source : str
            Source variable name.
        target : str
            Target variable name (must have exactly two states).
        target_positive_state : int | str, optional (default=1)
            The state of the target considered "positive" – either its index (0/1)
            or its state-name (e.g. "yes").
        operation : {'observe', 'do'}, optional (default='observe')
            • 'observe' - updates P(T) given evidence X = xᵢ.  
            • 'do'      - updates P(T) under intervention do(X = xᵢ).
    
    Returns:
        float – BIBAS score (0–100), or None if computation fails
    """
    # Helper: convert index → state-name when state_names are defined
    def _state_val(cpd, var, idx_or_name):
        if isinstance(idx_or_name, int) and cpd.state_names.get(var):
            return cpd.state_names[var][idx_or_name]
        return idx_or_name

    try:
        source_cpd = model.get_cpds(source)
        target_cpd = model.get_cpds(target)

        if target_cpd.variable_card != 2:
            raise ValueError("Target must be binary (exactly two states)")

        # Resolve positive state name and its index
        t_pos_name = _state_val(target_cpd, target, target_positive_state)
        t_states   = target_cpd.state_names.get(target, [0, 1])
        t_pos_idx  = t_states.index(t_pos_name) if isinstance(t_pos_name, str) else t_pos_name

        # Prior probability of T+
        elim = VariableElimination(model)
        p_t_pos = elim.query([target], show_progress=False).values[t_pos_idx]

        # Prior distribution of X (weights for aggregation)
        p_x = elim.query([source], show_progress=False).values

        shifts = []

        if operation == "observe":
            # Evidence-based posterior
            for i, weight in enumerate(p_x):
                if weight == 0:
                    continue  # skip impossible state
                evidence_val = _state_val(source_cpd, source, i)
                posterior = elim.query(
                    variables=[target],
                    evidence={source: evidence_val},
                    show_progress=False,
                ).values[t_pos_idx]
                shifts.append(weight * abs(posterior - p_t_pos))

        elif operation == "do":
            # Intervention-based posterior
            if target in model.get_parents(source):
                return 0.0  # causal influence child→parent is undefined (treated as 0)

            cinf = CausalInference(model)
            for i, weight in enumerate(p_x):
                if weight == 0:
                    continue
                do_val = _state_val(source_cpd, source, i)
                posterior = cinf.query(
                    variables=[target],
                    do={source: do_val},
                    show_progress=False,
                ).values[t_pos_idx]
                shifts.append(weight * abs(posterior - p_t_pos))

        else:
            raise ValueError("operation must be 'observe' or 'do'")

        return sum(shifts) * 100

    except Exception as e:
        print(f"[BIBAS Error] {e}")
        return None

def rank_sources_for_target(model, target, target_positive_state=1, operation="observe"):
    """
    Ranks all source nodes by their BIBAS score on a given binary target.
    
    Parameters:
        model: pgmpy.models.DiscreteBayesianNetwork
        target: str – name of the target node (must be binary)
        target_positive_state: int – state of the target considered "positive"
        operation: 'observe' or 'do'
    
    Returns:
        pd.DataFrame with columns: ['source', 'bibas_score'], sorted descending
    """
    target_card = model.get_cpds(target).variable_card
    if target_card != 2:
        raise ValueError("Target must be binary")

    sources = [node for node in model.nodes() if node != target]

    rows = []
    for src in sources:
        score = compute_bibas_pairwise(
            model,
            source=src,
            target=target,
            target_positive_state=target_positive_state,
            operation=operation
        )
        rows.append({"source": src, "bibas_score": score})

    df = pd.DataFrame(rows).sort_values("bibas_score", ascending=False).reset_index(drop=True)
    return df