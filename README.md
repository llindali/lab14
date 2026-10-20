# Lab 14 — Portfolio Baselines

Linda Li · FIN 43900 · October 20, 2026

## Define and represent

What does each simple portfolio earn and risk, and does any meet the Meridian mandate?
All returns, volatilities and correlations are course-authored annual training values, not market estimates. The objective is 6.5%, using a labelled CPI estimate of 2.5% plus 4%. Sleeve order is bills / 10-year Treasury / IG bonds / global equity.

## Run and reproduce

Standard library only; no installation required:

```bash
python portfolio.py
python mandate.py
python validate.py
```

`portfolio.py` has editable inputs and reusable functions, with no printing when imported. `mandate.py` copies the existing Lab 13 checker and adds candidate E. The original Lab 13 repository is unchanged. `validate.py` checks published answers and deliberate input errors. `results.txt` records actual runs.

## Results

| Portfolio | Weights (%) | Return | Volatility | Reserve | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

All published rounded values match. Rounded inverse-volatility weights total 99.9%; the unrounded weights sum to 100%.

None meets both the expected-return objective and all checkable mandate rules: the benchmark meets the return objective but fails the 3% reserve minimum; the other two clear that reserve minimum but miss the return objective. Candidate E is 40% IG fund and 60% equity fund and fails exactly one checkable rule, the reserve rule, with 0.0%. Passing checkable rules does not establish overall suitability or guarantee a calendar-year loss limit. The inherited checker does not evaluate the trading-volume rule without trade/volume data; the loss promise still requires CIO clarification.

## Validation evidence

- Symmetric IG/equity correlation changed from 0.25 to 0.50: benchmark volatility rises to 11.00%.
- Symmetric correlation 1.3: rejected with a clear out-of-range error.
- One-sided correlation change: rejected as asymmetric.
- Original input remains 0.25 in both cells after validation.
- Candidate E run through the actual inherited mandate checker: reserve failure confirmed.

These are AI-executed checks of this repository. They do not document a partner file swap or a student oral explanation.

## Diversification and hand calculation

Diversification combines exposures whose returns do not move perfectly together. With positive weights, a correlation below +1 lowers the covariance contribution relative to perfect positive correlation. It can lower combined volatility below either asset in some mixes, but does not always do so; this benchmark's 10.46% lies between bond risk of 6% and equity risk of 16%. Systematic risk remains, and correlations can increase in stress.

Expected return: 0.40 × 0.05 + 0.60 × 0.08 = 0.068 = **6.80%**.

Covariance: 0.25 × 0.06 × 0.16 = **0.0024**.

Variance: (0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.0024)
= 0.000576 + 0.009216 + 0.001152 = **0.010944**.

Volatility: sqrt(0.010944) = **10.46%**. Omitting covariance gives 9.90%, which is wrong for the supplied correlation. At correlation 0.50, variance is 0.012096 and volatility is 11.00%.

## Code explanation for student review

`covariance_matrix` validates the correlation table, then multiplies each correlation by the two sleeves' volatilities. `portfolio_variance` loops over every ordered sleeve pair, multiplying the two weights by that pair's covariance and summing. The diagonal terms are standalone variance contributions. Off-diagonal pairs occur twice, supplying the factor of two in the two-asset formula. `portfolio_volatility` takes the square root, returning to return units. This is a review aid; the required partner explanation must be done without AI.

## Reflection drafts for Linda to review

Inverse volatility puts 84.3% into bills because their 0.5% volatility is much lower than the others. Their inverse volatility is 200, versus about 14.29, 16.67 and 6.25. Normalizing these numbers heavily favors bills. This rule ignores expected returns, correlations and mandate objectives when assigning weights, so low volatility does not imply a suitable portfolio.

I would show the CIO the benchmark first because it is the policy reference and earns an expected 6.8%, yet holds no eligible reserve. This immediately exposes the conflict between the stated benchmark and the reserve requirement. I would show the other baselines next to illustrate the return sacrificed for lower volatility. None should be adopted unchanged.

## Student input and activities still required

1. **AI quiz:** identify the line you understand least and answer a question before receiving its explanation. Starting question: in `portfolio_variance`, why do we loop over both `(i, j)` and `(j, i)`? What would happen to benchmark volatility if all off-diagonal terms were omitted? Linda's answer is pending.
2. **Partner work:** provide the Lab 13 partner's name, complete the no-screen diversification explanation and swap, explain the volatility block line by line without AI, and record the partner's question plus your actual answer. No activity has been claimed as completed.
3. **Swap and break:** run the partner's actual file, set IG/equity correlation to 1.3, observe rejection, and undo it. Supply the actual outcome or file if debugging is needed. This repository's equivalent automated test passed, but is not a substitute for the partner exercise.
4. **Learn/reflect:** review the written explanation and reflection drafts, then discuss with your partner as assigned. Add any corrections from your own understanding.
5. **Before Thursday / Project 2:** supply your own mandate (client, objective, horizon, reserve and constraints) and choose 3–6 funds fitting it. The practice universe below is provisional and has not been presented as your own chosen universe.
6. **Historical data:** after the universe is chosen, obtain five years of monthly Yahoo Finance **Adj Close** prices, including payouts, and combine into `prices.csv` with date first, oldest month first, and one column per ticker. Record the source and actual download date for each. No prices have been fabricated and no download has been claimed. An export is needed if the data source cannot be accessed here.
7. **Checkout:** submit your individual GitHub file links in the course's required submission location. Repository publication is complete; course submission is a student action.

## Provisional practice universe for Thursday

These are the instructor's examples, not personalized recommendations or a confirmed Project 2 selection. Price availability and adjusted columns still need verification.

| Ticker | Fund name | Role | Intended source | Download date |
|---|---|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve | Yahoo Finance monthly historical Adj Close | Pending |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | Yahoo Finance monthly historical Adj Close | Pending |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income | Yahoo Finance monthly historical Adj Close | Pending |
| VT | Vanguard Total World Stock ETF | Broad global equity | Yahoo Finance monthly historical Adj Close | Pending |

## Sources and checkout links

- [Lab 14 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md)
- [Student handout](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md)
- [Inherited Lab 13 checker](https://github.com/llindali/lab13/blob/main/mandate.py)
- [Written work](https://github.com/llindali/lab14/blob/main/README.md)
- [Risk engine](https://github.com/llindali/lab14/blob/main/portfolio.py)
- [Mandate checker](https://github.com/llindali/lab14/blob/main/mandate.py)
- [Validation](https://github.com/llindali/lab14/blob/main/validate.py)
- [Actual output](https://github.com/llindali/lab14/blob/main/results.txt)

AI assisted implementation, calculation checks and writing drafts. Student quiz and partner work remain pending.
