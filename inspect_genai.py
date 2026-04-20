import google.generativeai as genai
import pkg_resources
print(pkg_resources.get_distribution('google-generativeai').version)
print([n for n in dir(genai) if n.startswith('Text') or n.startswith('Generative') or n.startswith('generate') or n in ('configure','api_key')])
