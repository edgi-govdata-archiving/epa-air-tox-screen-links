import datetime


def get_internet_archive_url(url):
    this_year = datetime.datetime.now().year
    return f"https://web.archive.org/web/{this_year}0000000000*/{url}"


def generate_name(url):
    """
    For example, from https://gaftp.epa.gov/rtrmodeling_public/AirToxScreen/2020/Cancer/BySource/Region1_CancerRisk_by_block_srcgrp.xlsx
    to AirToxScreen/2020/Cancer/BySource/Region1_CancerRisk_by_block_srcgrp.xlsx
    by removing the host and the first slash, then replacing slashes with spaces
    """
    starter = url.replace("https://www.epa.gov/system/files/documents/", "")
    starter = starter.replace("https://www.epa.gov/system/files/other-files/", "")
    starter = starter.replace("https://gaftp.epa.gov/rtrmodeling_public/", "")
    starter = starter.replace("%20", " ")
    filename = starter.split("/")[-1]
    starter = starter.replace(filename, "")
    starter = starter.replace("_", " ")
    starter = starter.replace("/", " ")
    # replace hyphens with discretionary hyphens
    starter = starter.replace("-", "&#8209;")
    # replace extension with (extension)
    filename, extension = filename.split(".")
    filename = filename.replace("_", " ")
    return f"{starter}: {filename} ({extension})"


def generate_description():
    text = """
  <p>
  This is a list of links to the EPA's Air Tox Screen data.
  The data is available in the EPA's website and in the Internet Archive.
  The list was generated in January, 2025 from the EPA's website. Note that the links may have changed since then,
  and the Internet Archive may not have captured the most recent version of the data.
  This page provided by the Environmental Data and Governance Initiative <a href="https://envirodatagov.org/">(EDGI)</a>.
  The GitHub repository for this page is <a href="https://github.com/willf/epa-air-tox-screen-links"><code>epa-air-tox-screen-links</code></a>.
  </p>
  """
    return text


def generate_index():
    with open(
        "/Users/willf/edgi/epa-air-tox-screen-links/epa-air-tox-screen-links.txt", "r"
    ) as file:
        urls = file.readlines()

    html_content = (
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EPA 2020 AirToxScreen: Assessment Result Links</title>
        <style>
      body {
        font-family: Georgia, sans-serif;
        background-color: #f4f4f4;
        font-size: 16px;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: left;
        align-items: left;
        height: 100vh;
      }
      .container {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        text-align: left;
      }
      h1 {
        color: #333;
        font-family: Arial, sans-serif;
      }
      label {
        display: block;
        margin: 10px 0 5px;
        font-weight: bold;
      }
      select {
        width: 33%;
        padding: 10px;
        margin-bottom: 20px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      button {
        width: 20%;
        padding: 10px;
        margin-top: 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
      }
      button:hover {
        background-color: #0056b3;
      }
      button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
      }
      quote {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 80%;
        background-color: #f9f9f9;
        border-left: 10px solid #ccc;
        margin: 20px 0;
        padding: 10px 20px;
        font-style: italic;
        color: #555;
      }
      code {
      font-size: 100%
      }
      table {

        width: 100%;
      }
      th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
      }
    </style>
    </head>
    <body>
    <div id="container" class="container">
        <h1>EPA 2020 AirToxScreen: Assessment Result Links</h1>
    """
        + f"""
        {generate_description()}
        <table>
    """
    )

    for url in urls:
        url = url.strip()
        name = generate_name(url)
        archive_url = get_internet_archive_url(url)
        html_content += f'<tr><td><code>{name}</code></td><td><a href="{url}" target="_blank">EPA</a></td>'
        if archive_url:
            html_content += (
                f'<td><a href="{archive_url}" target="_blank">Internet Archive</a></td>'
            )
        html_content += "</tr>"

    html_content += """
        </table>
    </div>
    </body>
    </html>
    """

    with open("/Users/willf/edgi/epa-air-tox-screen-links/index.html", "w") as file:
        file.write(html_content)


if __name__ == "__main__":
    generate_index()
