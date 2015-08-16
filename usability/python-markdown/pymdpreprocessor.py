# -*- coding: utf-8 -*-
"""This preprocessor replaces Python code in markdowncell with the result
stored in cell metadata
"""

from nbconvert.preprocessors import *
import re

def get_variable( match, variables):
    try:
        x = variables[match]
        return x
    except KeyError:
        return ""


class PyMarkdownPreprocessor(Preprocessor):
    
    def replace_variables(self,source,variables):
        """
        Replace {{variablename}} with stored value
        """
        try:
            replaced = re.sub("{{(.*?)}}", lambda m: get_variable(m.group(1),variables) , source)
        except TypeError:
            replaced = source
        return replaced

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess cell

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """
        if cell.cell_type == "markdown":
            if hasattr(cell['metadata'], 'variables'):
                variables = cell['metadata']['variables']
                if len(variables) > 0:
                    cell.source = self.replace_variables(cell.source, variables)
        return cell, resources
