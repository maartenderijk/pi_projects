import re
from os import path, listdir

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
                        for template_name in templates.groups():
                            template_content = self.read_templates(template_name)
                            writer.write(template_content)
                    else:
                        writer.write(line)

    def read_templates(self, template_name):
        template_tag = template_name.strip()
        template_files = [f for f in listdir(self.template_folder) if path.isfile(path.join(self.template_folder, f)) and f.startswith(template_tag)]
        template_content = ""
        
        if len(template_files) == 0:
            return template_content
 
        for template_file in template_files:
            with open(path.join(self.template_folder, template_file)) as template_reader:
                template_content += template_reader.read() 
        return template_content

        

if __name__ == "__main__":
    s = SiteGenerator()
    s.output_file = "./render/index.html"
    s.render()