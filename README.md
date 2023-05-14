# High Harmonic Generation from Relativistic Plasma Mirrors

This is a repository contains code, note, articles and other resources related to the MSc. project titled _High Harmonic Generation from Relativistic Plasma Mirrors_.

> The repository is made of different materials in a one year period and during this, there have been a lot of changes. It is possible that some part of codes might not work properly, especially the older ones.

## Folder Structure

Here is a brief explanation of the folder structure:

### `Articles`

This contains articles and papers related to the project. The articles are mostly in PDF format and are further organized in different folders based on the topic.

### `EPOCH`

This is the main folder containing the _EPOCH_ simulation files. The folder is further organized in different folders and subfolders based on what type of simulations are performed. For example, the folder `EPOCH/High_Harmonic_Generation` has the simulations for HHG from plasma mirrors and its subfolders contain the simulations for the effect of various laser and plasma parameters on the HHG. `EPOCH/HPC` has files for the simulations done on HPC. These simulations were done in 2D.

### `Preliminaries`

This folder has materials related to some preliminary studies done. For example, `Preliminaries/Numerical_Methods` gives some basic idea about the numerical methods and their implementations while `Preliminaries/FDTD` has some very simple simulations done using FDTD method.

### `Presentations`

This is the second most important folder in this repo. The folder has `tex` codes for the four presentation and four reports created during the project. The subfolder `Presentations/PPTs` has the four presentations and `Presentations/Reports` has the four reports. This folder also has `Presentations/creating_images` which has some scripts used to generate images for the presentations and reports.

### `Reference Materials`

The folder has a few books and articles, as well as a few markdown notes created by us.

### `Tools`

This folder is a small module which has implementation of some numerical methods and other helper tools.

### `zpic`

This folder has the `zpic` code which is another PIC code. We worked with it a few month and found that it was not sufficient for our needs. So, we switched to _EPOCH_.
