from itertools import combinations
from data import shares
from typing import Callable


def brute_force(
    dataset: dict,
    force: int,
    accept: Callable[[dict], bool],
    evaluate: Callable[[dict, dict], bool],
    combine: Callable[[dict, dict], dict],
    serialize: Callable[[dict], str],
    deserialize: Callable[[str], dict],
    best_match_file_path: str,
):
    with open(best_match_file_path, 'r+') as f:
        try:
            best_cmb = deserialize(f.read())
        except:
            best_cmb = None
        for cmb in combinations(dataset.keys(), force):
            cmb = combine(dataset, cmb)
            if accept(cmb):
                if (best_cmb and evaluate(cmb, best_cmb)) or not best_cmb:
                    best_cmb = cmb.copy()
                    best_cmb_serialized = serialize(best_cmb)
                    f.seek(0)
                    f.write(best_cmb_serialized)
                    f.truncate()
                    print(best_cmb_serialized)