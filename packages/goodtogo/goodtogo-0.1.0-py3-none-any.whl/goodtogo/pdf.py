import click
import os

from xhtml2pdf import pisa

from goodtogo.files import readlines, downloads_path

def generate_pdf(name: str, code_md: list[str]):
    pisa.showLogging()
    verify_creation = input("Are you sure you want to generate? (y/n) ")

    if (verify_creation != "y"):
        click.echo("Cancelling...")
        return

    text = f"<html><body><div><h1>{name} - AP CSP</h1></div><br></br>"

    for file in code_md:
        lines = readlines(file)
        title = os.path.basename(file)
        text = text + f"<div style='margin: 0;'><h3>{title}</h3></br><pre><code>"
        for line in lines:
            text = text + line + "<br></br>"

        text = text + f"</code></pre></div>"

    text = text + "</body></html>"

    with open(downloads_path + "/" + name + ".pdf", "w+b") as destination:
        pisa_status = pisa.CreatePDF(
        text,
        dest=destination, 
        )