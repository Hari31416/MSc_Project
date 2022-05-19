import nbformat
from nbconvert import HTMLExporter
import bs4
import pyperclip
import os
import re
import tqdm


class Notebook:
    """
    Tools for Jupyter Notebooks. Available methods are:
    - create_content: Creates a table of contents for a notebook using the headers defined in the notebook.
    - export_notebook: Export a notebook to an HTML file.
    - export_directory: Exports every Jupyter notebook in the current directory to HTML.
    - list_notebooks: Returns a list of the paths to the notebooks in the current directory.
    """

    def __init__(self, directory=os.curdir) -> None:
        self.directory = directory
        self.notebooks = self.list_notebooks()

    def list_notebooks(self):
        """
        List all the notebooks in the current directory.

        Returns
        -------
        notebooks : list
            List of the paths to the notebooks.
        """
        notebooks = []
        for file in os.listdir(self.directory):
            if "checkpoint" in file:
                continue
            if file.endswith(".ipynb"):
                notebooks.append(os.path.join(self.directory, file))
        return notebooks

    def export_notebook(self, notebook_path, output_path=None):
        """
        Export a notebook to an HTML file.

        Parameters
        ----------
        notebook_path : str
            Path to the notebook to export.
        output_path : str
            Path to the output file.

        Returns
        -------
        output_path : str
            Path to the output  html file.
        """
        # Extracting html from the notebook
        notebook = nbformat.read(notebook_path, as_version=4)
        html_exporter = HTMLExporter(template_name="classic")
        (body, _) = html_exporter.from_notebook_node(notebook)

        if output_path is None:
            output_path = os.path.splitext(notebook_path)[0] + ".html"

        # Fixing the title
        title = notebook_path.split(os.path.sep)[-1].split(".")[0]
        title = title.replace("_", " ").title()
        body = re.sub("<title>Notebook</title>", f"<title>{title}</title>", body)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(body)

        return output_path

    def export_directory(self):
        """
        Exports every Jupyter notebook in the current directory to HTML.

        Returns
        -------
        file_paths: list
            List of the paths to the HTML files.
        """
        file_paths = []
        for file in tqdm.tqdm(self.notebooks, desc="Exporting notebooks..."):
            path = self.export_notebook(os.path.join(self.directory, file))
            file_paths.append(path)
        return file_paths

    def create_content(self, notebook_path, return_string=False):
        """
        Creates a table of contents for a notebook using the headers defined in the notebook.

        Parameters
        ----------
        notebook_path : str
            Path to the notebook to create the table of contents for.
        return_string : bool
            If True, returns the table of contents as a string.

        Returns
        -------
        table_of_contents : str
            Table of contents as a string.
        """
        print("Converting the Notebook to HTML.")
        notebook = nbformat.read(notebook_path, as_version=4)
        html_exporter = HTMLExporter(template_name="classic")
        (body, _) = html_exporter.from_notebook_node(notebook)
        soup = bs4.BeautifulSoup(body, "lxml")

        print("Looking for the Headers and their positions.")
        headers = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}

        for hs in headers.keys():
            headers[hs] = soup.select(hs)

        positions = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
        all = []
        for hs in positions.keys():
            positions[hs] = [str(soup).find(str(h)) for h in headers[hs]]
            all.extend(positions[hs])
        all.sort()
        positions["all"] = all

        print("Getting correct order of the Headers.")
        correct_order = []
        for i in positions["all"]:
            for keys in positions.keys():
                if i in positions[keys]:
                    correct_order.append(keys)
                    break

        index = []
        for order in correct_order:
            index.append(headers[order][0])
            headers[order].pop(0)

        print("Creating the Contents.")
        start = "<ol>"
        end = "</ol>"
        string = f"""<h2 id="Contents">Contents<a href="#Contents"></a></h2>
        {start}
        """
        current_header = "h1"
        for i, order in enumerate(correct_order):
            previous_header = current_header
            current_header = order
            to_add = f"""<li>{str(index[i].select('a')[0]).replace("¶", index[i].get_text()[:-1]).replace("anchor-link", "")}</li>\n"""
            if previous_header == current_header:
                string += to_add

            elif int(previous_header[-1]) < int(current_header[-1]):
                string += start
                string += to_add

            elif int(previous_header[-1]) > int(current_header[-1]):
                string += end
                string += to_add
        string += end
        pyperclip.copy(string)
        print("Content copied to clipboard.")
        if return_string:
            return string
        else:
            return None
