from ai_assistant.llm_cli import openai_client
from ai_assistant.prompt_llm import AIAssistant
from ai_assistant.consts import COMMANDS
from file_processing import file_handling
from ai_assistant.llm_cli import openai_client
from ai_assistant.prompt_llm import AIAssistant
from ai_assistant.consts import COMMANDS
from rich.console import Console
from rich.theme import Theme
from yaspin import yaspin
import click
from pathlib import Path





custom_theme = Theme({"success": "green", "failure": "bold red", "fun": "purple"})


console = Console(theme=custom_theme)




@yaspin(text="Generating code documentation...")
def prompt(code: str):
    loader = yaspin()
    loader.start()
    assistant = AIAssistant(openai_client)
    result = assistant.run_assistant(code, COMMANDS["w_doc"])
    loader.stop()
    return result





@click.group()
def cli():
    pass



@click.command()
@click.argument('directory', type=Path)
# @click.argument('url', type=str)
# @click.argument('repo_id', type=str)
def scan_project(directory):
    gitignore_content = file_handling.parse_gitignore(directory)
    if gitignore_content != None:
        ignore = set(gitignore_content)
        result = file_handling.process_directory(directory, ignore)
        return print(result)
    result = file_handling.process_directory(directory, {})
    return print(gitignore_content)
    


@click.command()
@click.argument('directory', type=Path)
# @click.argument('url', type=str)
# @click.argument('repo_id', type=str)
def read_file_content(directory):
    result = file_handling.read_file_content(directory)
    print(result)


@click.command()
@click.argument('directory', type=Path)
# @click.argument('url', type=str)
@click.argument('new_content', type=str)
def modify_file_content(directory: Path, new_content: str):
    result = file_handling.modify_file_content(directory, new_content)
    print(result)

@click.command()
@click.argument('directory', type=Path)
# @click.argument('url', type=str)
def delete_file(directory: Path):
    isDeleted = file_handling.delete_file(directory)
    if isDeleted:
        print("true")
    print("false")


@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def write_doc(directory):
    source_code = file_handling.process_directory(directory)
    response = prompt(source_code)
    if type(response):
        file_handling.create_markdown_file("./documentation", response.data)
        console.print("check for: documentation.md at the root of your project 📁", style="fun")
        console.print("Thanks for using ano-code 😉.", style="fun")
    else:
        console.print(response.data, style="failure")


cli.add_command(write_doc)
cli.add_command(scan_project)
cli.add_command(read_file_content)
cli.add_command(modify_file_content)
cli.add_command(delete_file)


if __name__ == "__main__":
    write_doc()
    
