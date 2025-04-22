from lib4sbom.generator import SBOMGenerator, SBOMOutput
from lib4sbom.parser import SBOMParser

base_parse = SBOMParser()
base_parse.parse_file("/root/Downloads/alma.spdx")

sbom_output = SBOMOutput(output_format="Tag")
print(base_parse.get_sbom())
sbom_output.generate_output(base_parse.get_sbom())


# my_generator = SBOMGenerator(False, sbom_type="spdx", format="tag")
# Will be displayed on console
# my_generator.generate("TestApp", base_parse.get_sbom())
