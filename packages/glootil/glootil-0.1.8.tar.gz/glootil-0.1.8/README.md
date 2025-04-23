# Glootil

A Python 3 library to create [gloodata](https://gloodata.com) extensions.

## Usage

```sh
mkdir my-gd-ext
cd my-gd-ext
uv init
uv add glootil uvicorn fastapi
```

edit `main.py` to contain:

```python
from datetime import datetime
from enum import Enum

from glootil import Toolbox

tb = Toolbox("my-gd-ext", "My Extension", "My Utility Tools")


@tb.enum(icon="visible")
class DisplayFormat(Enum):
    LINE = "Line"
    TABLE = "Table"
    TEXT = "Text"


@tb.tool(
    name="Compound Interest Rate Calculator",
    ui_prefix="Compound Interest Rate",
    args={
        "principal": "Principal",
        "interest_rate": "Interest Rate",
        "years": "Years",
        "display_format": "Format",
    },
    examples=[
        "calculate compound interest for initial 1500 dollars, 2.5% interests for 8 years in line chart",
        "compound interst for $2000 at 3.5% interests for 10 years as a table",
    ],
)
def compound_interest_calculator(
    principal: float = 1.0,
    interest_rate: float = 3.0,
    years: int = 5,
    display_format: DisplayFormat = DisplayFormat.LINE,
):
    year = datetime.now().year
    amount = principal
    cols = [("year", "Year"), ("amount", "Amount"), ("interest", "Interest")]
    rows = []

    for i in range(0, years + 1):
        interest = amount * (interest_rate / 100)
        rows.append((year + i, amount, interest))
        amount += interest

    if display_format == DisplayFormat.TABLE:
        return {
            "type": "Table",
            "columns": cols,
            "rows": rows,
        }
    elif display_format == DisplayFormat.TEXT:
        lines = [
            f"- {year}: ${amount} (${interest} interests)"
            for (year, amount, interest) in rows
        ]
        return "\n".join(lines)
    else:
        return {
            "type": "Series",
            "title": "Compound Interest by Year",
            "xColTitle": "Year",
            "yColTitle": "$",
            "xCol": "year",
            "valCols": ["amount", "interest"],
            "cols": cols,
            "rows": rows,
        }


tb.serve(host="127.0.0.1", port=8087)
```

Start:

```sh
uv run main.py
```

On gloodata write in the prompt bar:

> Add extension Fincance at port 8087

Click `Test` and then `Save`

Now in the prompt bar write something like:

> calculate compound interest for initial 2500 dollars, 3.5% interests for 15 years

Check the [examples](https://github.com/gloodata/glootil-py/tree/main/examples) folder for more.

## License

MIT, see LICENSE file for details
