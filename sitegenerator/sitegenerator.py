import re
from os import path

class SiteGenerator(object):
    ''' 
    Simple template based site generator.
    Replaces all the {{ templatename }} tags in the base template with the template contents.
   
    '''
    def __init__(self, base_template="./base.html", output_file="index.html", template_folder="./templates"):
        self.base_template = base_template
        self.output_file = output_file
        self.template_folder = template_folder
    
    def render(self):
        re_pattern = "[{][{](.*)[}][}]" 

        with open(self.output_file, "w") as writer:
            with open(path.join(self.template_folder, self.base_template)) as base_reader:
                for line in base_reader:
                
                    templates = re.search(re_pattern, line)        
                    if templates:
                        for template in templates.groups():
                            template_content = self.read_template(template)
                            writer.write(template_content)
                    else:
                        writer.write(line)

    def read_template(self, template):
        template_file = template.strip() + ".html"
        with open(path.join(self.template_folder, template_file)) as template_reader:
            template_content = template_reader.read() 
        return template_content

        

if __name__ == "__main__":
    s = SiteGenerator()
    s.output_file = "./render/index.html"
    s.render()