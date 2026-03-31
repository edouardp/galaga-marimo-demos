# galaga-marimo-demos

This repo contains small, concept-first `marimo` notebooks built with `galaga`.
The goal is not to dump API demos into notebooks. The goal is to build short,
interactive explanations that help a reader understand geometric algebra ideas
through computation, visuals, and controlled interaction.

## Purpose

Each notebook should teach one core idea well.

A good notebook in this repo should do three things at once:

- explain the domain or geometric idea
- show the geometric algebra formulation
- show the code that computes it

The notebooks should feel like teaching artifacts, not library showcases.

## Scope

The repo currently focuses on:

- Euclidean rotor intuition
- spacetime algebra and boosts
- rotor interpolation
- geometric projectors
- short, interactive derivations

New notebooks should fit that level and style unless there is a clear reason to
expand the scope.

## Core Pedagogical Approach

### 1. Concept first

Start from the idea being explained, not the API.

Examples:

- “two reflections compose to a rotation”
- “rapidity labels boosts”
- “a line and a plane are both blades, so projection uses one formula”

Avoid leading with imports, symbolic machinery, or implementation detail.

### 2. One idea per notebook

Do not mix several abstraction levels into one file. A notebook should have one
 dominant claim and one main interaction loop.

Good:

- rotors from reflections
- rotor space
- 3D rotor slerp
- projectors

Bad:

- a notebook that tries to teach rotors, quaternions, projectors, and STA all at once

### 3. Domain -> GA -> code -> validation

The standard loop is:

1. state the phenomenon or geometric claim
2. express it in GA terms
3. compute it in code
4. validate it visually or numerically

The notebook should close that loop explicitly.

### 4. Prefer construction over definition

Build ideas from simpler ingredients.

Examples:

- reflections -> rotor
- bivector -> exponential -> rotor -> sandwich action
- relative rotor -> logarithm -> slerp

### 5. Make the payoff visible

If GA is cleaner than the non-GA alternative, make that visible.

Examples:

- one projector formula for both lines and planes
- one rotor interpolation formula in 3D even when the plane changes
- spacetime bivectors splitting naturally into rotation and boost generators

If the concept is easy without GA, either acknowledge that or choose a better
example. The 2D slerp notebook is acceptable as intuition, but the 3D version
is more persuasive.

## Notebook Structure

Follow this structure unless there is a strong reason not to.

### 1. Imports cell

The first cell should import what the notebook needs and return only those
objects needed downstream.

Typical imports:

- `Algebra`
- `exp`, `log`, `sandwich`, `project`, `reject`, `unit`, etc.
- `galaga_marimo as gm`
- `numpy as np`
- `marimo as mo`
- `matplotlib.pyplot as plt`

### 2. Plot helper cell

Put plotting helpers near the top in their own cell. Return the plotting
function(s) for later use.

Plot helpers should:

- take already-computed GA objects as arguments
- extract components locally
- close figures with `plt.close(fig)`
- return the figure

Important:

- keep plot plumbing inside the helper whenever possible
- do not unpack `vector_part`, `scalar_part`, or coefficient arrays in the main teaching cell just to satisfy a plotting API
- let the main cell stay focused on the GA explanation, symbolic objects, and displayed relationships

### 3. Short algebra-intro markdown cell before `Algebra(...)`

Before defining the algebra, include a short hidden-code markdown cell that
states what algebra is being built.

Examples:

- `Cl(2,0)` with basis-vector squares and why that matches the plane
- `Cl(1,3)` with signature `(+, -, -, -)` and why STA is less familiar

This is now a repo convention.

### 4. Algebra construction cell

Define the algebra in its own cell, always return the algebra object itself,
and then return the basis elements needed downstream.

Examples:

- `alg = Algebra((1, 1))`
- `sta = Algebra((1, -1, -1, -1), names="gamma")`

Preferred pattern:

```python
alg = Algebra((1, 1))
e1, e2 = alg.basis_vectors(lazy=True)
return alg, e1, e2
```

### 5. Explanatory markdown cells

Use short `@app.cell(hide_code=True)` markdown cells to introduce each section.

Good section types:

- title + claim
- what the object is
- the minimal formula
- why this matters
- conclusion

Keep them short. These notebooks are not textbooks.

### 6. Control-definition cells

Define sliders and dropdowns in their own earlier cells.

Important:

