---
title: 'pyfebio: A Python Application Programming Interface for FEBio'
tags:
  - Python
  - finite element analysis
  - biomechanics
authors:
  - name: Scott C. Sibole
    orcid: 0000-0003-2260-8167
    corresponding: true
    affiliation: 1
  - name: Steve A. Maas
    affiliation: "2,3"
  - name: Michael R. Herron
    affiliation: "2,3"
  - name: Jason P. Halloran
    affiliation: 1

affiliations:
 - name: Applied Sciences Laboratory, Washington State University, United States
   index: 1
 - name: Department of Biomedical Engineering, University of Utah, United States
   index: 2
 - name: Scientific Computing and Imaging Institute, University of Utah, United States
   index: 3
date: 7 January 2026
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

`pyfebio` is a Python package supporting programmatic generation of FEBio model definition files. Beyond enabling scripted modeling workflows, belonging to
the wider Python ecosystem provides seamless integration with many packages for scientific computing, data science and visualization, machine learning, *etc*.
Furthermore, modeling and simulation workflows often require iterations of simulations with changing parameters each with post-processing of results.
With scripted workflows, these iterations are not only automated but also have inherent provenance tracking, which enables reproducibility and repeatability
of the analyses.

# Statement of Need

Finite element models are often generated through a graphical user interface with point-and-click operations, which can be tedious, time-consuming, and error-prone. 
Programmatic generation of FEBio models allows for more efficient, verifiable, and scalable modeling workflows. The Python language has become highly popular
in scientific computing, data science, and machine learning with many libraries supporting these disciplines. Integration of `pyfebio` with the rich Python software 
ecosystem allows for the creation of powerful workflows and applications utilizing FEA with FEBio.

# State of the Field 

Similar projects to `pyfebio` include:

- `febio-python` 
- `interFEBio`
- `waffleiron`
- `FEPyio`

  +--------------------+----------------+--------------+--------------+----------+-----------+
  |                    | febio-python   | interFEBio   | waffleiron   | FEPyio   | pyfebio   |
  +:==================:+:==============:+:============:+:============:+:========:+:=========:+
  | Runtime Validation | No             | No           | No           | No       | Yes       |
  +--------------------+----------------+--------------+--------------+----------+-----------+
  | XPLT Handling      | In-memory      | In-memory    | In-memory    | No       | HDF5      | 
  +--------------------+----------------+--------------+--------------+----------+-----------+
  | Documentation      | Extensive      | Broken Link  | Planned      | No       | Extensive | 
  +--------------------+----------------+--------------+--------------+----------+-----------+
  | Type Annotation    | Yes            | Yes          | No           | Yes      | Yes       |
  +--------------------+----------------+--------------+--------------+----------+-----------+
  | Component Creation | Abstract       | Abstract     | Abstract     | Abstract | Concrete  |
  +--------------------+----------------+--------------+--------------+----------+-----------+
  | Legacy Support     | Yes            | No           | Yes          | No       | No        |
  +--------------------+----------------+--------------+--------------+----------+-----------+

The major difference between `pyfebio` and these similar packages is the concrete definition and validation of all components.
While an abstracted definition allows for flexibility and a smaller codebase, it often shifts the responsibility of ensuring validity 
to the user. With concrete definitions, we can also constrain attributes with much more granularity. Furthermore, this approach
makes the codebase simple and easy to extend.

# Software Design

An FEBio model is encoded in the Extensible Markup Language (XML), which adopts a tree structure with a root element
and nested sub-elements. While long-established packages such as `ElementTree` and `lxml` exist for XML parsing and definition,
a specialized package with predefined XML elements for FEBio model components was desired. To this end, `pyfebio` leverages the
`pydantic-xml` package [@pydantic_xml] that extends the popular runtime static type checking library, `pydantic` [@Colvin_Pydantic_Validation_2025],
for validated XML (de)serialization. In addition to type validation, this approach also allows for the enforcement of custom constraints
on model values when appropriate e.g. an elastic modulus must be positive. When possible, default values are assigned to class attributes 
to reduce the amount of code required when defining an FEBio model.

Discretization of model geometry, referred to as meshing, is a challenging task for which numerous software applications exist. These, in turn, often have
custom file formats. To handle translation, of these formats the `meshio` package is utilized. Meshes defined in various formats are first translated into
a `meshio.Mesh` object and then `pyfebio` can translate this object into an FEBio mesh. This also allows for the usage of higher-order elements.

FEBio results are saved in a custom binary format called `XPLT`. Workflows typically need to access and post-process simulation results. To this end, `pyfebio` supports translation 
to the popular `HDF5` format. After conversion, `HDF5` packages such as`h5py` can be used for data analysis and management. `HDF5` also supports lazy loading such that only accessed
data is loaded into memory. This enables handling of large datasets that may not fit into memory.

# Research Impact

`pyfebio` has been used extensively in internal modeling workflows with publications forthcoming. Collaborators in the National Institutes of Health funded `KneeHub` project [@Rooks2021]
have been made aware of the public repository. Furthermore, by hosting `pyfebio` on the `febiosoftware` GitHub organization, visibility and awareness of the project in the FEBio user community should be increased.

# AI usage disclosure

Code prediction provided by the `Zeta` model implemented in the `Zed` integrated development environment software was used occasionally during development. Large Language Model prompting was not employed.

# Acknowledgements

This project was supported with funding from NIH-NIBIB R01EB024573.

# References
