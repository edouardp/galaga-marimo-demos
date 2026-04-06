# Authoring Notebooks

This file is for coding assistants working in this repo: Codex, Claude Code, and similar tools.

The goal is not just to make notebooks that run. The goal is to make notebooks that teach well.

## Core Principle

Treat each notebook as having three layers:

1. The conceptual GA layer
2. The visible rendered math layer
3. The plotting/UI plumbing layer

Keep these separate.

- The conceptual GA layer should build multivectors, rotors, projectors, scalar expressions, and named intermediate objects.
- The visible rendered math layer should show those objects using `gm.md(t"""...""")` and `.display()`.
- The plotting/UI plumbing layer should extract `scalar_part`, `vector_part`, coefficients, `numpy` arrays, colors, axis limits, etc.

Do not mix all three layers in one cell unless there is a very strong reason.

## Default Notebook Structure

Prefer this structure:

1. Intro markdown
2. Algebra-intro markdown
3. `Algebra(...)` cell
4. Control cell(s)
5. Main calculation cell(s)
6. Main explanation/render cell(s) using `gm.md(t"""...""")`
7. `## Appendum: Plotting Code`
8. Hidden plotting/helper cells

Put plotting code at the end of the notebook under:

```python
@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appendum: Plotting Code
    """)
    return
```

Plot helpers should accept GA objects directly. They should do their own unpacking internally.

## Main Cell vs Appendix

Main cells should:

- build the important GA objects
- name the important GA objects
- keep scalar expressions as GA scalars when they are part of the math
- render symbolic chains with `.display()`
- pass GA objects to plot helpers

Appendix/helper cells should:

- unpack with `.scalar_part`, `.vector_part`, or basis projections
- build `numpy` arrays
- choose plot bounds
- style plots
- compute coefficients used only for plotting

If a line exists only to support the plot, it belongs in the appendix.

## Naming Strategy

Use `.name(...)` to mark conceptual milestones.

Good things to name:

- generators
- rotors
- projected/rejected parts
- physical observables
- probabilities
- invariants
- intermediate objects the reader should recognize and reuse

Do not name every temporary.

Too many names make the notebook feel like a symbol dump.

### `.name(...)` guidance

The API is:

```python
mv.name(label=None, *, latex=None, unicode=None, ascii=None)
```

At least one of `label` or `latex` must be provided.

Recommended patterns:

```python
_R = exp(-theta * B / 2).name(latex="R")
_s = (_R * e3 * ~_R).name(latex="s")
_p = ((alg.scalar(1) + (_s | _n)) / 2).name(latex=r"P_N")
```

Notes:

- `repr(mv)` follows the unicode-facing label when present.
- `.latex()` follows the LaTeX-facing label.
- `.display()` uses the LaTeX-facing symbolic chain.

## Use `.display()` Aggressively

The repo pattern is:

```python
gm.md(t"""
{_R.display()} <br/>
{_s.display()} <br/>
{_p.display()}
""")
```

This is usually the best way to show the symbolic story.

Why:

- unnamed expressions show the expression directly
- named expressions show `name = expression`
- if the expression simplifies further, `.display()` can show `name = expression = evaluated form`

This is ideal for teaching.

Examples:

- `B = e1 ∧ e2 = e12`
- `R = exp(-θ B / 2)`
- `P = (1 + s·n)/2 = 0.734`

Prefer `.display()` over manually duplicating the equation in markdown.

## Prefer GA Scalars Over Python Floats When the Scalar Is Part of the Math

If a scalar is part of the mathematical story, keep it as a GA scalar.

Use:

- `alg.scalar(x)` for meaningful general scalars
- `alg.frac(a, b)` for exact rational factors
- `sqrt(...)` for square roots that belong in the algebraic layer
- `scalar_sqrt(...)` only when scalar-only intent is pedagogically important

Examples:

```python
theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
half = alg.frac(1, 2)
prob = ((alg.scalar(1) + (_s | _n)) * half).name(latex=r"P_N")
norm_x = sqrt((_x * ~_x).name(latex="n")).name(latex=r"\|x\|")
```

Why:

- `alg.frac(1, 2)` preserves the symbolic `1/2` in `.display()`
- `alg.scalar(...)` keeps constants and parameters in the expression tree
- `sqrt(...)` now works on more than just plain scalars and is the better default notebook-facing function

Avoid converting early like:

```python
prob = (1.0 + (_s | _n).scalar_part) / 2.0
```

when the probability itself is part of the explanation.

Instead prefer:

```python
prob = ((alg.scalar(1) + (_s | _n)) / 2).name(latex=r"P_N")
```

Then render:

```python
{prob.display()}
```

Convert to Python floats only when you truly need:

- plot heights
- axis limits
- `numpy` arrays
- conditional logic

## `alg.frac(...)` Should Usually Replace `alg.scalar(1/2).name(...)`

