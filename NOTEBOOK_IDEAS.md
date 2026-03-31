# Notebook Ideas

This file is a working design brief for the notebook suite in this repo.

It has two jobs:

- record the notebook ideas that have already come up in discussion
- give enough detail that another agent can implement a notebook from the brief

The repo style is assumed throughout:

- concept-first, not API-first
- one main idea per notebook
- short algebra-intro markdown cell before `Algebra(...)`
- controls defined earlier, rendered in the same main output cell as `gm.md(...)` and the plot
- local-only intermediates underscored
- exported notebook names plain and intentional
- verify with `uv`

## Status Labels

- `done`: already implemented in this repo
- `next`: strong candidate to build next
- `backlog`: worthwhile, but not yet prioritized

## Existing Notebook Families

### Rotors and Reflections

- `done` `notebooks/rotors/reflections_ga.py`
  Focus: reflection as the primitive rigid motion.
  Core claim: `v' = -n v n` is already a complete geometric action, and rotors are built from reflections.
  Plot: mirror line plus input/output vectors.

- `done` `notebooks/rotors/versor_composition.py`
  Focus: composing reflections into a versor.
  Core claim: geometric multiplication composes transformations directly.
  Plot: first reflection, second reflection, and equivalent versor action.

- `done` `notebooks/rotors/rotors_from_reflections.py`
  Focus: two reflections give a rotor.
  Core claim: rotors are even versors built from reflection composition.

- `done` `notebooks/rotors/rotor_space.py`
  Focus: vectors rotate by sandwiching, rotors move by single-sided multiplication.
  Core claim: vectors and rotors live in different spaces.
  Plot: rotor space on the left, vector space on the right.

- `done` `notebooks/rotors/rotor_slerp.py`
  Focus: 2D rotor interpolation.
  Core claim: 2D rotor slerp is conceptually clean but not the strongest GA payoff.

- `done` `notebooks/rotors/rotor_slerp_3d.py`
  Focus: 3D rotor interpolation across changing planes.
  Core claim: GA still gives one rotor interpolation story when the rotation plane changes.

- `done` `notebooks/rotors/rotor_logarithms.py`
  Focus: recovering a bivector generator from a rotor.
  Core claim: `log(R)` exposes the plane-and-angle information packed into a rotor.

- `done` `notebooks/rotors/rotor_action_multivectors.py`
  Focus: sandwich action on more than vectors.
  Core claim: rotors preserve grade and rotate bivectors and higher-grade objects too.

### Grade Structure and Algebra Mechanics

- `done` `notebooks/grade/bivectors_are_planes.py`
  Focus: bivectors as oriented plane elements.
  Core claim: a bivector is a geometric plane/area object, not just an antisymmetric algebraic leftover.

- `done` `notebooks/grade/grade_and_dimension.py`
  Focus: grade as geometric dimension.
  Core claim: scalar/vector/bivector/trivector are geometric dimensions, not arbitrary tags.

- `done` `notebooks/grade/involutions_and_grade_ops.py`
  Focus: reverse, involute, conjugate, and grade decomposition.
  Core claim: involutions are grade-structured symmetries.

- `done` `notebooks/grade/grade_structure.py`
  Focus: even/odd subalgebras, pseudoscalar parity, and dimension dependence.
  Core claim: grade structure is broader than one algebra example; the pseudoscalar commutation story depends on dimension parity.

- `done` `notebooks/grade/grade_routing_products.py`
  Focus: products as grade routers.
  Core claim: in `Cl(2,0)`, `ab = a·b + a∧b` is the cleanest first example of products selecting grade routes.
  Plot: vectors and oriented area on the left, signed grade routing bars on the right.

- `done` `notebooks/grade/norms_units_inverses.py`
  Focus: square, norm, unit, inverse.
  Core claim: these are related but distinct questions about an object.

- `done` `notebooks/grade/bivector_commutators.py`
  Focus: bivectors as the Lie algebra of infinitesimal rotations.
  Core claim: bivector commutators encode rotational structure.

- `done` `notebooks/grade/commutator_lie_jordan.py`
  Focus: antisymmetric vs symmetric product splits.
  Core claim: commutator/Lie and anticommutator/Jordan expose different structure in the same geometric product.

### Subspaces and Euclidean Geometry

- `done` `notebooks/subspaces/projectors.py`
  Focus: projection onto lines and planes.
  Core claim: one projector story works across subspace dimensions.

- `done` `notebooks/subspaces/subspace_actions.py`
  Focus: projection, rejection, reflection as a family.
  Core claim: these are coordinated subspace actions, not isolated formulas.

- `done` `notebooks/subspaces/duality_and_complements.py`
  Focus: metric duality vs complement.
  Core claim: they may coincide in Euclidean examples, but they are not the same operation.

