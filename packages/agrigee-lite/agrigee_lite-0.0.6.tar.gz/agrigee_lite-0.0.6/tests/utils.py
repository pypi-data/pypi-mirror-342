import numpy as np

import agrigee_lite as agl
from agrigee_lite.sat.abstract_satellite import AbstractSatellite


def assert_np_array_equivalence(arr1: np.ndarray, arr2: np.ndarray, threshold: float = 0.1) -> None:
    arr1 = arr1.flatten()
    arr2 = arr2.flatten()

    if arr1.shape != arr2.shape:
        raise AssertionError(f"Shape mismatch: {arr1.shape} vs {arr2.shape}")

    bound1 = arr2 * (1 - threshold)
    bound2 = arr2 * (1 + threshold)
    lower_bound = np.minimum(bound1, bound2)
    upper_bound = np.maximum(bound1, bound2)

    valid = (arr1 >= lower_bound) & (arr1 <= upper_bound)

    if not np.all(valid):
        invalid_indices = np.where(~valid)[0]
        error_pct = 100 * len(invalid_indices) / len(arr1)

        msg_lines = [
            f"Arrays differ: {len(invalid_indices)} of {len(arr1)} values outside threshold ({error_pct:.2f}%)",
        ]

        for i in invalid_indices[:5]:
            msg_lines.append(
                f"[{i}] Downloaded={arr1[i]:.4f}, Original={arr2[i]:.4f}, "
                f"Allowed=[{lower_bound[i]:.4f}, {upper_bound[i]:.4f}]"
            )

        raise AssertionError("\n".join(msg_lines))


def get_all_satellites_for_test() -> list[AbstractSatellite]:
    return [agl.sat.Sentinel2(), agl.sat.Sentinel2(use_sr=True)]
