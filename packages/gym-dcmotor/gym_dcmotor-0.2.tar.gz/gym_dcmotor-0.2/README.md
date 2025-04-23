# Gym DCMotor

A simple DC Motor simulator in Python that uses the RK45 numerical ODE solver.

## Kinematic Equations

The dynamics of the DC motor are governed by the following equations:

### Armature Current ($I_a$):

$$
\frac{dI_a}{dt} = \frac{V_a - K_b \cdot \omega - R_a \cdot I_a}{L_a}
$$

### Angular Velocity ($\omega$):

$$
\frac{d\omega}{dt} = \frac{K_t \cdot I_a - B \cdot \omega - T_l}{J}
$$

### Parameters:

- $I_a$ : Armature current  
- $\omega$ : Angular velocity  
- $V_a$ : Applied voltage  
- $K_b$ : Back EMF constant  
- $R_a$ : Armature resistance  
- $L_a$ : Armature inductance  
- $K_t$ : Torque constant  
- $B$ : Viscous damping coefficient  
- $T_l$ : Load torque  
- $J$ : Moment of inertia  