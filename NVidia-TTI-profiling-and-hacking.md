## Deep dive into performance benchmarking and optimization
-----------------------------------------------------------

### Outline
-----------

The operator used in this training session is based on simplfications of the
systems presented in:
*Self-adjoint, energy-conserving second-order pseudoacoustic systems for VTI and TTI media for reverse migration and full-waveform inversion*
_(2016) Kenneth Bube, John Washbourne, Raymond Ergas, and Tamas Nemeth SEG_
[Technical Program Expanded Abstracts](https://library.seg.org/doi/10.1190/segam2016-13878451.1)

In particular, we will use the TTI self-adjoint variable-density
forward-propagating operator:

* This is an excellent *use case from industry*, which represents the bulk of a
  wave solver close to what would be used in a production environment.
* We focus on the *stencil part of the propagator*, that is the loops and
  expressions that Devito generates given the finite-difference approximation
  of the TTI partial differential equations expressed in the DSL. 
* Severa simplifications made to remove what would be noise in this tutorial:
  * "Dummy" datasets (e.g., all material parameters initialized to constant
    values), but such that the simulation output remains finite;
  * No boundary conditions;
  * No host-device data streaming (by default);
  * No higher-order optimizations (by default) such as adapting boxes;
  * ...


### Login
---------

You will login to a VM in the Azure Cloud that has been pre-configured with all
the necessary to run the TTI demo on a GPU (either an NVidia V100 or A100).

To login:

```
ssh ...
```

To spawn the docker container from which you'll run the demo:

```
docker container run ... Dockerfile.nvidia.run.X ...
```

where either `X=acc` or `X=cuda`. The former will create a docker container
where Devito generates OpenACC code, while the latter targets CUDA.



### Run the TTI demo
--------------------

As easy as:

```
cd demos/tti_acoustic_self_adjoint/
python run.py -d 412 423 476 -tn 200
```

This will run a the TTI demo on a `412x423x476` grid for `200` timesteps. The
docker container from which you run has already set all the necessary
environment variables such that Devito generates and runs GPU code.

Some performance metrics, including GFlops/s and GPoints/s, will be emitted to
standard output when the simulation terminates. More info about the Devito
Operator performance available
[here](https://github.com/devitocodes/devito/wiki/FAQ#is-there-a-way-to-get-the-performance-of-an-operator).


### Hack the TTI demo
---------------------

The TTI demo tells you where the generated code is stashed. Run it, and you'll
see a message along the lines of:

```
Operator `TTISelfAdjointForward` jit-compiled
`/tmp/devito-jitcache-uid1002/a60cccac86fdd90c77b2d67c11268042ec93e014.cpp` in
2.95 s with `NvidiaCompiler`
```

You can edit the generated file and test your changes thanks to the "JIT
backdoor" -- a mechanism in Devito that allows users and developers to test
their own hacks directly without having to interfere with the Devito compiler.
So, make your edits, save the file, and re-run as:

```
DEVITO_JIT_BACKDOOR=1 python run.py -d 412 423 476 -tn 200
```

You may start, for example, by adding a `printf` prior to the time loop, just
to get familiar with this feature.

More on the JIT backdoor available
[here](https://github.com/devitocodes/devito/wiki/FAQ#can-i-manually-modify-the-c-code-generated-by-devito-and-test-these-modifications).


### On the CUDA backend
-----------------------

At the time of this training session, the CUDA backend in DevitoPRO is still in
its infancy. It will generate functioning code for the TTI demo, but
performance-wise it is still borked in all sort of ways. This makes it an
interesting starting point for a performance optimization exercise based on
profiling (NVidia NSight Compute) and manual hacking via the JIT backdoor.
