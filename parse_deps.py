import json
import os
import re

deps = set()
for file in os.listdir("notebooks"):
    if file.endswith(".ipynb"):
        with open(os.path.join("notebooks", file), "r") as f:
            nb = json.load(f)
            for cell in nb.get("cells", []):
                if cell["cell_type"] == "code":
                    source = "".join(cell.get("source", []))
                    for line in source.split("\n"):
                        if "pip install" in line:
                            # Extract everything after "pip install"
                            parts = line.split("pip install")
                            if len(parts) > 1:
                                reqs = parts[1].split()
                                for r in reqs:
                                    if r.startswith("-") or r == "install": continue
                                    # Strip quotes and commas
                                    r = r.replace('"', '').replace("'", "").replace(",", "")
                                    if "git+" not in r and r:
                                        deps.add(r)
                                    if "unsloth" in r:
                                        deps.add("unsloth")

print("\n".join(sorted(list(deps))))
