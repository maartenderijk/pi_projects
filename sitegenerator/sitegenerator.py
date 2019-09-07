import re
from os import path, listdir


class SiteGenerator(object):
    ''' 
    Simple template based site generator.
    Replaces all the {{ templatename }} tags in the base template with the template contents.
    Replaces all the {% variable %} tags with values from the SiteGenerator.replacements dictionary
    '''

    def __init__(self, base_template="base.html", output_file="index.html", template_folder="./templates", replacements={}):
        self.base_template = base_template
        self.output_file = output_file
        self.template_folder = template_folder
        self.replacements = replacements

    def render(self):
        re_pattern_templates = r"([{][{]\s*\S*\s*[}][}])"

        with open(self.output_file, "w") as writer:
            with open(path.join(self.template_folder, self.base_template)) as base_reader:
                for line in base_reader:
                    templates_matches = re.findall(re_pattern_templates, line)
                    if templates_matches:
                        for template_name in templates_matches:
                            template_content = self.read_templates(
                                template_name)
                            writer.write(template_content)

                    else:
                        writer.write(line)

        self.replace_tags()

    def read_templates(self, template_name):
        """ 
        Returns content of all the templates with the same template tag.
        The template tag is defined as the text in the filename before the first underscore.
        The alfa-numerical order after the first underscore is used as render order.
        """
        template_tag = (template_name[2:-2].strip()).split("_")[0]
        template_files = [f for f in listdir(self.template_folder) if path.isfile(
            path.join(self.template_folder, f)) and f.startswith(template_tag)]
        template_files.sort(reverse=True)

        template_content = ""

        if len(template_files) == 0:
            return template_content

        for template_file in template_files:
            with open(path.join(self.template_folder, template_file)) as template_reader:
                template_content += template_reader.read()
        return template_content

    def replace_tags(self):
        """ 
        Replaces all the {% variable %} tags in the output file with values from the replacement dictionary.
        If no match if found in the dictionary the tag will not be replaced.
        """

        re_pattern_replacements = r"([{][%]\s*\S*\s*[%][}])"

        with open(self.output_file, 'r') as template_file:
            template_data = template_file.read()

        replacements_matches = re.findall(
            re_pattern_replacements, template_data)
        for replacement_tag in replacements_matches:
            r = (replacement_tag[2:-2]).strip()
            new_text = self.replacements.get(r)

            if new_text:
                template_data = template_data.replace(
                    replacement_tag, new_text)

        with open(self.output_file, 'w') as template_file:
            template_file.write(template_data)


if __name__ == "__main__":
    s = SiteGenerator()
    s.output_file = "./render/index.html"
    s.replacements = {"footertext": "This is a footertext",
                      "secondtext": "This is secondtext"}
    s.render()
