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

## Choose a Blade Convention at Algebra Construction Time

Meaningful basis names are part of the teaching surface.

Do not default to whatever unnamed basis happens to come out of `Algebra(...)`
if the notebook is about a specific algebra tradition or notation.

Prefer choosing the blade convention when constructing the algebra:

```python
from galaga import Algebra
from galaga.blade_convention import (
    b_default,
    b_gamma,
    b_pga,
    b_sta,
    b_cga,
)

alg = Algebra((1, 1, 1), blades=b_default())
sta = Algebra((1, -1, -1, -1), blades=b_sta())
pga = Algebra((1, 1, 1, 0), blades=b_pga())
cga = Algebra(4, 1, blades=b_cga())
```

This is better than renaming individual basis vectors later unless you need a
very small local override.

### Built-in conventions to prefer

Use these first:

- `b_default()` for ordinary Euclidean/vector GA notebooks
- `b_gamma()` when the notebook is about gamma-vector notation
- `b_pga()` for projective geometry notebooks
- `b_sta()` for spacetime algebra notebooks
- `b_cga()` for conformal GA notebooks

These factories exist so the notebook starts with the right naming language.

### Practical defaults by topic

Use:

- `Algebra((1, 1), blades=b_default())` for early 2D Euclidean notebooks
- `Algebra((1, 1, 1), blades=b_default(overrides={"pss": "I"}))` when a named Euclidean pseudoscalar helps
- `Algebra((1, -1, -1, -1), blades=b_sta())` for standard STA notebooks
- `Algebra((1, -1, -1, -1), blades=b_sta(sigmas=True))` when observer-relative `σ_k` notation is pedagogically central
- `Algebra((1, 1, 1, 0), blades=b_pga())` for 2D PGA notebooks
- `Algebra(3, 1, blades=b_cga(euclidean=2))` for 2D CGA
- `Algebra(4, 1, blades=b_cga())` for 3D CGA

### Style matters

Blade naming style is a teaching decision too:

- `style="compact"`: `e₁₂`
- `style="juxtapose"`: `e₁e₂`
- `style="wedge"`: `e₁∧e₂`

Use:

- `compact` when you want concise basis-blade notation
- `juxtapose` when you want product structure to stay visible
- `wedge` when the notebook is emphasizing exterior / subspace meaning

Examples:

```python
Algebra(3, blades=b_default(style="compact"))      # e₁₂
Algebra(3, blades=b_default(style="juxtapose"))    # e₁e₂
Algebra(3, blades=b_default(style="wedge"))        # e₁∧e₂
Algebra(1, 3, blades=b_gamma())                    # γ₀γ₁
Algebra(1, 3, blades=b_gamma(style="compact"))     # γ₀₁
```

### Use the factory features instead of manual renaming when possible

Examples:

```python
Algebra(3, blades=b_default(prefix="v", style="compact"))   # v₁, v₂, v₃ and v₁₂
Algebra(3, 0, 1, blades=b_pga(pseudoscalar="I"))            # PGA with I
Algebra(4, 1, blades=b_cga(null_basis="plus_minus"))        # e₊, e₋ basis
Algebra(1, 3, blades=b_sta(sigmas=True))                    # σ₁, σ₂, σ₃ aliases
```

This gives better teaching results than retrofitting names later.

### Prefer `basis_blades(...)`, `locals(...)`, and `blade(...)` Over Manual Basis-Blade Rebuilding

As of `galaga 1.0.2+`, `Algebra` has notebook-friendly helpers for getting
named basis blades directly.

Prefer these over manually rebuilding basis blades with expressions like:

```python
e12 = (e1 * e2).name(latex=r"e_{12}")
```

unless the notebook is specifically teaching that construction.

Preferred patterns:

If the notebook only needs basis vectors, prefer the simplest form:

```python
e1, e2, e3 = alg.basis_vectors(lazy=True)
```

If the notebook also needs named bivectors, then use one of these:

```python
e12, e13, e23 = alg.basis_blades(2, lazy=True)
```

```python
_basis = alg.locals(grades=[1, 2], lazy=True)
locals().update(_basis)
print("Injected:", ", ".join(_basis))
```

```python
e12 = alg.blade("e12")
gamma12 = sta.blade("γ12")
```

Use:

- `basis_vectors(...)` by default when only basis vectors are needed
- `basis_blades(k, ...)` when the notebook needs standard named higher-grade blades as variables
- `locals(...)` when the notebook benefits from many basis blades being available directly and the local namespace will still stay readable
- `blade("name")` when you want one specific named blade that matches the chosen convention

Use manual products like

```python
B = e1 * e2
```

or

```python
B = e1 ^ e2
```

only when the notebook is actually teaching:

- the geometric product relation between basis vectors and bivectors
- the wedge construction of a plane element
- a sign/orientation point that depends on the written product order

If the blade is just a standard basis object needed for later work, prefer the
constructor helpers.

`basis_blades(2)` returns the canonical basis order. In `Cl(3,0)`, that is:

```python
e12, e13, e23 = alg.basis_blades(2, lazy=True)
```

Prefer canonical names like `e13` over ad hoc alternatives like `e31` unless
the notebook is explicitly about orientation/sign.

