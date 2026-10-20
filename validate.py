"""Reproduce the lab's known answers and deliberate input breaks."""
from copy import deepcopy
import portfolio as p
import mandate as m


def main():
    covariance = p.covariance_matrix(p.SLEEVES, p.CORRELATION)
    expected = [("6.80%", "10.46%", "0.0%"),
                ("5.20%", "5.21%", "50.0%"),
                ("3.77%", "1.05%", "90.3%")]
    for (name, weights), answer in zip(p.baseline_weights(p.SLEEVES).items(), expected):
        actual = (f"{p.expected_return(weights, p.SLEEVES):.2%}",
                  f"{p.portfolio_volatility(weights, covariance):.2%}",
                  f"{p.reserve_weight(weights):.1%}")
        assert actual == answer, (name, actual, answer)
        assert abs(sum(weights) - 1) < 1e-12
        print(f"PASS {name}: {actual}")
    changed = deepcopy(p.CORRELATION)
    changed[2][3] = changed[3][2] = 0.50
    volatility = p.portfolio_volatility([0, 0, .4, .6],
                                       p.covariance_matrix(p.SLEEVES, changed))
    assert f"{volatility:.2%}" == "11.00%"
    print(f"PASS correlation 0.50: benchmark volatility {volatility:.2%}")
    for label, a, b in [("out-of-range", 1.3, 1.3), ("asymmetric", .5, .25)]:
        broken = deepcopy(p.CORRELATION)
        broken[2][3], broken[3][2] = a, b
        try:
            p.covariance_matrix(p.SLEEVES, broken)
        except ValueError as error:
            print(f"PASS {label} rejected: {error}")
        else:
            raise AssertionError(f"{label} was accepted")
    results = m.check(m.CANDIDATES["E"])
    assert [(label, value) for label, value, passed in results if not passed] == [
        ("Reserve >= 3.0%", 0)]
    print("PASS candidate E: reserve 0.0%, fails the 3.0% reserve rule")
    assert p.CORRELATION[2][3] == p.CORRELATION[3][2] == .25
    print("PASS original correlations restored at 0.25")


if __name__ == "__main__":
    main()
