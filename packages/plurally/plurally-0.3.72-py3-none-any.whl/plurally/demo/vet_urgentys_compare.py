import json
import shutil
from pathlib import Path

import diff_match_patch as dmp_module
import markdown2


def make_bullet(content):
    # Split the content into lines for easier manipulation
    lines = content.split("\n")

    # Iterate over the lines and add a blank line before list items as needed
    for i in range(1, len(lines)):
        if lines[i].startswith("-") and not lines[i - 1].startswith("-") and lines[i - 1].strip() != "":
            lines.insert(i, "")
            i += 1  # Skip the inserted blank line
    processed_content_corrected = "\n".join(lines)
    return processed_content_corrected


def generate_html_page_with_side_by_side_diff(runs_data, out_dir, old_version="old", new_version="new"):
    # Initialize the diff_match_patch object
    title = f"Vet Urgentys {old_version} -> {new_version}"
    dmp = dmp_module.diff_match_patch()

    # HTML template with side navigation
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .sidenav {{
                width: 250px;
                position: fixed;
                top: 0;
                left: 0;
                overflow-x: hidden;
                overflow-y: auto; /* Enable vertical scrolling */
                padding: 8px 0;
                max-height: 100vh; /* Set maximum height to the viewport height */
            }}
            .sidenav a {{
                padding: 6px 8px 6px 16px;
                text-decoration: none;
                color: #111;
                display: block;
            }}
            .sidenav a:hover {{ background-color: #ddd; }}
            .main {{ margin-left: 260px; padding: 0 10px; }}
            .tab {{ display: none; }}
            .tab-buttons button {{ padding: 10px 20px; border: 1px solid #ccc; cursor: pointer; }}
            .tab-buttons button.active {{ background-color: #007BFF; color: white; border: 1px solid #0056b3; }}
            .active {{ background-color: #ddd; }}
            .diff {{ white-space: pre-wrap; font-family: monospace; }}
            table {{ border: 1px solid #ccc; border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="sidenav">
            <h3>Runs</h3>
    """

    # Add side navigation items
    for index, run_data in enumerate(runs_data):
        html_content += f'<a href="javascript:void(0)" onclick="openRun(event, \'run{index}\')">{run_data["name"]}</a>'

    html_content += """
        </div>
        <div class="main">
            <h1 id="case-name">{title}</h1>
    """

    # Add content for each run
    for index, run_data in enumerate(runs_data):
        audio_file_path = run_data["audio_file_path"]
        markdown_new = run_data["markdown_new"]
        markdown_old = run_data["markdown_old"]
        # Compute the diff
        diffs = dmp.diff_main(markdown_old, markdown_new)
        dmp.diff_cleanupSemantic(diffs)
        html_diff = dmp.diff_prettyHtml(diffs)

        # Convert Markdown to HTML

        converter = markdown2.Markdown(extras=["tables"])  # <-- here
        html_new = converter.convert(make_bullet(markdown_new))
        html_old = converter.convert(make_bullet(markdown_old))

        html_content += f"""
            <div id="run{index}" class="tab">
                <audio controls>
                    <source src="{audio_file_path}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <div class="tab-buttons">
                    <button onclick="openTab(event, 'new_version_{index}')">{new_version}</button>
                    <button onclick="openTab(event, 'old_version_{index}')">{old_version}</button>
                    <button onclick="openTab(event, 'diff_version_{index}')">Diff</button>
                </div>
                <div id="new_version_{index}" class="tab">
                    <h2>{new_version}</h2>
                    <div>{html_new}</div>
                </div>
                <div id="old_version_{index}" class="tab">
                    <h2>{old_version}</h2>
                    <div>{html_old}</div>
                </div>
                <div id="diff_version_{index}" class="tab">
                    <h2>Diff</h2>
                    <div class="diff">{html_diff}</div>
                </div>
            </div>
        """

    html_content += """
            <script>
                function openRun(evt, runName) {
                    var i, tabcontent, runlinks;
                    tabcontent = document.getElementsByClassName("tab");
                    for (i = 0; i < tabcontent.length; i++) {
                        tabcontent[i].style.display = "none";
                    }
                    runlinks = document.getElementsByClassName("sidenav")[0].getElementsByTagName("a");
                    for (i = 0; i < runlinks.length; i++) {
                        runlinks[i].className = "";
                    }
                    document.getElementById(runName).style.display = "block";
                    evt.currentTarget.className = "active";
                    // Update the case name in the main tab
                    document.getElementById("case-name").innerText = evt.currentTarget.innerText;
                    // Open the first tab within the selected run
                    var firstTabButton = document.getElementById(runName).getElementsByClassName("tab-buttons")[0].getElementsByTagName("button")[0];
                    firstTabButton.click();
                }

                function openTab(evt, tabName) {
                    var i, tabcontent, tabbuttons;
                    tabcontent = evt.currentTarget.parentElement.parentElement.getElementsByClassName("tab");
                    for (i = 0; i < tabcontent.length; i++) {
                        tabcontent[i].style.display = "none";
                    }
                    tabbuttons = evt.currentTarget.parentElement.getElementsByTagName("button");
                    for (i = 0; i < tabbuttons.length; i++) {
                        tabbuttons[i].className = "";
                    }
                    document.getElementById(tabName).style.display = "block";
                    evt.currentTarget.className = "active";
                }

                document.getElementsByClassName("sidenav")[0].getElementsByTagName("a")[0].click();
            </script>
        </div>
    </body>
    </html>
    """

    (out_dir / "index.html").write_text(html_content, encoding="utf-8")


d1 = Path("/home/villqrd/veturgentys_cases/vet_urgentys_1")
d2 = Path("/home/villqrd/veturgentys_cases/vet_urgentys_3")

runs_data = []
out_dir = Path("/home/villqrd/veturgentys_cases/out")
print(out_dir)
if out_dir.exists():
    shutil.rmtree(out_dir)
out_dir.mkdir(parents=True, exist_ok=True)
res_dir = out_dir / "res"
res_dir.mkdir(parents=True, exist_ok=True)

for p1 in sorted(d1.iterdir()):
    name = p1.name.partition("_")[-1].partition("_")[-1]
    p2s = [p for p in d2.iterdir() if p.name.endswith(name)]
    if len(p2s) != 1:
        raise ValueError(f"Expected one match for {name}, found {len(p2s)}")
    p2 = p2s[0]

    for ix_run, run1 in enumerate(sorted(p1.iterdir()), 1):
        run2 = p2 / run1.name

        audio_file_path = run1 / "recording.m4a"
        local_file_path = res_dir / f"{name} {ix_run}.m4a"

        markdown_old = json.loads((run1 / "meta.json").read_text())["output"]["report"]["content"]["content"]
        markdown_new = json.loads((run2 / "meta.json").read_text())["output"]["report"]["content"]["content"]
        runs_data.append(
            {
                "name": f"{name} {ix_run}",
                "audio_file_path": local_file_path.relative_to(out_dir),
                "markdown_new": markdown_new,
                "markdown_old": markdown_old,
            }
        )
        shutil.copy(audio_file_path, local_file_path)


generate_html_page_with_side_by_side_diff(runs_data, out_dir, "v0.1", "v0.2")
