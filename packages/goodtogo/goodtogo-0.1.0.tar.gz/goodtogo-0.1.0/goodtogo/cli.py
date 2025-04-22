# cli.py
import os
import click

from colorama import Fore

from goodtogo.files import readlines, writelines, downloads_path
from goodtogo.scraper import scrap
from goodtogo.pdf import generate_pdf

from goodtogo.langs import languages

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """🐿️ Good to Go - Check if your AP CSP personal project is ready for submission, scrape comments and help document."""

@cli.command()
@click.option("-i", "--input", prompt="Input a path to the script", help="Script to scrape", type=str)
@click.option("-t", "--type", prompt="What type of file?", help="Type of file", type=click.Choice(languages))
@click.pass_context
def scrape(ctx: click.Context, input: str, type: click.Choice):
    """scrape comments off your file and generate a copy without it"""

    chosen_lang = languages[type]

    data = readlines(input)
    new = scrap(data, chosen_lang["comment"], chosen_lang["multiline"])

    file_name = os.path.basename(input)

    copy_title_split = file_name.split(".")

    file_name = downloads_path + "/" + copy_title_split[0] + "-good." + copy_title_split[1]

    writelines(file_name, new)
    
    click.echo("")
    click.echo(Fore.GREEN + "☑ Successfully scraped file!")
    click.echo(Fore.RESET + "It can be found in " + Fore.BLUE + file_name)
    click.echo(Fore.RESET + "")

@cli.command()
@click.option("-n", "--name", prompt="Input project name", help="Project Name", type=str)
@click.option("-i", "--input", prompt="Input directory to generate", help="Directory to generate", type=str)
@click.option("-l", "--language", prompt="Language used in project", help="Language to create PDF", type=click.Choice(languages))
@click.pass_context
def generate(ctx: click.Context, name: str, input: str, language: click.Choice): 
    """generate the PDF of the code for your project"""

    code_paths = []

    chosen_lang = languages[language]

    if not input.endswith("/"):
        input = input + "/"

    for file in os.listdir(input):
        if file.endswith(chosen_lang["extension"]):
            code_paths.append(input + file)
            print(file)
            
    generate_pdf(name, code_paths)

    file_name = downloads_path + "/" + name + ".pdf"

    click.echo("")
    click.echo(Fore.GREEN + "☑ Successfully generated project PDF!")
    click.echo(Fore.RESET + "It can be found in " + Fore.BLUE + file_name)
    click.echo(Fore.RESET + "")