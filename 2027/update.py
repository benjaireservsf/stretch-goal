#!/usr/bin/env python3
"""Update the 2027 goal boards.
Usage: python3 update.py 2027-01-29 install=125000 service=40000 maintenance=22000 duct=9000
  - first argument is the date the totals are as of (end of that working day)
  - the four numbers are year-to-date revenue for each department
Writes data.json and refreshes the baked copy inside index.html, appends to history (replacing any entry for the same date)."""
import json, re, sys, time, os
here = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3:
    sys.exit(__doc__)
as_of = sys.argv[1]
vals = dict(a.split("=") for a in sys.argv[2:])
keys = ["install", "service", "maintenance", "duct"]
d = json.load(open(os.path.join(here, "data.json")))
cur = {k: float(vals[k].replace(",", "").replace("$", "")) if k in vals else d["ytd"][k] for k in keys}
cur = {k: int(round(v)) for k, v in cur.items()}
d["ytd"] = cur
d["asOf"] = as_of
d["updatedAt"] = int(time.time() * 1000)
d["history"] = [h for h in d["history"] if h["asOf"] != as_of] + [dict(asOf=as_of, **cur)]
d["history"].sort(key=lambda h: h["asOf"])
j = json.dumps(d, separators=(",", ":"))
open(os.path.join(here, "data.json"), "w").write(j)
p = os.path.join(here, "index.html")
s = open(p).read()
s2 = re.sub(r'(<script type="application/json" id="baked">)(.*?)(</script>)', lambda m: m.group(1) + j + m.group(3), s, count=1, flags=re.S)
assert s2 != s or j in s
open(p, "w").write(s2)
print("company total:", sum(cur.values()), cur, "as of", as_of)
