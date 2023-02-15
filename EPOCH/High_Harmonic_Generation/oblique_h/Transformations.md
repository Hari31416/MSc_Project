# Transformations

All the simulations are done in the M-frame, however, vizualization and stuffs are performed in L-frame. The transformation between the two frames is given by the following equations.

## Definitions

We define the following variables:

- $\alpha$ : The angle of incident of the laser beam on the mirror (This will become zero in M-Frame)
- $\beta =  \cos\alpha$: The beta-factor
- $\Gamma = \sin\alpha$: Gamma-Factor
- $\omega_0$: The 'original' angular frequency of the laser beam
- $\omega_L$: The angular frequency of the laser beam in the L-frame
- $\omega_M$: The angular frequency of the laser beam in the M-frame
- $\lambda_0$: The 'original' wavelength of the laser beam
- $\lambda_L$: The wavelength of the laser beam in the L-frame
- $\lambda_M$: The wavelength of the laser beam in the M-frame
- $\tau_0$: The 'original' time period of the laser beam
- $\tau_L$: The time period of the laser beam in the L-frame
- $\tau_M$: The time period of the laser beam in the M-frame
- $E_0$: The 'original' electric field of the laser beam
- $\mathbf{E_L}$: The electric field of the laser beam in the L-frame
- $\mathbf{E_M}$: The electric field of the laser beam in the M-frame
- $I_0$ : The 'original' intensity of the laser beam
- $I_L$ : The intensity of the laser beam in the L-frame
- $I_M$ : The intensity of the laser beam in the M-frame
- $n_0$ : The 'original' plasma density
- $n_L$ : The plasma density in the L-frame
- $n_M$ : The plasma density in the M-frame

## The Transformation Equations

Here are the transformations between the two frames:

| Quantity                   | L-Frame                                 | M-Frame             |
| -------------------------- | --------------------------------------- | ------------------- |
| $\omega$                   | $\omega_0$                              | $\omega_0 \beta$    |
| $\lambda$                  | $\lambda_0$                             | $\lambda_0/\beta$   |
| $n$                        | $n_0$                                   | $n_0/\beta$         |
| $\mathbf{E}$ (p-polarized) | $E_0 (-\Gamma \hat{x} + \beta \hat{y})$ | $E_0 \beta \hat{y}$ |
| $\mathbf{E}$ (s-polarized) | $E_0 \hat{z}$                           | $E_0 \beta \hat{z}$ |

## Simulation Remarks

$a_0$ remains the same.

$I \propto E^2$ decreases by a factor of $\cos^2\alpha$

$\alpha = 0$ should give the usual results.

> Write the input deck such that both the 'original' and the 'transformed' quantities are present.

Parameters which are needed to be changed in the input deck are:

1. Wavelength
2. Density
3. Intensity

In the deck file, $\omega$ and the laser time (laser length) depends on $\lambda$ so, just change $\lambda$

Change the `max_den` parameter to change density.

$a_0$ is

$$
a_0^2 = \frac{I\lambda_0^2}{1.37\times 10^{18} Wcm^{-2}\mu m ^2}
$$

In input deck, intensity is defined as

$$
I = a_0^2\times 1.37 \times 10^{22}
$$

So, we assume that the wavelenth is $1 \mu m$. However, wavelength is increasing here so, let's rewrite the intensity in the full form:

$$
I = \frac{a_0^2 \times 1.37\times 10^{18}}{\lambda^2}
$$

Still assuming that the wavelength is in $\mu m$. All this was in L-Frame. In M-frame

$$
I = \frac{a_0^2 \times 1.37\times 10^{18}}{\lambda_M^2}
$$

So, it basically decreases by $\beta ^2$.

$$
I_M = I_L\times \beta^2
$$

So, assuming that $\lambda_0 = 1 \mu m$, we can safely write

$$
I_M = a_0^2\times 1.37 \times 10^{22} \times \beta^2
$$

## Plotting Remarks

Do every plot in L-Frame. For this, you need to use transformation equations.
