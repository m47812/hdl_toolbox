import os
import textwrap

class TemplateManager:
    def template_file_path(self, template_path):
        # get the directory of the current script
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # join the directory of the current script with the relative path
        absolute_path = os.path.join(current_dir, template_path)
        # normalize the path (remove any .., ., etc.)
        absolute_path = os.path.normpath(absolute_path)
        return absolute_path
    
    def read_template_file_abs_path(self, abs_path):
        try:
            with open(abs_path, 'r') as file:
                data = file.read()
        except:
            raise FileNotFoundError("The given file was not found:" + abs_path)
        return data
    
    def read_template_file_relative_path(self, template_path):
        abs_path = self.template_file_path(template_path)
        return self.read_template_file_abs_path(abs_path)
    
    def indent(self, string, nb_tabs):
        return textwrap.indent(string, 4 * nb_tabs * ' ')
