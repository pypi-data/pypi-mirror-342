# Jabs Mimir

**Jabs Mimir** is a lightweight, extensible UI micro-framework built on top of `tkinter` and `ttkbootstrap`, designed for rapid internal tool development and structured form workflows.

It provides:

- Reusable UI primitives with validation and tooltips
- Support for block-based form components with dynamic variable binding
- Integration with custom validation logic (via resolver, file loader, or direct function)
- Modular architecture suitable for internal tooling and small boilerplate projects

---

## Installation

```bash
pip install jabs-mimir
```

---

## Quick Start

```python
from jabs_mimir import Mimir, DataBlockWrapper, UtilityModule
import tkinter as tk
import ttkbootstrap as tb

class App(tb.Window):
    def __init__(self):
        super().__init__(title="Mimir Demo")
        self.ui = Mimir(self)

        # Option 1: Inline validator resolver (string-based)
        self.ui.setValidatorResolver(lambda name: {
            "not_empty": lambda val: bool(str(val).strip())
        }.get(name))

        # Option 2 (alternative): load from file
        # self.ui.setValidatorFile("include/validator.py")

        self.ui.switchView(self.mainView)

    def mainView(self, ui, *args):
        frame = tb.Frame(self)
        fields = [
            {"type": "heading", "label": "Basic Info"},
            {"label": "Name", "key": "name", "variable": tk.StringVar(), "validation": "not_empty"},
            {"label": "Age", "key": "age", "variable": tk.IntVar()}
        ]

        meta = UtilityModule.buildBlockMeta(fields)
        block = DataBlockWrapper(meta)

        ui.renderFields(frame, fields)
        ui.addNextButton(frame, row=len(fields)+1, viewFunc=self.mainView)

        return frame

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## Validation

Jabs Mimir supports **both automatic and manual validation**, triggered on field focus-out and verified again when clicking "Next".

### You can define validation in two ways:

#### 1. **String-based validation (via file or resolver)**

**Define a validator in a file**:
```python
# include/validator.py
def not_empty(value):
    return bool(str(value).strip())
```

**Load it**:
```python
self.ui.setValidatorFile("include/validator.py")
```

**Use string key in field**:
```python
{"label": "Name", "variable": tk.StringVar(), "validation": "not_empty"}
```

#### 2. **Direct function reference**

```python
from include.validator import not_empty

fields = [
    {"label": "Name", "variable": tk.StringVar(), "validation": not_empty}
]
```

Both methods are fully supported and interchangeable.

Mimir automatically:
- Binds validation on focus-out
- Stores all validators internally
- Re-validates all fields when clicking "Next"
- Blocks navigation if any invalid inputs remain
- Highlights invalid fields with red styling

Works even for readonly fields (like file upload paths), which normally can't be focused.

---

## Buttons & Navigation

Mimir provides helpers for both view transitions and general-purpose action buttons.

### `addNextButton(...)`
Use this when you want a button that:
- Runs validation on all fields
- Automatically switches to a new view
- Looks like a "next step" button

```python
self.ui.addNextButton(parent, row=5, viewFunc=initERPInput, label="Next")
```

### `addButton(...)`
Use this when you want full control over what happens on click.
- Can be used with or without validation (`validate=True` or `False`)
- Perfect for "Save", "Preview", or conditional logic buttons

```python
self.ui.addButton(parent, row=6, command=self.doSomething, label="Save", validate=True)
```

If you just want to go to the next frame **with validation**, use `addNextButton`. If you want to run custom logic (e.g. saving data, previewing content, or optionally switching views), use `addButton` instead.

---

## Working with Blocks

Mimir makes it easy to group inputs into reusable, structured blocks of fields (also called *Data Blocks*). These blocks:

- Are defined using a list of field dictionaries
- Can be rendered vertically or horizontally
- Are assigned metadata for identification (`store_id`, `custom_label`, etc.)
- Can be validated, modified, and repeated dynamically
- Wrap all data in a `DataBlockWrapper`

### Creating a Field Block

```python
fields = [
    {"type": "heading", "label": "Store 1"},
    {"label": "Cash", "key": "cash", "variable": tk.DoubleVar()},
    {"label": "Card", "key": "card", "variable": tk.DoubleVar()}
]

meta = UtilityModule.buildBlockMeta(fields, store_id=1)
block = DataBlockWrapper(meta)
```

### Rendering a Block in the UI

```python
self.blocks = []

self.ui.renderBlockUI(
    container=frame,
    fields=fields,
    blockList=self.blocks,
    layout="vertical",
    label="Store 1",
    meta={"store_id": 1}
)
```

This will create a labeled block frame (with remove button), populate it with your fields, and store the block object in `self.blocks`.

### Accessing Block Data

You can easily access or print values from any block:

```python
for block in self.blocks:
    print("Cash:", block.get("cash").get())
    print("Card:", block.get("card").get())
```

You can also loop through and validate them with:

```python
valid_blocks = [b for b in self.blocks if UtilityModule.isBlockValid(b)]
```

### Repeating Dynamic Blocks

Use `renderBlockUI()` repeatedly to dynamically add multiple blocks (e.g., one per store or user):

```python
for i in range(5):
    self.ui.renderBlockUI(
        container=frame,
        fields=fields,
        blockList=self.blocks,
        label=f"Store {i+1}",
        meta={"store_id": i+1}
    )
```

---

## Components

### `Mimir`
Manages UI views, tooltips, validation, field rendering, and form logic.
Supports reusable custom field types via `registerFieldType()`.

### `DataBlockWrapper`
A wrapper for block-level form metadata and values. Supports dot-access and `.get()`/`.set()` calls.

### `UtilityModule`
Helper methods for building field metadata, extracting values, validating blocks, and block meta handling.

---

## License
MIT License © 2025 William Lydahl