Use:

```python
half = alg.frac(1, 2)
```

instead of:

```python
half = alg.scalar(1/2).name(latex=r"\frac{1}{2}")
```

Reason:

- `alg.frac(...)` preserves exact symbolic fractions in the expression tree
- `.display()` then shows the exact fraction first and the evaluated decimal second

This is particularly useful for:

- projector formulas
- polarization identities
- symmetric/antisymmetric splits
- half-angle rotor formulas

## Use `sqrt(...)` by Default

This repo now has a fully MV-capable `sqrt(...)` in `galaga`.

Use `sqrt(...)` by default when you mean “square root in the algebraic layer”.

Use `scalar_sqrt(...)` only if the notebook is explicitly emphasizing scalar-only behavior.

For pedagogical purposes, `sqrt(...)` is the better default because it keeps the expression tree more general and future-proof.

## Expression Trees Are Part of the Teaching Surface

Do not think of expression trees as just an implementation detail.

They are part of the notebook’s visible math layer.

You should choose between:

- unnamed vs named
- `alg.scalar(...)` vs Python numeric
- `alg.frac(...)` vs decimal scalar
- `sqrt(...)` vs `scalar_sqrt(...)`

based on what gives the best `.display()` output for the student.

## Authoring Workflow: Probe Small Expressions First

When authoring or revising notebooks, use short `uv` snippets to test how expressions render before committing them to the notebook.

Recommended workflow:

1. build the candidate expression
2. try `.name(...)`
3. inspect:
   - `repr(...)`
   - `.latex()`
   - `.display()`
4. compare variants
5. choose the one that teaches best

Typical probing pattern:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'PY'
from galaga import Algebra, sqrt

alg = Algebra((1, 1, 1))
e1, e2, e3 = alg.basis_vectors(lazy=True)

half = alg.frac(1, 2)
expr = (half * (e1 + e2)).name(latex='x')

print(expr)
print(expr.latex())
print(expr.display())
PY
```

Use this workflow when deciding:

- whether a scalar should stay symbolic
- whether a name helps or clutters
- whether the expression chain is pedagogically readable

## What Good Notebook Math Looks Like

Good:

```python
theta = alg.scalar(np.radians(angle.value)).name(latex=r"\theta")
B = (e1 ^ e2).name(latex="B")
R = exp(-theta * B / 2).name(latex="R")
s = (R * e3 * ~R).name(latex="s")
P = ((alg.scalar(1) + (s | n)) / 2).name(latex=r"P_N")

gm.md(t"""
{theta.display()} <br/>
{B.display()} <br/>
{R.display()} <br/>
{s.display()} <br/>
{P.display()}
""")
```

Weak:

```python
theta = np.radians(angle.value)
R = exp(-(theta/2) * (e1 ^ e2))
s = R * e3 * ~R
p = (1 + (s | n).scalar_part) / 2
```

Why weak:

- important scalars have dropped out of the GA layer
- the notebook loses the symbolic story
- the reader sees results but not the derivation

## Distinguish Conceptual Objects From Plotting Objects

Keep these as conceptual objects:

- `theta`
- `B`
- `R`
- `s`
- `P`
- `F`
- `F²`
- projected/rejected pieces

Keep these as plotting objects:

- `_coords`
- `_coeffs`
- `_xlim`
- `_bars`
- `_color`
- `_pts`

Plotting objects should generally live in the appendix.

## Use Clear Code Names

Do not overuse paper-style names in code when they obscure purpose.

Prefer readable internal names like:

- `first_axis`
- `second_axis`
- `spin_after_first`
- `ensemble_average_spin`

Use compact symbolic names in the displayed math if needed.

Code should help teach, not merely imitate paper notation.

## Keep the Notebook Honest

Do not use a prettier symbolic form if it hides what the notebook is actually doing.

Examples:

- If a notebook is really using observer-relative bivectors, say so.
- If a value is a scalar overlap and not a projector, do not call it a projector.
- If a plot is showing dual normals rather than planes directly, explain that.

Clarity beats elegance when the two conflict.

## Summary Rules

If you are unsure, follow these defaults:

- Keep meaningful quantities in GA form as long as possible.
- Use `alg.frac(...)` for simple exact fractions.
- Use `alg.scalar(...)` for meaningful non-fraction scalars.
- Use `sqrt(...)` as the default algebraic square root.
- Name conceptual milestones, not every temporary.
- Use `.display()` inside `gm.md(t"""...""")` for the visible math.
- Move coefficient extraction and `numpy` conversion into the appendix plotting helpers.
- Probe candidate expressions in short `uv` snippets before finalizing notebook code.

The notebook consumer should mostly see:

- clean symbolic derivations
- clearly named intermediate objects
- plots that match those objects

They should not have to mentally reconstruct the math from plotting code.
