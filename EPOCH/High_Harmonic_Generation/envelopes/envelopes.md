# Envelopes

The envelopes tried are:

## Guassian

$$
    P(t)=
    \begin{cases}
         & e^{\frac{-(t-T/2)^2}{2(0.2T)^2}} \text{ for } 0 \leq t \le T \\
         & 0         \;      \text{ otherwise }
    \end{cases}
$$

## Sine Squared

$$
    P(t)=
    \begin{cases}
         & \sin^2(\pi t/T) \text{ for } 0 \leq t \le T \\
         & 0         \;      \text{ otherwise }
    \end{cases}
$$

## Traingular

$$
    P(t)= 2\times
    \begin{cases}
         & t/T \text{ for } 0 \leq t \le T/2 \\
         & 1-t/T \text{ for } T/2 \leq t \le T \\
         & 0         \;      \text{ otherwise }
    \end{cases}
$$

Other parameters which are a constant are:

`a0 =  0.5`

`factor =  4`

`nx =  16000`
