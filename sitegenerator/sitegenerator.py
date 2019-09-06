import re
from os import path, listdir

# TODO: Check Regex
# TODO: Remove strip() functions
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
        re_pattern_templates = "[{][{]\s*(\S*)\s*[}][}]"

        with open(self.output_file, "w") as writer:
            with open(path.join(self.template_folder, self.base_template)) as base_reader:
                for line in base_reader:

                    templates = re.search(re_pattern_templates, line)
                    if templates:
                        for template_name in templates.groups():
                            template_content = self.read_templates(
                                template_name)
                            writer.write(template_content)

                    else:
                        writer.write(line)

        # self.replace()

    def read_templates(self, template_name):
        template_tag = template_name.strip()
        template_files = [f for f in listdir(self.template_folder) if path.isfile(
            path.join(self.template_folder, f)) and f.startswith(template_tag)]
        template_content = ""

        if len(template_files) == 0:
            return template_content

        for template_file in template_files:
            with open(path.join(self.template_folder, template_file)) as template_reader:
                template_content += template_reader.read()
        return template_content

    def replace(self):
        re_pattern_replacements = "[{][%]\s*(\S*)\s*[%][}]"

        with open(self.output_file, 'r') as file:
            filedata = file.read()

        replacements_matches = re.findall(re_pattern_replacements, filedata)
        for r in replacements_matches:
            print(self.replacements.get(r))

            filedata = filedata.replace(r, 'abcd')

        # # Write the file out again
        # with open('file.txt', 'w') as file:
        #     file.write(filedata)


if __name__ == "__main__":
    s = SiteGenerator()
    s.output_file = "./render/index.html"
    s.replacements = {"footertext": "This is a footertext",
                      "secondtext": "This is secondtext"}
    s.render()