- define controls in one cell
- render them in the main output cell that also shows `gm.md(...)` and the plot

Do not place a separate `mo.vstack([...controls...])` display cell between the
control definition and the actual teaching cell unless there is a deliberate
reason to do so.

This is an established repo convention.

### 7. Main output cell

The main teaching cell should usually do all of this together:

- read the current UI values
- compute the GA objects
- build a concise `gm.md(...)` explanation
- render the plot
- show the controls at the top of the same output

Typical pattern:

```python
mo.vstack([
    slider_a,
    slider_b,
    gm.md(_md),
    draw_something(...),
])
```

## Markdown and Explanation Style

### Keep explanations compact

Use short markdown sections. Long essays are a poor fit for these notebooks.

Aim for:

- a clear title
- one or two paragraphs of explanation
- one formula block when needed
- one short “why this matters” section near the end

### Use raw strings for markdown with backslashes

When writing LaTeX-heavy markdown, prefer raw triple-quoted strings:

```python
mo.md(r"""
... \theta ...
""")
```

This avoids Python escape-sequence warnings like the earlier `\wedge` issue.

### Distinguish object, generator, operator, action

This matters a lot in GA notebooks. Be explicit about the role of each object.

Examples:

- blade: the subspace object
- unit bivector: the generator
- rotor: the operator
- sandwich product: the action

### Minimal necessary math

Only include the math needed to support the visual/computational story.

Do not include long derivations unless the derivation is the notebook.

## Coding Style

### Use `uv`

This repo uses `uv`. Verification and execution should be done with `uv` in the
repo environment.

Examples:

- `UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile notebooks/rotors/notebook.py`
- `UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'PY' ... PY`

Use `UV_CACHE_DIR=/tmp/uv-cache` in sandboxed environments.

### Name local-only variables with leading underscores

In `marimo`, non-underscored top-level names in a cell are treated as outputs.
If a cell is not intended to export variables to other cells, use underscored
names for intermediates.

Preferred:

- `_theta`
- `_R`
- `_v`
- `_md`

Use plain names only for values intentionally exported to other cells.

This is especially important for avoiding cell redefinition errors.

This also means you must not underscore names that later cells need.

Example:

```python
sta = Algebra((1, -1, -1, -1), names="gamma")
g0, g1, g2, g3 = sta.basis_vectors(lazy=True)
return g0, g1
```

That cell is intentionally exporting `sta`, `g0`, `g1`, `g2`, and `g3` as
top-level notebook names. If you instead wrote `_sta`, `_g0`, `_g1`, and so on,
those names would stay local to the cell and would not be available in the rest
of the notebook.

The repo convention is stricter than that example alone: always expose the
algebra object itself as well. That keeps notebook structure uniform and avoids
revisiting the algebra cell later when a new scalar or helper construction needs
it.

### Avoid accidental exported names

If a cell is only for rendering and does not feed later cells, end it with:

```python
return
```

Do not return unnecessary values from rendering cells.

### Keep cell responsibilities narrow

Each cell should have one job:

- define imports
- define plot helpers
- define the algebra
- define controls
- compute and render one concept

### Keep helper functions pure

Plot helpers should not depend on notebook globals unless necessary. Pass in the
computed objects they need.

### Prefer explicit computation over hidden magic

If a notebook claims an invariant or identity, compute it and show it.

Examples:

- `R \tilde{R} = 1`
- `proj + rej = v`
- `p^2 = m^2`
- `I^2 = -1`

## Plotting Conventions

### Show the geometry directly

Plots should visually support the claim being made.

Examples:

- Minkowski diagram for boosts
- vector plot for 2D rotations
- rotor-space circle for 2D rotors
- sphere plot for 3D rotated vectors
- line and plane decomposition for projectors

### Keep plots readable

Default preferences:

- equal aspect ratio when appropriate
- visible grid with low alpha
- labeled axes
- concise title
- legend only when it helps

### Keep dynamic bounds honest

If the geometry grows with the parameter, expand plot bounds accordingly rather
than letting objects disappear off-screen. The Lorentz-boost notebook now uses
this rule.

### Close figures

Always call `plt.close(fig)` before returning a figure from a helper.

## Interaction Design

### Controls must map to real parameters

Every slider or dropdown should represent a meaningful quantity:

- angle
- rapidity
- momentum
- mass
- line direction
- plane choice
- blend parameter

Avoid arbitrary controls.

