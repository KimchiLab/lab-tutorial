# repository_project_title
This is a demo repository for lab tutorials

## Licensing and Use

### License
This reposiotry is licenced under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), an Attribution-NonCommercial-ShareAlike 4.0 International license. 

### Contributors
- Jane Doe (primary/first)
- Eyal Kimchi (Principle Investigator)
- Jenna Shin (as of 08/20/2026)

#### Contact Information
For any questions concerning this repository please contact:\
Eyal Y Kimchi, MD PHD\
Email: eyal.kimchi@northwestern.edu | [Website](https://kimchilab.org/)

## Project Description
### Objective

### Hypotheses
(Possible link to pre-registration)

### Methods
(protocols, sampling, instruments, coverage, etc.)

### Data
(Range of years over which data was collected, location, size, quality assurance metrics, missing data, etc)

### Results Overview
(Basic results tables and key context to understand the figures)

### File Structure Overview
(File layers, naming convections, etc.)

## Evironment Configuration

### Prerequisite Programs
- [Git v2.46+](https://git-scm.com/downloads)
- [Python3 v3.12.6+](https://www.python.org/downloads/)
- [Anaconda Distribution  v3.12.4 or Minicondav24.7.1](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#)
- [R v3.6.0+ and R Studio v2024.04.2+](https://posit.co/download/rstudio-desktop/)

### Repository Cloning
To clone the repository to your local machine, paste the following in the command line:
   ```sh
   git clone https://github.com/kimchilab/<example>.git
   ```

### Environment Install
Both Python and R environment files are stored as .yaml files at the top level of the repository. To configure both environments, make sure that you have a conda package installed and run the corresponding lines from the top directory


#### To create the environment:
Python:
```sh
    conda env create -f <env_name_py>.yml
```

R:
```sh
    conda env create -f <env_name_py>.yml
```

#### To activate and use the environment:
Python:
```sh
    conda activate <env_name_py>
```
R:
```sh
    conda activate <env_name_py>
```

### R Project Evironment
To populate the correct file paths and dependencies, please open ```<example>.Rproj``` before running any of the scripts for analysis in RStudio

## Detailed File Structure

### /Data
All relevant data is stored in the /Data folder off of the repository path. 

| Filename | Description | Functions Called By |
| --- | --- | --- |
|VideoMetaData.csv| Detail all column meanings and units of measurement | What analyses are dependent on this file? |
|features_data.csv| --- | --- |

### /Scripts
| Filename | Description | Prerequisite Files | Outputs |
| --- | --- | --- | --- |
|LMEM_Delirium_Analysis.R  | --- | --- | --- |

### /Results
Insert Description Here

| Filename | Description | Analysis of Origin |
| --- | --- | --- |
|Behavioral_bootstrapping_results.csv | Include description of tabular columns | --- |
|LmemResults-Comprehensive-StratifiedDeliriumStatus.txt | --- | --- |


### /Figures
Define figure descriptions/captions
