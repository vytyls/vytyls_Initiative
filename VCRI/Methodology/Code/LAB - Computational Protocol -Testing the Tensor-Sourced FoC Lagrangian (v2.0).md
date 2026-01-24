---
title: LAB - Computational Protocol - Testing the Tensor-Sourced FoC Lagrangian (v2.0)
date: 25.10.06
time: 18:05:00
author: Lative, Syence
source: Synthesis Session
tags:
  - focTheory
  - computation
  - tensorFields
  - PDE
---

## 1. Objective

The primary goal of this computational pass is to validate the new tensor-based formulation of the FoC Lagrangian. We will test whether a source term derived from the divergence of a simple, externally-defined tensor field can produce the same characteristic **threshold-driven domain formation** observed in our previous 1D PDE simulations that used a scalar source. This serves as a critical, low-cost sanity check before developing more complex models.

---

## 2. Methodology: Modifying the 1D PDE Toy Model

We will adapt the existing 1D PDE simulation framework. The core PDE remains:
$$
\partial_t^2 A - c^2 \partial_x^2 A + \gamma \partial_t A + \frac{dV}{dA} = \text{Source}(x,t)
$$

The key modification is to replace the old scalar source, $I(x,t)$, with the new source term derived from the v2.0 Lagrangian's equations of motion:
$$
\text{Source}(x,t) = J^\rho(x,t) = \frac{1}{2} \lambda \partial_\sigma T^{\sigma\rho}_{\text{intent}}(x,t)
$$

---

## 3. A Simple Tensor Ansatz

To make this computationally tractable, we will not simulate a full 4D tensor. Instead, we will define a simple, spatially and temporally localized **tensor ansatz**. Following the suggestion in, we will use a form that primarily represents a "torque" or "flow" in a single spatial direction.

Let's define our simple Intention Tensor as having only two non-zero components, $T^{01}_{\text{intent}}$ and $T^{10}_{\text{intent}}$ (antisymmetric):
$$
T^{01}_{\text{intent}}(x,t) = -T^{10}_{\text{intent}}(x,t) = A_0 \cdot \exp\left(-\frac{(x-x_0)^2}{2\sigma_x^2}\right) \cdot \exp\left(-\frac{(t-t_0)^2}{2\sigma_t^2}\right)
$$
-   $A_0$ is the sweepable amplitude of the intention.
-   The Gaussian terms provide localization in space ($x$) and time ($t$).

### 3.1 Deriving the Source Term

With this ansatz, the source term for our 1D simulation (where $\rho=0$ for the scalar potential $A_0 \approx A$) becomes:
$$
J^0(x,t) = \frac{1}{2} \lambda \left( \partial_0 T^{00} + \partial_1 T^{10} \right) = \frac{1}{2} \lambda \partial_x T^{10}_{\text{intent}}(x,t)
$$
This is a simple numerical derivative that can be calculated at each time step and fed into the PDE solver.

---

## 4. Simulation Protocol

1.  **Implement the Tensor Source:** Modify the existing 1D PDE code to replace the `I(x,t)` function with the new `J^0(x,t)` function, which computes the spatial derivative of the simple tensor ansatz defined above.
2.  **Parameter Sweep:** Perform a sweep of the tensor amplitude, $A_0$, across a range comparable to the previous scalar amplitude sweeps (e.g., $A_0 \in [0.0, 1.0]$). Keep other parameters (damping $\gamma$, potential shape, etc.) consistent with previous runs for direct comparison.
3.  **Primary Metric:** The primary success metric will be the **side-well occupancy** of the field at the end of the simulation. We will plot this metric against the input amplitude $A_0$.
4.  **Data Visualization:** Generate spacetime plots of the field $A(x,t)$ for several key values of $A_0$ (below, at, and above the observed threshold).

---

## 5. Expected Outcome & Success Criteria

The experiment will be considered a success if we observe a **sharp, non-linear increase in side-well occupancy** as the tensor amplitude $A_0$ crosses a critical threshold.

This result would confirm that the more sophisticated tensor-based Lagrangian is not only theoretically sound but also numerically stable and capable of reproducing the core threshold phenomenon of the FoC framework. A positive result will provide the confidence needed to proceed with more complex 2+1D simulations.