- `done` `notebooks/subspaces/subspace_representations.py`
  Focus: same subspace, different representation.
  Core claim: blade, dual, and complement views can describe the same geometry while making different operations easier.

- `done` `notebooks/subspaces/line_triangle_intersection.py`
  Focus: ray-triangle intersection in `Cl(3,0)`.
  Core claim: Euclidean GA is enough for plane hit plus inside-triangle test.
  Plot: fixed triangle, constrained ray, hit point, and barycentric classification.

### PGA and Incidence

- `done` `notebooks/pga/meets_joins_pga.py`
  Focus: joins of points and meet of lines.
  Core claim: PGA keeps incidence primary; affine formulas are secondary extraction.

- `done` `notebooks/pga/meet_join_duality.py`
  Focus: meet and join as dual operations.
  Core claim: join and meet are the same incidence machinery seen through complementary representations.

### STA and Relativity

- `done` `notebooks/sta/lorentz_boost.py`
  Focus: boosts and Minkowski diagrams.
  Core claim: timelike bivectors generate boosts just as spacelike bivectors generate rotations.

- `done` `notebooks/sta/relative_vectors_sta.py`
  Focus: Pauli algebra inside STA.
  Core claim: Euclidean 3D vector algebra sits inside STA via `σ_i = γ_iγ_0`.

- `done` `notebooks/sta/null_vectors_sta.py`
  Focus: timelike, null, and spacelike vectors.
  Core claim: the sign of `v²` determines the geometric class, and boosts preserve it.

- `done` `notebooks/sta/thomas_wigner_rotation.py`
  Focus: residual spatial rotation after composing non-collinear boosts.
  Core claim: the leftover spatial rotor is the finite Thomas-Wigner rotation.

- `done` `notebooks/sta/one_g_travel.py`
  Focus: constant proper acceleration.
  Core claim: proper acceleration is simple in ship time and hyperbolic in Earth time.

- `done` `notebooks/sta/dirac_antiparticles_sta.py`
  Focus: negative-energy / antiparticle structure in STA.
  Core claim: the negative branch is natural in spacetime algebra, not an artifact of matrix machinery.

- `done` `notebooks/sta/electromagnetism_one_bivector.py`
  Focus: `F = E + I B`.
  Core claim: electric and magnetic fields are observer-relative parts of one bivector.

- `done` `notebooks/sta/moving_charge_magnetic_field.py`
  Focus: magnetism emerging from a boosted pure electric field.
  Core claim: in the charge rest frame the field can be purely electric; in a lab frame the same boosted bivector develops a magnetic part.

## Strong Next Candidates

### 1. Boosting the Electromagnetic Field

- `next`
- Suggested path: `notebooks/sta/boosting_em_field.py`

Goal:
- Show that a boost mixes electric and magnetic parts because the field is one bivector `F`.

Core claim:
- A pure electric or pure magnetic field in one frame need not stay pure under a boost.

Algebra:
- Use `Cl(1,3)` with `(+, -, -, -)`.
- Build `F = E + I B`.
- Choose a boost rotor `R = exp(-(φ/2) γ0 n)`.
- Compute `F' = R F ~R`.
- Extract `E' = F' | γ0`.
- Extract `B'` by projecting `F'` onto the `Iσ_i` basis.

Controls:
- a few field components, not all six
- one boost rapidity slider
- one boost direction dropdown or simple plane choice

Plot:
- left: 3D lab-relative `E` and `B` arrows before/after
- right: bivector basis coefficient bars before/after

What to avoid:
- a six-component control panel
- too much derivation about Maxwell equations
- mixing in Lorentz force; keep this notebook about field transformation only

### 2. Lorentz Force from Bivector Action

- `next`
- Suggested path: `notebooks/sta/lorentz_force_from_F.py`

Goal:
- Show how the field bivector acts on particle velocity and why electric and magnetic responses feel different.

Core claim:
- `F` acting on the particle state naturally separates into acceleration along `E` and turning by `B`.

Algebra:
- Start with one simple `F`
- Use a particle four-velocity or relative velocity
- Build a pedagogical force expression rather than a full integrator if needed

Controls:
- magnetic field along one axis
- optional electric field along another
- initial velocity direction

Plot:
- velocity-space curve or qualitative trajectory
- maybe a companion panel for `E`, `B`, and `v`

What to avoid:
- too much numerical ODE machinery unless it directly supports the teaching goal

### 3. Electromagnetic Invariants

- `next`
- Suggested path: `notebooks/sta/em_invariants.py`

Goal:
- Center a notebook on `F²` and what its scalar and pseudoscalar parts mean.

Core claim:
- The invariant content of the field is cleaner in STA than in separate vector formulas.

Algebra:
- Compute `F²`
- Show `⟨F²⟩0`
- Show `⟨F²⟩4`
- Explain electric-dominated vs magnetic-dominated vs null field cases

