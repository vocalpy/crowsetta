(api-core)=

# Core

This page documents the core API of crowsetta, 
including data types, other classes, and modules.

## Data types

### Annotation

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst
   
   crowsetta.Annotation   
```

### Sequence

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst
   
   crowsetta.Sequence   
```

### Segment

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst
   
   crowsetta.Segment   
```

### BBox

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst
   
   crowsetta.BBox   
```

## Classes

### Transcriber

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst
   
   crowsetta.Transcriber   
```

## Modules

### `crowsetta.data`

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   :recursive:

   crowsetta.data.data
```

```{note}
Modules in `crowsetta.data` besides `crowsetta.data.data` 
contain example data files and a citation,
e.g., `crowsetta.data.birdsongrec` contains an example 
file `Annotation.xml` and `citation.txt`.
For that reason just `crowsetta.data.data` is shown.
```

### `crowsetta.interface`

For complete documentation of the interface, 
please see {ref}`this page <api-interface>`.

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   
   crowsetta.interface   
```


### typing

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   :recursive:

   crowsetta.typing   
```


### validation

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   :recursive:

   crowsetta.validation   
```

## Decorators

### `crowsetta.register_format`

```{eval-rst}
.. autosummary::
   :toctree: generated
   
   crowsetta.register_format   
```