### Synchronize views

When the user changes a control, the notebook should update together:

- symbolic expression
- numeric values
- geometric plot

This is one of the strongest conventions in the repo.

### Prefer one main interactive loop

A notebook can have multiple sections, but each section should still feel like a
single coherent interaction rather than a grab-bag of disconnected widgets.

## Conventions by Topic

### Euclidean 2D notebooks

Good for:

- first intuition
- rotor-space visualization
- reflections and bivectors

Typical basis:

- `e1`, `e2`

Typical plot:

- arrows in the plane
- unit circle

### 3D notebooks

Use when the 2D case is too easy or hides the real benefit.

Good for:

- changing rotation planes
- showing that rotor space is larger than the complex-number analogy
- projectors into planes

Typical basis:

- `e1`, `e2`, `e3`

Typical plot:

- 3D quiver plot
- optional sphere or plane surface

### STA notebooks

Use extra explanatory care. Readers are less likely to already know STA.

STA notebooks should usually:

- explicitly state the signature `(+, -, -, -)`
- identify timelike and spacelike basis vectors
- explain whether a bivector generates a boost or a rotation
- connect the abstract algebra back to physical meaning

Examples:

- Lorentz boosts
- Dirac negative-energy states
- twin paradox

## What to Avoid

- notebooks that are mostly API demonstrations
- long derivations without interactive payoff
- multiple unrelated ideas in one file
- hidden conventions about sign choices with no explanation
- duplicated slider display cells
- exported marimo names that are only local intermediates
- fixed plot bounds when the geometry obviously grows beyond them
- multiple notebooks with overlapping subject matter but no clearly distinct claim

## Checklist for New Notebooks

Before considering a notebook done, check:

1. Is there one clear idea?
2. Is there a short algebra-intro markdown cell before `Algebra(...)`?
3. Are controls defined earlier but rendered in the same output cell as the markdown and plot?
4. Are local-only intermediates underscored?
5. Does the notebook compute the claimed invariant or identity?
6. Does the plot directly support the main idea?
7. Does the notebook use `gm.md(...)` for computed expressions?
8. Does the file compile under `uv`?

## Verification

Use `uv` for verification.

Typical command:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -m py_compile notebooks/rotors/notebook.py
```

For runtime spot checks:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'PY'
import notebook_name
print("import ok")
PY
```

## Topic Folders

The notebooks now live under `notebooks/` and are grouped by topic.

- `notebooks/rotors`
  rotors, reflections, versors, rotor interpolation, and rotor action
- `notebooks/grade`
  grade decomposition, grade routing, involutions, norms, and algebraic structure
- `notebooks/subspaces`
  projectors, subspace actions, duality, and subspace representations
- `notebooks/pga`
  projective incidence geometry
- `notebooks/sta`
  spacetime algebra and relativity

## Current Notebooks

### Rotors

- [notebooks/rotors/notebook.py](./notebooks/rotors/notebook.py): basic 2D rotor rotation
- [notebooks/rotors/reflections_ga.py](./notebooks/rotors/reflections_ga.py): single reflections as the primitive rigid motion
- [notebooks/rotors/versor_composition.py](./notebooks/rotors/versor_composition.py): composing reflections into a general versor
- [notebooks/rotors/rotors_from_reflections.py](./notebooks/rotors/rotors_from_reflections.py): reflections composing into rotors
- [notebooks/rotors/rotor_space.py](./notebooks/rotors/rotor_space.py): vectors vs rotors, sandwich vs composition
- [notebooks/rotors/rotor_slerp.py](./notebooks/rotors/rotor_slerp.py): 2D rotor slerp
- [notebooks/rotors/rotor_slerp_3d.py](./notebooks/rotors/rotor_slerp_3d.py): 3D rotor slerp across planes
- [notebooks/rotors/rotor_logarithms.py](./notebooks/rotors/rotor_logarithms.py): recovering bivector generators with `log(R)`
- [notebooks/rotors/rotor_action_multivectors.py](./notebooks/rotors/rotor_action_multivectors.py): sandwich action on vectors and bivectors

### Grade Structure