Controls:
- two or three field components only

Plot:
- coefficient bars and a small classification panel

What to avoid:
- treating this as just a symbolic printout; the classification should be obvious

### 4. Barycentric Coordinates from Oriented Areas

- `next`
- Suggested path: `notebooks/subspaces/barycentric_from_areas.py`

Goal:
- Make the inside-triangle test and barycentric coordinates their own notebook.

Core claim:
- Barycentric weights are oriented area ratios, so “inside/outside” is a geometric sign test, not an arbitrary algorithm.

Algebra:
- Stay in `Cl(3,0)` or even a 2D Euclidean setup embedded in 3D
- Triangle area from wedge of edge vectors
- Subtriangle areas from wedges against a point
- Normalize by total area

Controls:
- one point inside/near triangle
- maybe a small triangle-shape deformation slider

Plot:
- triangle, point, subareas shaded by weight or sign

What to avoid:
- burying the idea inside line-triangle intersection logic

### 5. Reflection and Refraction from Surface Geometry

- `next`
- Suggested path: `notebooks/subspaces/reflection_refraction.py`

Goal:
- Use surface normals and decomposition into parallel/perpendicular parts to derive reflection and maybe simple refraction.

Core claim:
- surface response is just subspace decomposition plus one geometric rule

Algebra:
- decompose incident direction relative to a normal
- reflection by flipping the normal component
- optional Snell law extension for refraction

Controls:
- incident angle
- refractive index ratio if refraction is included

Plot:
- surface line/plane, incident ray, reflected ray, refracted ray

What to avoid:
- overcomplicating with Fresnel coefficients unless the notebook is explicitly about that

## Backlog: Good Geometry Topics

### Line-Plane Distance and Projection

- `backlog`

Goal:
- give a compact notebook around distance to a plane and orthogonal projection

Core claim:
- rejection gives distance-bearing geometry directly

Plot:
- point, plane, projected point, rejection vector

### Segment-Triangle or Line-Plane Intersection Family

- `backlog`

Goal:
- grow the current line-triangle notebook into a small family of geometry query notebooks

Core claim:
- once the GA object setup is right, several intersection tests look like close cousins

### Winding and Orientation Tests

- `backlog`

Goal:
- 2D orientation sign, side-of-line, winding intuition

Core claim:
- wedge sign is already the orientation predicate

Plot:
- line and moving point
- signed area visualization

## Backlog: Further STA / Physics Topics

### Maxwell as One STA Equation

- `backlog`

Goal:
- show the compact STA Maxwell equation as the unification of the usual four equations

Core claim:
- one STA equation packages divergence and curl structure together

Warning:
- keep this concept-first; do not turn it into a full EM course notebook

### Electromagnetic Waves in STA

- `backlog`

Goal:
- plane-wave field as a null or constrained bivector field

Core claim:
- propagation and orthogonality are cleaner in STA field language

### Stress-Energy / Momentum Flow in EM

- `backlog`

Goal:
- show how energy and momentum flow can be described from the field algebraically

Core claim:
- STA can express field structure and field transport in one language

### Dirac Matrices vs STA

- `backlog`

Goal:
- side-by-side notebook comparing matrix and STA descriptions

Core claim:
- the matrix language can be re-read as geometry

Warning:
- keep the scope tight; compare one or two ideas, not all of Dirac theory

## Backlog: PGA Topics

### Motors in PGA

- `backlog`

Goal:
- show translations and rotations unified as motors

Core claim:
- rigid motions in Euclidean space are one motor story in PGA

Plot:
- simple shape moved by translation, rotation, then a motor

### Line / Plane Incidence in PGA

- `backlog`

Goal:
- return to projective incidence after the Euclidean intersection notebooks

Core claim:
- PGA makes incidence primary rather than derived

## Backlog: Bilinear Operations

These are good companions to `notebooks/grade/inner_product_polarization.py`. They keep the focus on two-input geometric operations rather than on a larger physics or subspace application.

### Outer Product as Bilinear Oriented Area

- `backlog`

Goal:
- build the wedge product as the antisymmetric bilinear partner to the dot product notebook

Core claim:
- the outer product is bilinear, signed, and measures oriented area rather than overlap

Suggested algebra:
- `Cl(2,0)`

Suggested controls:
- one fixed vector
- one rotating vector
- optional length slider for the second vector

Suggested visuals:
- the two vectors
- the parallelogram they span
- a signed area readout or a bivector coefficient bar

What to emphasize:
- bilinearity: doubling one input doubles the area element
- antisymmetry: swapping inputs flips the sign
- comparison to the polarization notebook: dot product from squared lengths, wedge product from oriented area

### Symmetric vs Antisymmetric Bilinear Split

- `backlog`

