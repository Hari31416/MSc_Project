# ROM

To induce large intensity boosts on the reflected laser beam, plasma mirrors need to be set in relativistic motion, which is possible when they are exposed to laser intensities ranging from at least $10^{18} W/cm^2$ up to the highest laser intensities available to date, of a few $10^{22} W/cm^2$. The incident laser field then drives a periodic oscillation of the plasma mirror surface, at relativistic velocities. This relativistic oscillating mirror (ROM) induces a periodic Doppler effect on the reflected field . Each time the mirror surface moves outward, it compresses the laser energy in time, leading to a sharpening of the reflected waveform. Although still periodic in time, this waveform is no longer sinusoidal: its spectrum thus consists of the combination of the laser frequency $\omega_n$ with a comb of high-order harmonics of frequencies $n\omega_n$. This physical process is now fairly well-understood theoretically.

## Models

### Purturabation Theory

Generation of harmonics of low order from plasmas can be treated by perturbation theory. It fails for high intensity.

### Relativistic Equations

Based on relativistic equation of motion and hydrodynamics approxiamation. The cutoff frequency is:

$$
n_{\max}^2 = n_p/n_c
$$

They demonstrated that the "principal source of high-harmonic emission is the strong non linear restoring force" which exists when resonant absorption occurs in a highlt steep density profile.

### Moving Mirror Model

”interpreted the harmonic generation as due to the Doppler effect produced by a reflecting charge sheet, formed in a narrow region at the plasma boundary, oscillating under the action of the laser pulse”. Maximum cutoff frequency $=4\gamma_{\max}^2$.

### Moving Mirror Model 2

The HH are generated due to sharp spikes in the relativistic $\gamma$ factor. Cutoff is $\sqrt{8\alpha }\gamma_{\max}^3$. This was done using the relativistic plasma similarity theory.

The electrons are driven by the laser light pressure, a restoring electrostatic force comes from the ions. As a consequence, the plasma surface oscillates and the electrons gain a normal momentum component. Since the plasma is overdense, the incident electromagnetic wave is not able to penetrate it. This means that there is an electric current along the plasma surface. For this reason, the momenta of electrons in the skin layer have, apart from the components normal to the plasma surface, also tangential components. Though the motion of the plasma surface is qualitatively different: its velocity $v_s$ is not ultra relativistic for most of the times but smoothly approaches c only when the tangential electron momentum vanishes . The $\gamma$-factor of the surface $\gamma_s$ also shows specific behavior. It has sharp peaks at those times for which the velocity of the surface approaches c. When $v_s$ reaches its maximum and $\gamma_s$ has a sharp peak, high harmonics of the incident wave are generated and can be seen in the reflected radiation. Physically this means that the high harmonics are due to the collective motion of bunches of fast electrons moving towards the laser pulse.

In the power law part the spectrum decays as:

$$
I_n \propto 1/n^{8/3}
$$

[Theory of high-order harmonic generation in relativistic laser interaction with overdense plasma](https://www.researchgate.net/publication/6644474_Theory_of_high-order_harmonic_generation_in_relativistic_laser_interaction_with_overdense_plasma)

## Oscillating Mirror Model

The interaction with light generates some periodic motion of the plasma in response to the electromagnetic forces. It is assumed that the duration of the light pulse is sufficiently short so that the motion of the ions may be neglected. The ions are treated as a fixed positive background charge.

The basic approximation of the oscillating mirror model is to neglect the details of the changes of the electron density profile and to represent the collective electronic motion by the motion of the boundary of the supercritical region. This boundary represents an effective reflecting surface performing an oscillatory motion, the oscillating mirror.

### Phase Modulation

Neglecting for a moment retardation effects the phase shift of the reflected wave resulting from a sinusoidal displacement of the reflecting surface in the z-direction:

$$
s(t) = s_0 \sin(\omega t)
$$

is given by

$$
\phi(t) = (2\omega_0s_0/c)\cos\theta \sin \omega_m t
$$

where $\theta$ is the angle of incidence and $\omega_m$ is the mirror frequency (modulation frequency). The electric field of the reflected wave is given by

$$
E_R \propto e^{-i\omega_0 t}e^{i\phi(t)} =  e^{-i\omega_0 t} \sum _{n \to -\infty}^{n \to -\infty}J_n(\xi) e^{-in\omega_m t}
$$

where $J_n(\xi)$ is the Bessel function of order $n$ and $\xi =( 2\omega_0s_0/c)\cos\theta$.

We can see that the phase modulation produced by the oscillating mirror
gives rise to a series of sidebands at distances from the
carrier frequency $\omega_0$ given by multiples of the modulation
frequency $\omega_m$.

The reflecting surface performs a periodic motion at a frequency $2\omega_0$, or a superposition of $\omega_0$ and $2\omega_0$ , depending on the polarization and angle of incidence of the incoming light. Thus, the modulation frequencies provided by the mirror motion are $\omega_m = \omega_0$ and/or $\omega_m = 2\omega_0$. The key point is that this type of modulation produces sidebands representing even and odd harmonics of the fundamental frequency $\omega_0$ . These ideas suggests an interpretation of high-order harmonic generation from a plasma—vacuum interface as a phase modulation from a periodically moving reflecting surface (Doppler shift).

#### s and p polarized light

- _p-polarized light_: The electric and the magnetic field are, respectively, parallel and perpendicular to the plane of incidence. The electrons move in the plane of incidence. The electron boundary is driven at frequencies $\omega_0$ and $2\omega_0$ , because both the transverse and the longitudinal component of the electron velocity contribute to the motion of the boundary. It follows that in this case both even and odd harmonics with polarization are generated.
- _s-polarized light_: The electric field is parallel to the plasma—vacuum interface. The electrons move in a plane perpendicular to the plane of incidence. In this configuration only the longitudinal component contributes, while the transverse component of the electron motion is ineffective. The normal motion of the mirror is driven at one frequency only, $\omega_m = 2\omega_0$ . It follows that the reflected light is composed of s-polarized odd harmonics. There are no s-polarized even harmonics.

#### Spectral Intensity Distribution

1. For a s-polarized fundamental wave we have. $\omega_m = 2 \omega_0$

   $$
   S((2n+1)\omega_0) = (\pi E_0)^2\left(\frac{J_n((n+1)\xi)}{(n+1)}- \frac{J_{n+1}(n\xi)}{(n)}\right)^2
   $$

2. For a p-polarized fundamental wave we have. $\omega_m = \omega_0$ and $\omega_m = 2 \omega_0$
   $$
    S(n\omega_0) = (\pi E_0)^2\left(\frac{J_{n-1}(\frac{1}{2}(n+1)\xi)}{\frac{1}{2}(n+1)}- \frac{J_{n+1}\frac{1}{2}((n-1)\xi)}{\frac{1}{2}(n-1)}\right)^2
   $$

We see that the spectrum depends only on $\xi$ where $\xi =( 2\omega_0s_0/c)\cos\theta$. The amplitude $s_0$ is bounded so that the velocity deos not exceed speed of light, that is $s_0<c/\omega_m$. For s-polarization, as $\omega_ = 2\omega_0$, we have $\xi < \cos \theta$. Further, for normal incident $\xi>1$.

[High-order optical harmonic generation from solid surfaces](https://www.researchgate.net/publication/227076835_High-order_optical_harmonic_generation_from_solid_surfaces)

## Universal Spectra

### Ideal mirror is not possible

The 'ideal mirror' boundary condition implies zero tangential components of the vector potential at the mirror surface. As a consequence, when the ideal mirror moves with $\gamma >>1$ toward a laser pulse with the electric field $E_l$ and duration $\tau$, then the reflected pulse acquires the electric field $E_{refl} \propto \gamma^2 E_l$ and the duration $\tau_{refl} \propto \tau\gamma^2$ . Consequently, the energy of the reflected pulse must be $\gamma^2$ times higher than that of the incident one. However, as the plasma surface is driven by the same laser pulse, this scaling is energetically prohibited, and the plasma cannot serve as an 'ideal mirror.' Indeed, the ideal mirror must support a surface current $J_m \propto (eN_c \gamma ac^2/ \omega)$ growing with the $\gamma$ factor. A realistic plasma surface does not provide such a current and the boundary condition must be changed.

### Solution

The boundary condition gives:

$$
E_r \left[t', X(t') \right] = -E_i \left[t', X(t') \right]
$$

