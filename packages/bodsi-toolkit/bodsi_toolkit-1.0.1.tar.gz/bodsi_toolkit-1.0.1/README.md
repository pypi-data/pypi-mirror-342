# Dynamic Systems Identification (Polynomial Models)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

## Description:   

The Bi-Objective Dynamic Systems Identification (BODSI) class offers a robust framework for identifying dynamic systems modeled by Polynomial NARX structures. It adopts a bi-objective parameter estimation technique where the first equation minimizes the dynamic error, and the second equation ensures precise static curve fitting. 
The BODSI_TOOKIT class includes functionalities for generating candidate terms, identifying clusters, constructing dynamic and static matrices, and parameter mapping, in addition to advanced decision-making tools based on model correlation. This ensures unbiased parameter estimation and allows users to visualize static models, validate dynamic performance, and select optimal solutions for their specific needs.

For further details on the minimal correlation criterion and its use in multi-objective parameter estimation, refer to:   
[1] Márcio F.S. Barroso, Ricardo H.C. Takahashi, Luis A. Aguirre, "Multi-objective parameter estimation via minimal correlation criterion," Journal of Process Control, Volume 17, Issue 4, 2007, Pages 321-332, ISSN 0959-1524. 
https://doi.org/10.1016/j.jprocont.2006.10.005

Cite As
Márcio F. S. Barroso, Eduardo M. A. M. Mendes and Jim Jones S. Marciano. Bi-Objective Dynamic Systems Identification (BODSI class) (https://www.mathworks.com/matlabcentral/fileexchange/180331), MATLAB Central File Exchange. Retrieved March 8, 2025.

## Installation
To install the package, use:
```sh
pip install bodsi_toolkit
