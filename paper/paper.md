---
title: 'pyfebio: A Python Application Programming Interface for FEBio'
tags:
  - Python
  - finite element analysis
  - biomechanics
authors:
  - name: Scott C. Sibole
    orcid: 0000-0000-0000-0000
    corresponding: true
    affiliation: 1
  - name: Jason P. Halloran
    affiliation: 1
  - name: Steve A. Maas
    affiliation: "2,3"
  - name: Michael R. Herron
    affiliation: "2,3"

affiliations:
 - name: Applied Sciences Laboratory, Washington State University, United States
   index: 1
 - name: Department of Biomedical Engineering, University of Utah, United States
   index: 2
 - name: Scientific Computing and Imaging Institute, University of Utah, United States
   index: 3
date: 10 November 2025
bibliography: paper.bib
---

# Summary

The finite element method is a popular numerical technique for solving the partial differential equations that describe physical phenomena.
Its application, referred to as finite element analysis (FEA), has seen ubiquitous adoption across engineering and the natural sciences.
While many general-purpose FEA software packages exist, it is commonly necessary to extend their functionality for a particular application through
custom extensions or plugins often written by the user or research community. In biomedical fields particularly, one encounters the need for highly
specialized models of biological tissue material behavior, growth mechanics, multiphasic physics, active force production, and other complex
phenomena. Addressing these challenges was the motivation for the development of the FEBio (Finite Elements for Biomechanics) open-source
software nearly two decades ago [@Maas:2012]. FEBio has been widely adopted in the biomedical community [TODO: add some stats here]

`pyfebio` is a Python package enabling programmatic generation of FEBio model definition files. The Python ecosystem provides a rich set of tools for scientific computing,
data science and engineering, machine learning, and visualization.

# Statement of Need


# Methods

An FEBio model is encoded in the Extensible Markup Language (XML), which adopts a tree structure with a root element
and nested sub-elements. While long-established packages such as `ElementTree` and `lxml` exist for XML parsing and definition,
a specialized package with predefined XML elements for FEBio model components was desired. To this end, `pyfebio` leverages the
`pydantic-xml` package [@pydantic_xml] that extends the popular runtime static type checking library, `pydantic` [@Colvin_Pydantic_Validation_2025],
for validated XML (de)serialization. In addition to type validation, this approach also allows the enforcement of custom constraints
on model values when appropriate. When possible, default values are assigned to class attributes to reduce the amount of code required
when defining an FEBio model.

A small dependency set was utilized in `pyfebio` to minimize conflicts when integrating with the wider Python ecosytem, which contains a wealth of packages for scientific computing and numerical analysis.

# Acknowledgements

# References