- [notebooks/grade/bivectors_are_planes.py](./notebooks/grade/bivectors_are_planes.py): bivectors as oriented plane elements
- [notebooks/grade/grade_and_dimension.py](./notebooks/grade/grade_and_dimension.py): grade as geometric dimension
- [notebooks/grade/involutions_and_grade_ops.py](./notebooks/grade/involutions_and_grade_ops.py): reverse, involute, conjugate, and grade projections
- [notebooks/grade/grade_structure.py](./notebooks/grade/grade_structure.py): even/odd structure and pseudoscalar parity
- [notebooks/grade/grade_routing_products.py](./notebooks/grade/grade_routing_products.py): how products route between grades
- [notebooks/grade/norms_units_inverses.py](./notebooks/grade/norms_units_inverses.py): square, norm, unit, and inverse
- [notebooks/grade/bivector_commutators.py](./notebooks/grade/bivector_commutators.py): bivectors as a Lie algebra of infinitesimal rotations
- [notebooks/grade/commutator_lie_jordan.py](./notebooks/grade/commutator_lie_jordan.py): antisymmetric vs symmetric product structure

### Subspaces

- [notebooks/subspaces/projectors.py](./notebooks/subspaces/projectors.py): line and plane projection with one GA story
- [notebooks/subspaces/subspace_actions.py](./notebooks/subspaces/subspace_actions.py): projection, rejection, and reflection as one family
- [notebooks/subspaces/duality_and_complements.py](./notebooks/subspaces/duality_and_complements.py): metric duality vs complement
- [notebooks/subspaces/subspace_representations.py](./notebooks/subspaces/subspace_representations.py): one subspace, several equivalent representations

### PGA

- [notebooks/pga/meets_joins_pga.py](./notebooks/pga/meets_joins_pga.py): PGA joins and affine meet extraction
- [notebooks/pga/meet_join_duality.py](./notebooks/pga/meet_join_duality.py): meet and join as dual incidence operations

### STA

- [notebooks/sta/lorentz_boost.py](./notebooks/sta/lorentz_boost.py): boosts and Minkowski diagrams in STA
- [notebooks/sta/relative_vectors_sta.py](./notebooks/sta/relative_vectors_sta.py): the Pauli subalgebra inside STA
- [notebooks/sta/null_vectors_sta.py](./notebooks/sta/null_vectors_sta.py): timelike, spacelike, and null vectors in STA
- [notebooks/sta/dirac_antiparticles_sta.py](./notebooks/sta/dirac_antiparticles_sta.py): Dirac negative-energy states in STA
- [notebooks/sta/thomas_wigner_rotation.py](./notebooks/sta/thomas_wigner_rotation.py): residual spatial rotation from non-collinear boosts
- [notebooks/sta/one_g_travel.py](./notebooks/sta/one_g_travel.py): constant proper acceleration in STA

## Notebook Families

The suite is now large enough that related notebooks should be framed as
companions rather than accidental repeats.

- reflections -> versors -> rotors:
  `notebooks/rotors/reflections_ga.py`, `notebooks/rotors/versor_composition.py`, `notebooks/rotors/rotors_from_reflections.py`
- rotor representations and interpolation:
  `notebooks/rotors/rotor_space.py`, `notebooks/rotors/rotor_logarithms.py`, `notebooks/rotors/rotor_slerp.py`, `notebooks/rotors/rotor_slerp_3d.py`
- blades, grades, and actions:
  `notebooks/grade/bivectors_are_planes.py`, `notebooks/grade/grade_and_dimension.py`, `notebooks/rotors/rotor_action_multivectors.py`, `notebooks/subspaces/subspace_actions.py`
- duality and incidence:
  `notebooks/subspaces/duality_and_complements.py`, `notebooks/subspaces/subspace_representations.py`, `notebooks/pga/meets_joins_pga.py`, `notebooks/pga/meet_join_duality.py`
- STA and relativity:
  `notebooks/sta/lorentz_boost.py`, `notebooks/sta/null_vectors_sta.py`, `notebooks/sta/thomas_wigner_rotation.py`, `notebooks/sta/one_g_travel.py`
- STA structure and quantum-adjacent ideas:
  `notebooks/sta/relative_vectors_sta.py`, `notebooks/sta/dirac_antiparticles_sta.py`

When adding a new notebook near an existing family, state explicitly what the
new notebook adds that the older one does not.

## Bottom Line

This repo is for short, well-shaped GA notebooks that make one idea click.

The standard is:

- concept first
- minimal but real math
- explicit computation
- synchronized symbolic and geometric views
- small, disciplined `marimo` cells
- conventions that make the notebooks easy to extend without fighting the tool
