---
title: 'pyfebio: A Python Application Programming Interface for FEBio'
tags:
  - Python
  - finite element analysis
  - biomechanics
authors:
  - name: Scott C. Sibole
    orcid: 0000-0000-0000-0000
    equal-contrib: true
    corresponding: true
    affiliation: 1
  - name: Jason Halloran
    equal-contrib: false
    affiliation: 1
  - name: Steve Maas
    equal-contrib: false
    affiliation: "2,3"
  - name: Michael Ross Herron
    equal-contrib: false
    affiliation: "2,3"

affiliations:
 - name: Applied Sciences Laboratory, Washington State University, United States
   index: 1
 - name: Muscoskeletal Research Laboratory, University of Utah, United States
   index: 2
 - name: Scientific Computing and Imaging Institute, University of Utah, United States
   index: 3
date: 10 November 2025
bibliography: paper.bib
---

# Summary

The finite element method is a popular numerical technique for solving the partial differential equations that describe physical phenomena.
Its application, referred to as finite element analysis (FEA), has seen ubiquitous adoption across engineering and physics. While many general-purpose FEA software
packages exist, it is a commonly necessary to extend their functionality for a particular application through custom extensions or plugins often written by the user
or research community. In biomedical fields, one encounters the need for highly specialized models of biological tissue material behavior, growth mechanics,
multiphasic physics, active force production, and other complex phenomena. Addressing these challenges was the motivation for the development of the
FEBio (Finite Elements for Biomechanics) open-source software nearly two decades ago `[@Mass:2012]`.



# Statement of Need

The Python ecosytem provides a wealth of packages for scientifc computing.

The pyfebio package provides a Python interface for the FEBio finite element analysis software. This package allows users to define FEBio XML model definition files with the Python programming language. Model components are classes that inherit from the pydantic-xml
BaseXMLModel. This provides the runtime static type checking of the pydantic library, ensuring that the XML model definition files are valid and well-formed. When possible, components have default values, minimizing the amount of code required to define a model.

Possible applications include automated modelling and simulation pipelines, inverse finite element analysis, sensitity analysis, mesh convergence studies, and others.

# Acknowledgements

# References
