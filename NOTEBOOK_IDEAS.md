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

## Current Priority Roadmap

Most of the earlier `next` candidates in this file have now been implemented.
The strongest remaining additions are the places where GA gives a reader a real
conceptual win rather than only a different notation.

### Highest-Priority Next Notebooks

#### 1. Inertia Tensor as a Bivector-to-Bivector Map

- `next`
- Suggested path: `notebooks/physics/inertia_tensor_bivector_map.py`

Goal:
- Show that inertia does not fundamentally map an “angular velocity vector” to an
  “angular momentum vector.” It maps a bivector generator of rotation to a
  bivector angular momentum.

Core claim:
- The inertia tensor is clearer when treated as a linear map on rotational plane
  elements.

Plot:
- body shape or mass-point configuration
- one chosen rotation plane
- input angular-velocity bivector coefficients vs output angular-momentum
  bivector coefficients

What to avoid:
- a full rigid-body simulation on the first pass
- too much matrix language too early

#### 2. Rotating Frames: Coriolis and Centrifugal Terms

- `next`
- Suggested path: `notebooks/physics/rotating_frames_ga.py`

Goal:
- Derive the familiar fictitious forces from a rotor-driven moving frame.

Core claim:
- Coriolis and centrifugal terms are not arbitrary corrections; they come from
  differentiating in a rotating frame, and the commutator structure is visible in
  GA.

Plot:
- particle trajectory in inertial vs rotating frames
- force-term bars or vector overlays

What to avoid:
- too much mechanics notation at once

#### 3. Vector Derivative Sequel in 3D / STA

- `next`
- Suggested path: `notebooks/sta/vector_derivative_in_sta.py`

Goal:
- Follow the 2D operator-routing notebook with a version where the derivative is
  clearly the same object behind grad, div, curl, and the STA Maxwell equation.

Core claim:
- The vector derivative is one geometric object whose grade channels recover the
  standard differential operators.

Plot:
- one scalar field and one vector field in 3D slices
- grade-channel readout for `∇v`

What to avoid:
- turning the first sequel into a full PDE notebook

#### 4. Rotor Blending Beyond Two Orientations

- `next`
- Suggested path: `notebooks/rotors/multi_rotor_blending.py`

Goal:
- Extend slerp to a weighted blend of several orientations.

Core claim:
- Rotor logarithms make multi-orientation blending geometrically coherent in a
  way that ad hoc coefficient interpolation is not.

Plot:
- a few key orientations on the sphere
- blended result under changing weights

What to avoid:
- jumping immediately to skinning jargon without first making the geometry clear

#### 5. Reflection and Refraction from Subspace Geometry

- `next`
- Suggested path: `notebooks/subspaces/reflection_refraction.py`

Goal:
- Use decomposition relative to a surface normal to derive reflection and simple
  refraction.

Core claim:
- surface response is subspace decomposition plus one propagation rule

Plot:
- surface line, incident ray, reflected ray, refracted ray

What to avoid:
- mixing in Fresnel amplitudes here; keep this notebook geometric

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

### Stress-Energy / Momentum Flow in EM

- `backlog`

Goal:
- show how energy and momentum flow can be described from the field algebraically

Core claim:
- STA can express field structure and field transport in one language

### Observer Dependence of Event Order from a Calculus View

- `backlog`

Goal:
- follow the existing event-order notebook with one that ties the ordering issue
  to spacetime foliations and observer-relative time functions

Core claim:
- “which event is first?” is not a raw spacetime fact for spacelike separation;
  it depends on the observer’s chosen timelike direction field

### Null Congruences and Real Twistor Precursors

- `backlog`

Goal:
- continue the conformal STA / null-geometry strand toward families of null rays
  rather than one ray at a time

Core claim:
- the right precursor to twistors is not complex machinery first, but the real
  incidence geometry of null directions, celestial spheres, and congruences

### Dirac Matrices vs STA Extensions

- `backlog`

Goal:
- continue the existing matrix-vs-STA notebook family with one narrow sequel

Core claim:
- once one comparison is understood, many matrix identities become geometric
  statements about multivectors and operators

Warning:
- keep the scope tight; compare one or two ideas, not all of Dirac theory

## Backlog: PGA Topics

### Camera Geometry in PGA

- `backlog`

Goal:
- show how rays from a scene point pass through a pinhole to an image plane

Core claim:
- PGA makes incidence primary in camera geometry: scene point, pinhole, and image
  point are linked by one projective line story

### Robot / Linkage Kinematics in PGA

- `backlog`

Goal:
- extend the rigid-motion strand into articulated mechanisms

Core claim:
- links, joints, and rigid motions are naturally projective / motor geometry

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

## Backlog: New High-Value Topic Families

These are the newer gaps that look especially strong now that the repo has a
much broader base.

### Mechanics and Dynamics

- `backlog` `notebooks/physics/precession_and_nutation_ga.py`
  Focus: rotor-driven rigid-body precession and nutation.
  Core claim: the evolving rotor and its bivector generator carry the dynamics
  more cleanly than Euler-angle bookkeeping.

- `backlog` `notebooks/physics/action_angle_geometry.py`
  Focus: orbital / rotational phase geometry.
  Core claim: GA can package angle, plane, and conserved geometric structure in
  one language.

### Electromagnetism and Gauge Structure

- `backlog` `notebooks/quantum/gauge_phase_vs_holonomy.py`
  Focus: local phase changes vs gauge-invariant loop phase.
  Core claim: Aharonov-Bohm is the cleanest physical reminder that local
  potentials and closed-loop holonomy play different roles.

- `backlog` `notebooks/sta/maxwell_from_calculus_side.py`
  Focus: derive the Maxwell split from the derivative operator itself.
  Core claim: the one-line Maxwell equation is persuasive only if the reader sees
  how the derivative operator packages the standard pieces.

### Quantum and Information

- `backlog` `notebooks/quantum/entanglement_as_geometric_correlation.py`
  Focus: entanglement framed as constrained joint geometry rather than spooky
  matrix data.
  Core claim: some entangled structure is best understood as relational geometry
  between measurement contexts.

- `backlog` `notebooks/quantum/two_qubit_geometry_intro.py`
  Focus: first honest step beyond the single-qubit Bloch picture.
  Core claim: the jump from one qubit to two is not “just a bigger Bloch sphere,”
  and GA can help organize what changes.

### Algebra and Representation Theory

- `backlog` `notebooks/grade/clifford_group_intro.py`
  Focus: Pin, Spin, versors, and the Clifford group in one explicit map.
  Core claim: the algebra is not just a bag of products; it has a transformation
  group structure generated by reflections.

- `backlog` `notebooks/grade/blade_naming_and_notation_as_pedagogy.py`
  Focus: how notation changes what the reader sees.
  Core claim: basis naming, dual conventions, and blade factories are not cosmetic
  in a teaching repo; they shape the conceptual layer directly.

## Guidance for Implementing Any of These

When building a new notebook from one of these briefs:

1. Pick one sentence that states the notebook’s main claim.
2. Keep the control set small and meaningful.
3. Prefer one main interactive loop over several disconnected sections.
4. Use plots to validate the claim, not decorate the notebook.
5. If the topic overlaps an existing notebook, explain the difference in the intro.
6. Choose the algebra that makes the concept clearest, not the most general one.
7. If a lower-dimensional algebra tells the story better, prefer that.
