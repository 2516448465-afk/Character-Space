"""Build a single-page HTML report from the collocate CSVs in output/.

Reads the three collocate CSVs, embeds each as a table in
output/results.html, and adds a dropdown to switch between runs.
"""

import string

import pandas as pd

RUNS = [
    ("window_h5", "window, horizon = 5", "output/collocates_woland_window_h5.csv"),
    ("window_h10", "window, horizon = 10", "output/collocates_woland_window_h10.csv"),
    ("sentence", "sentence", "output/collocates_woland_sentence.csv"),
]
OUTPUT_PATH = "output/results.html"

PAGE = string.Template("""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>Collocates of 沃兰德</title>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; margin: 2rem; color: #222; }
  header { display: flex; align-items: baseline; gap: 1.5rem; flex-wrap: wrap; }
  h1 { font-size: 1.4rem; margin: 0; }
  label { font-size: 1rem; color: #444; }
  select { font-size: 1rem; padding: .3rem .5rem; }
  h2 { font-size: 1.1rem; margin: 1.2rem 0 .6rem; }
  .count { font-weight: normal; color: #666; font-size: .9rem; margin-left: .5rem; }
  table.collocates { border-collapse: collapse; font-size: .95rem; }
  th, td { padding: .25rem .6rem; text-align: left; }
  thead th { position: sticky; top: 0; background: #f0f0f0; border-bottom: 2px solid #999; }
  th:nth-child(n+3), td:nth-child(n+3) { text-align: right; font-variant-numeric: tabular-nums; }
  tbody tr:nth-child(even) { background: #fafafa; }
  .empty { color: #666; font-style: italic; }
</style>
</head>
<body>
<header>
  <h1>Collocates of 沃兰德</h1>
  <label for="picker">Run:</label>
  <select id="picker">$options</select>
</header>
<main>
$sections
</main>
<script>
  const picker = document.getElementById("picker");
  function show() {
    document.querySelectorAll("section.run").forEach(s => {
      s.hidden = s.id !== picker.value;
    });
  }
  picker.addEventListener("change", show);
  show();
</script>
</body>
</html>
""")


def render_table(df: pd.DataFrame) -> str:
    if df.empty:
        return '<p class="empty">No collocates passed the filters.</p>'
    return df.to_html(
        index=False,
        border=0,
        classes=["collocates"],
        formatters={
            "exp_local": lambda v: f"{v:.2f}",
            "ratio_local": lambda v: f"{v:.2f}",
            "p_value": lambda v: f"{v:.2e}",
        },
    )


def main() -> None:
    options = []
    sections = []
    for run_id, label, path in RUNS:
        df = pd.read_csv(path)
        options.append(f'<option value="{run_id}">{label}</option>')
        sections.append(
            f'<section id="{run_id}" class="run" hidden>\n'
            f"  <h2>{label}<span class=\"count\">{len(df)} collocates</span></h2>\n"
            f"  {render_table(df)}\n"
            f"</section>"
        )
    html = PAGE.substitute(
        options="\n".join(options),
        sections="\n".join(sections),
    )
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"done: wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