Goal:
- make the decomposition of the geometric product into symmetric and antisymmetric bilinear pieces the entire point

Core claim:
- for vectors, the geometric product packages two different bilinear geometries at once

Suggested algebra:
- `Cl(2,0)`

Suggested controls:
- angle between two vectors
- optional length control for one vector

Suggested visuals:
- left panel: the two vectors and their parallelogram
- right panel: scalar channel vs bivector channel, with the full geometric product shown alongside

What to emphasize:
- `ab = a \cdot b + a \wedge b`
- the dot product is symmetric
- the wedge product is antisymmetric
- this notebook should overlap with `grade_routing_products.py` only if the framing is more explicitly “bilinear split” than “grade routing”

### Quadratic Form vs Bilinear Form

- `backlog`

Goal:
- pair `v^2` and `u \cdot v` directly so readers see the difference between quadratic and bilinear structure

Core claim:
- the metric first appears as a quadratic form on one vector, and polarization recovers the bilinear form on two vectors

Suggested algebra:
- `Cl(2,0)` first, with a possible later STA companion

Suggested controls:
- one vector for the quadratic side
- two-vector configuration for the bilinear side

Suggested visuals:
- one panel for squared length
- one panel for the polarization identity reconstruction

What to emphasize:
- why the identity is called “polarization”
- how a one-input square contains enough structure to recover a two-input product

### Bilinear Forms in Different Signatures

- `backlog`

Goal:
- compare Euclidean and spacetime bilinear structure using the same notebook design

Core claim:
- the same bilinear machinery behaves differently when the metric signature changes

Suggested algebra:
- side-by-side `Cl(2,0)` and STA `Cl(1,1)` or `Cl(1,3)` slices

Suggested controls:
- one shared pair of coefficient sliders
- optional toggle between Euclidean and spacetime interpretation

Suggested visuals:
- Euclidean plot of vectors and lengths
- Minkowski diagram or sign table for the spacetime case

What to emphasize:
- in Euclidean signature, squares are always nonnegative
- in spacetime signature, the bilinear form classifies timelike / spacelike / null directions
- this should be framed as a bilinear-signature notebook, not just another null-vector notebook

### Projection as a Bilinear Scalar Feeding a Geometric Construction

- `backlog`

Goal:
- show that a projection is not a primitive black box; it is built from a bilinear scalar and a direction

Core claim:
- `\mathrm{proj}_n(v) = (v \cdot n)n` turns the inner product into a concrete vector output

Suggested algebra:
- `Cl(2,0)`

Suggested controls:
- fixed or slowly rotating projection direction
- movable input vector

Suggested visuals:
- input vector
- projected component
- rejected component
- scalar readout of `v \cdot n`

What to emphasize:
- the inner product itself is scalar-valued
- the projection vector is built by feeding that scalar back into the geometry
- this notebook should complement `projectors.py` by foregrounding the bilinear origin of projection

### Bilinear Electromagnetic Self-Products

- `backlog`

Goal:
- make the invariant content of `F^2` feel like a genuine bilinear story rather than just “square the field”

Core claim:
- the important electromagnetic invariants come from bilinear self-combinations of the Faraday bivector

Suggested algebra:
- STA `Cl(1,3)`

Suggested controls:
- observer-relative electric and magnetic component sliders
- optional boost direction or field family presets

Suggested visuals:
- one panel for `E` and `B`
- one panel for the scalar and pseudoscalar invariant channels

What to emphasize:
- `F^2` contains scalar and pseudoscalar information
- the field classification comes from those bilinear invariant pieces
- this should build on `notebooks/sta/em_invariants.py` rather than replace it

## Backlog: “Concept Glue” Notebooks

These are useful when the suite becomes large and we want bridge notebooks rather than only new topics.

### Products as Geometry Selectors

- `backlog`

Goal:
- unify projection, rejection, reflection, and routing in one story

Core claim:
- many named GA operations are grade-aware or subspace-aware selection rules

### Exponential as Flow

- `backlog`

Goal:
- show `exp(generator * t)` as continuous motion

Core claim:
- exponentials are not a trick for rotors only; they encode flow from generators

### One Geometry, Many Representations

- `backlog`

Goal:
- tie together duality, complement, relative vectors, and bivector-vs-vector viewpoints

Core claim:
- many “different” GA objects are representation changes around the same geometry

## Guidance for Implementing Any of These

When building a new notebook from one of these briefs:

1. Pick one sentence that states the notebook’s main claim.
2. Keep the control set small and meaningful.
3. Prefer one main interactive loop over several disconnected sections.
4. Use plots to validate the claim, not decorate the notebook.
5. If the topic overlaps an existing notebook, explain the difference in the intro.
6. Choose the algebra that makes the concept clearest, not the most general one.
7. If a lower-dimensional algebra tells the story better, prefer that.