Where

$$
t = t' - X(t')
$$

is the retardation relation

No assumaption about the form of $X(t)$ is made. apart from it being a periodic function. They used the method of steepest descent to find the solution. This gave the cutoff.

### The Power Law and Decay

The power is

$$
I_n \propto 1/n^{5/2}
$$

for monochromatic wave and

$$
I_n \propto 1/n^{3}
$$

for broadband wave.

While the cutoff is:

$$
n_c \propto 4\gamma_{\max}^2
$$

[Relativistic Doppler Effect: Universal Spectra and Zeptosecond Pulses](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.93.115002)

## Doppler Shift Due to Moving Mirror

The change in frequency follows:

$$
f = f_0 \frac{1-2\frac{v}{c}\cos \alpha + \frac{v^2}{c^2}}{1 - \frac{v^2}{c^2}}
$$

where $\alpha$ is the angle made by the incident light. This transforms to the usual frequency shift for normal incident when $\alpha = 0$.

[The Doppler effect from a uniformly moving mirror](https://arxiv.org/pdf/physics/0409014.pdf)

## Naive Moving Mirror Model

It is reasonable to assume that there is no significant absorption in the target and that the reflection of the pulse is perfect. Such assumption is equivalent to treating the oscillating surface as the surface of a perfect conductor and to adopting the corresponding boundary conditions in Maxwell equations.

The motion of the surface corresponds to the motion of the electrons in the layer in the direction perpendicular to the surface. Thus this motion combines the effects of the Lorentz force, the relativistic mass correction, and the re- storing force in the x direction owing to plasma oscillations. Equations of motion for the mirror then read:

$$
\frac{d\mathbf{p}}{dt}
 = q\mathbf{E}+\frac{q}{c}\mathbf{v}\times \mathbf{B} - m\omega_p^2x
$$

We define $\mathbf{u} = \gamma \mathbf{v}$. The non vanishing part of the above equations are:

$$
\begin{align*}
\frac{du_x}{dt} &= \frac{q}{\gamma mc}u_yB_z(x,t) - \omega_p^2x\\
\frac{du_y}{dt} &= \frac{q}{m}E_y(x, t) -\frac{q}{\gamma mc}u_xB_z(x,t)\\
\end{align*}
$$

In the moving-mirror model we consider that all electrons move with exactly the same velocity and that all started from $s_x=0$. Therefore they constitute a plane that is oscillating according to the Lorentz and plasma forces. It is the moving mirror. The reflected field $E_R$ may be obtained from the requirement of vanishing of the total electric field at the electron surface $s_x(t)$,

$$
E_R[t-s_x(t)/c] + E_0 \cos[\omega_L(t + s_x(t)/c)] = 0
$$

[Generation of attosecond pulse trains during the reflection of a very intense laser on a solid surface](https://opg.optica.org/josab/fulltext.cfm?uri=josab-15-7-1904&id=35491)