If a notebook really needs the opposite orientation, express that honestly:

```python
e31 = -e13
```

### When to use CGA naming modes

For CGA there are two useful null-basis styles:

- `b_cga()`:
  uses `eₒ, e∞`
- `b_cga(null_basis="plus_minus")`:
  uses `e₊, e₋`

Pedagogical guidance:

- use `eₒ, e∞` when the notebook is about lifted points, infinity, distance, circles, spheres, incidence
- use `e₊, e₋` when you want to build the null basis explicitly from an orthogonal `(+,-)` pair

This repo often benefits from the second choice in early CGA notebooks, because
it lets the notebook show the null directions being constructed rather than
presenting them as magic primitives.

### STA-specific naming guidance

For STA notebooks:

- use `b_sta()` when the notebook is about spacetime vectors, boosts, fields, and rotors in spacetime
- use `b_sta(sigmas=True)` only when the notebook explicitly needs the observer-relative Pauli-style `σ_k` layer
- use `b_sta(pseudovectors=True)` only when trivector names like `iγ_k` are part of the lesson

Do not turn on `sigmas=True` just because it is available. It changes the visible
notation and should only be used when it actually helps the student.

### PGA and CGA should normally use their dedicated factories

Do not hand-roll PGA or CGA naming with `b_default(...)` unless there is a very
specific reason.

Use:

```python
Algebra((1, 1, 1, 0), blades=b_pga())
Algebra(4, 1, blades=b_cga())
```

Those factories already encode the standard naming choices:

- PGA: `e₀, e₁, ...`, pseudoscalar `I`
- CGA: `e₁, ..., eₒ, e∞` or `e₊, e₋`, pseudoscalar `I`

### Overrides are useful for concept notebooks

Use blade overrides when the notebook’s main idea is easier to read through a
named generator or pseudoscalar.

Examples:

```python
Algebra(3, blades=b_default(overrides={"pss": "I"}))
Algebra(3, blades=b_default(overrides={"+1+2": "B", "pss": "I"}))
Algebra(1, 3, blades=b_sta(overrides={
    "+1-1": ("s1", "σ₁", r"\sigma_1"),
    "pss": ("i", "i", "i"),
}))
```

Use overrides sparingly. They are good when they make the notebook’s central
objects easier to recognize, but too many overrides can make the basis feel
custom and unmoored.

### Do not swap conventions after construction

If the notebook needs a different naming system, create a new algebra instead of
trying to mutate the whole convention later.

Good:

```python
sta_plain = Algebra((1, -1, -1, -1), blades=b_sta())
sta_sigma = Algebra((1, -1, -1, -1), blades=b_sta(sigmas=True))
```

Avoid:

- constructing one algebra and then trying to globally reinterpret all basis names later

Use post-hoc renaming only for small local fixes.

### Post-hoc renaming is a surgical tool, not the default workflow

If one blade needs a better teaching name, use `get_basis_blade(...).rename(...)`.

Examples:

```python
alg.get_basis_blade("pss").rename("I")
alg.get_basis_blade("+1+2").rename("B")
alg.get_basis_blade("+1-1").rename(("s1", "σ₁", r"\sigma_1"))
```

But prefer construction-time conventions and overrides first.

### Signed blade aliases matter

Some named blades, especially in STA, correspond to products whose natural sign
does not match the canonical sorted basis blade.

Example:

- `σ₁ = γ₁γ₀`
- but the canonical basis blade is `γ₀γ₁ = -σ₁`

The factory helpers handle this correctly.

Do not try to recreate `σ_k` naming manually by renaming `γ₀γ_k` after the fact
unless you also know how to handle the sign convention.

### Blade lookup and notebook consistency

With conventions active, `blade("name")` lookup follows the chosen naming scheme.

That means if the notebook uses a convention, examples and helper code should use
the same names the reader sees.

Good:

```python
sta = Algebra((1, -1, -1, -1), blades=b_sta(sigmas=True))
sta.blade("σ₁")
sta.blade("pss")
```

Also good:

```python
e12 = alg.blade("e12")
e12, e13, e23 = alg.basis_blades(2, lazy=True)
_basis = alg.locals(grades=[1, 2], lazy=True)
locals().update(_basis)
print("Injected:", ", ".join(_basis))
```

Less good unless the construction itself is being taught:

```python
e12 = (e1 * e2).name(latex=r"e_{12}")
```

Avoid mixing displayed names and internal names in ways the reader cannot see.

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
- Prefer `basis_blades(...)`, `locals(...)`, and `blade(...)` for standard named basis blades.
- Only build basis blades manually when the notebook is teaching that construction or sign/orientation issue.
- Name conceptual milestones, not every temporary.
- Use `.display()` inside `gm.md(t"""...""")` for the visible math.
- Move coefficient extraction and `numpy` conversion into the appendix plotting helpers.
- Probe candidate expressions in short `uv` snippets before finalizing notebook code.

The notebook consumer should mostly see:

- clean symbolic derivations
- clearly named intermediate objects
- plots that match those objects

They should not have to mentally reconstruct the math from plotting code.
