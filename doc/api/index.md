```{eval-rst}
.. currentmodule:: crowsetta
```

# API Reference

This section documents the 
[API](https://en.wikipedia.org/wiki/API)
of crowsetta.

(api-core)=

# Core

This section documents the core API of crowsetta, 
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

## Example data

```{eval-rst}
.. autosummary::
   :toctree: generated
   
   crowsetta.example   
   crowsetta.examples.show
```

(api-formats)=

# Formats

This section documents the API of the :mod:`crowsetta.formats` module.
It is generated automatically. 
If you are a crowsetta user looking for 
more detail about the built-in formats,
please see: {ref}`formats-index`.

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   :recursive:

   crowsetta.formats
   crowsetta.formats.bbox
   crowsetta.formats.seq
```

(api-interface)=

# Interface

The section documents the API of the :mod:`crowsetta.interface` module.

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: module.rst
   :recursive:

   crowsetta.interface
```

## Base

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst

   crowsetta.interface.base.BaseFormat
```

## Sequence-Like

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst

   crowsetta.interface.seq.SeqLike
```

## Bounding Box-Like

```{eval-rst}
.. autosummary::
   :toctree: generated
   :template: class.rst

   crowsetta.interface.bbox.BBoxLike
```
