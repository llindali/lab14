"""Lab 13: Meridian Foundation mandate checker (standard library only)."""
from math import isclose

# Editable inputs: days are business days; weights are percentage points.
HOLDINGS = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
    "E": [0, 0, 0, 60, 40, 0, 0, 0],  # Lab 14 benchmark
}
RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MIN_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def check(weights):
    """Return measured values and pass/fail results for checkable rules."""
    if len(weights) != len(HOLDINGS):
        raise ValueError("Provide one weight per holding.")
    reserve_min = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    reserve = liquid = 0
    issuers = {}
    for (_, issuer, days, eligible), weight in zip(HOLDINGS, weights):
        if eligible:
            reserve += weight
        if days <= LIQUIDITY_WINDOW:
            liquid += weight
        if issuer not in EXEMPT_ISSUERS:
            issuers[issuer] = issuers.get(issuer, 0) + weight
    largest = max(issuers.values(), default=0)
    return [
        ("Weights sum to 100", sum(weights), isclose(sum(weights), 100, abs_tol=1e-9)),
        ("Long-only (lowest weight)", min(weights), min(weights) >= 0),
        (f"Reserve >= {reserve_min:.1f}%", reserve, reserve >= reserve_min),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MIN_LIQUID_SHARE:.1f}%",
         liquid, liquid >= MIN_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest, largest <= ISSUER_LIMIT),
    ]


def main():
    reserve_min = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_min:.1f}%")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        results = check(weights)
        for label, value, passed in results:
            print(f"{label}: {value:.1f} {'pass' if passed else 'FAIL'}")
        print("Calendar-year loss: requires CIO clarification")
        failures = sum(not passed for _, _, passed in results)
        print("passes every checkable rule" if not failures else f"fails {failures} rule(s)")


if __name__ == "__main__":
    main()
