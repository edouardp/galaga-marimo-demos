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

For notebook-authoring guidance aimed at coding assistants and contributors,
see:

- `AUTHORING_NOTEBOOKS.md`

## Scope

The repo currently focuses on:

- Euclidean rotor intuition
- spacetime algebra and boosts
- conformal geometric algebra in 2D and 3D
- conformal spacetime as a bridge toward null and twistor-adjacent geometry
- rotor interpolation
- geometric projectors
- short, interactive derivations

New notebooks should fit that level and style unless there is a clear reason to
expand the scope.

## Current Notebook Families

The repo is now broad enough that notebooks should usually be thought of in
families rather than as isolated files.

### Rotor and Euclidean GA strand

Representative files:

- `notebooks/rotors/reflections_ga.py`
- `notebooks/rotors/versor_composition.py`
- `notebooks/rotors/rotor_space.py`
- `notebooks/rotors/rotor_slerp.py`
- `notebooks/rotors/rotor_slerp_3d.py`
- `notebooks/rotors/one_sided_rotor_action.py`

This strand is about:

- reflections
- versors and rotors
- rotor interpolation
- what sandwiching is really doing

### Grade and algebra-mechanics strand

Representative files:

- `notebooks/grade/grade_and_dimension.py`
- `notebooks/grade/involutions_and_grade_ops.py`
- `notebooks/grade/inner_product_polarization.py`
- `notebooks/grade/inner_left_right_contractions.py`
- `notebooks/grade/inner_product_family.py`
- `notebooks/grade/commutator_lie_jordan.py`

This strand is about:

- grade structure
- algebraic product families
- scalar / bivector routing
- Lie vs Jordan structure

### Subspace and incidence strand

Representative files:

- `notebooks/subspaces/subspace_actions.py`
- `notebooks/subspaces/duality_and_complements.py`
- `notebooks/subspaces/line_triangle_intersection.py`
- `notebooks/subspaces/barycentric_from_areas.py`
- `notebooks/subspaces/polygon_area_bivectors.py`

This strand is about:

- projection / rejection / reflection
- duality and complements
- incidence and intersection
- oriented areas and polygon geometry

### PGA strand

Representative files:

- `notebooks/pga/meets_joins_pga.py`
- `notebooks/pga/meet_join_duality.py`
- `notebooks/pga/screw_motion_pga.py`

This strand is about:

- joins and incidence
- duality in projective geometry
- rigid motions and screw motions in PGA

### Quantum and spin strand

Representative files:

- `notebooks/quantum/stern_gerlach_intro.py`
- `notebooks/quantum/stern_gerlach_sequence.py`
- `notebooks/quantum/spinor_double_cover.py`
- `notebooks/quantum/spinor_sign_interferometer.py`
- `notebooks/quantum/exchange_symmetry_pauli.py`
- `notebooks/quantum/pauli_matrices_vs_ga.py`

This strand is about:

- Bloch-vector intuition
- spin measurement
- double cover and spinor sign
- exchange symmetry and exclusion
- matrix vs GA descriptions

### STA and relativistic physics strand

Representative files:

- `notebooks/sta/lorentz_boost.py`
- `notebooks/sta/one_g_travel.py`
- `notebooks/sta/electromagnetism_one_bivector.py`
- `notebooks/sta/em_waves_sta.py`
- `notebooks/sta/maxwell_equations_sta.py`
- `notebooks/sta/dirac_matrices_vs_sta.py`

This strand is about:

- boosts and rapidity
- STA fields and invariants
- electromagnetic waves and Maxwell
- Dirac/STA comparisons

### CGA strand

Representative files:

- `notebooks/cga/cga_2d_null_basis.py`
- `notebooks/cga/cga_2d_points_and_distance.py`
- `notebooks/cga/cga_2d_lines_and_circles.py`
- `notebooks/cga/cga_2d_up_and_down.py`
- `notebooks/cga/cga_2d_point_pairs_and_intersections.py`
- `notebooks/cga/cga_2d_translations.py`
- `notebooks/cga/cga_2d_rigid_motions.py`
- `notebooks/cga/cga_3d_spheres_and_planes.py`

This strand is about:

- conformal lifts
- distance in the conformal inner product
- lines, circles, spheres, and planes
- point pairs and intersections
- conformal translations and rigid motions

Suggested reading order:

1. `notebooks/cga/cga_2d_null_basis.py`
2. `notebooks/cga/cga_2d_points_and_distance.py`
3. `notebooks/cga/cga_2d_up_and_down.py`
4. `notebooks/cga/cga_2d_lines_and_circles.py`
5. `notebooks/cga/cga_2d_point_pairs_and_intersections.py`
6. `notebooks/cga/cga_2d_point_pair_splitting.py`
7. `notebooks/cga/cga_2d_translations.py`
8. `notebooks/cga/cga_2d_rigid_motions.py`
9. `notebooks/cga/cga_2d_inversion_in_circle.py`
10. `notebooks/cga/cga_3d_spheres_and_planes.py`

### Conformal STA and Twistor-Precursor strand

Representative files:

- `notebooks/sta/conformal_null_rays.py`
- `notebooks/sta/conformal_translations_sta.py`
- `notebooks/sta/conformal_null_infinity.py`
- `notebooks/sta/celestial_circle_at_event.py`
- `notebooks/sta/null_directions_celestial_sphere.py`

This strand is about:

- conformal spacetime null rays
- translations as conformal versor actions
- null infinity
- celestial spheres / circles at events
- the real geometric ingredients that later point toward twistor theory

Suggested reading order:

1. `notebooks/sta/null_directions_celestial_sphere.py`
2. `notebooks/sta/conformal_null_rays.py`
3. `notebooks/sta/conformal_translations_sta.py`
4. `notebooks/sta/conformal_null_infinity.py`
5. `notebooks/sta/celestial_circle_at_event.py`

These notebooks are intentionally real and geometric first. They are not a full
twistor-theory sequence; they are a conformal/null-geometry on-ramp that points
toward the incidence structures twistor theory later organizes.

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
- [notebooks/subspaces/polygon_area_bivectors.py](./notebooks/subspaces/polygon_area_bivectors.py): polygon area from signed bivector fan sums

### PGA

- [notebooks/pga/meets_joins_pga.py](./notebooks/pga/meets_joins_pga.py): PGA joins and affine meet extraction
- [notebooks/pga/meet_join_duality.py](./notebooks/pga/meet_join_duality.py): meet and join as dual incidence operations

### STA

- [notebooks/sta/lorentz_boost.py](./notebooks/sta/lorentz_boost.py): boosts and Minkowski diagrams in STA
- [notebooks/sta/relative_vectors_sta.py](./notebooks/sta/relative_vectors_sta.py): the Pauli subalgebra inside STA
- [notebooks/sta/null_vectors_sta.py](./notebooks/sta/null_vectors_sta.py): timelike, spacelike, and null vectors in STA
- [notebooks/sta/null_directions_celestial_sphere.py](./notebooks/sta/null_directions_celestial_sphere.py): null directions and the celestial sphere as a real twistor precursor
- [notebooks/sta/dirac_antiparticles_sta.py](./notebooks/sta/dirac_antiparticles_sta.py): Dirac negative-energy states in STA
- [notebooks/sta/thomas_wigner_rotation.py](./notebooks/sta/thomas_wigner_rotation.py): residual spatial rotation from non-collinear boosts
- [notebooks/sta/one_g_travel.py](./notebooks/sta/one_g_travel.py): constant proper acceleration in STA

### Quantum and Spin

- [notebooks/quantum/stern_gerlach_intro.py](./notebooks/quantum/stern_gerlach_intro.py): one-machine Stern-Gerlach probabilities and output states
- [notebooks/quantum/stern_gerlach_sequence.py](./notebooks/quantum/stern_gerlach_sequence.py): three-machine Stern-Gerlach path filtering and branching
- [notebooks/quantum/spinor_double_cover.py](./notebooks/quantum/spinor_double_cover.py): `Spin(2)` versus `SO(2)` and the rotor double cover
- [notebooks/quantum/qubit_superposition.py](./notebooks/quantum/qubit_superposition.py): qubit pure states as Bloch-sphere directions
- [notebooks/quantum/crossed_polarizers.py](./notebooks/quantum/crossed_polarizers.py): crossed polarizers as projection geometry

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
- spin and quantum-adjacent intuition:
  `notebooks/quantum/stern_gerlach_intro.py`, `notebooks/quantum/stern_gerlach_sequence.py`, `notebooks/quantum/spinor_double_cover.py`, `notebooks/quantum/qubit_superposition.py`, `notebooks/quantum/crossed_polarizers.py`

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
