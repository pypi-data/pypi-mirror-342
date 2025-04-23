# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spicypy', 'spicypy.control', 'spicypy.signal', 'spicypy.signal.spectral']

package_data = \
{'': ['*']}

install_requires = \
['control>=0.10.1,<1.0',
 'gwpy>=3.0.10,<4.0',
 'h5py>=3,<4',
 'lpsd>=1.0.5,<2.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.26.4,<3.0',
 'scipy>=1.5,<2.0']

setup_kwargs = {
    'name': 'spicypy',
    'version': '0.9',
    'description': 'A python package for signal processing & control systems. Combining several tools to facilitate signal processing, control systems modelling, and the interface between the two.',
    'long_description': '# spicypy\n\nSignal processing & control systems. Combining several tools to facilitate signal processing, control systems modelling,\nand the interface between the two.\n\nMore details are provided in [Documentation](https://pyda-group.gitlab.io/spicypy/).\n\n# Development roadmap\n\nSpicypy is based on two main packages: [GWpy](https://gwpy.github.io/docs/) for\nsignal-processing and [python-control](https://python-control.readthedocs.io/en/latest/)\nfor control systems modelling. The goal is to reuse as much of existing functionality of\nthese packages as possible.\nNovel functionality to be implemented is discussed in\n[Issues](https://gitlab.com/pyda-group/spicypy/-/issues).\n\nDevelopment process is steered by regular [meetings](https://gitlab.com/pyda-group/spicypy/-/wikis/home/meetings)\nwith participants across the gravitational wave science community.\n\nThe project is open for contributions, and feedback on usage is welcome. For reporting bugs and specific code suggestions\nplease consider [creating an Issue](https://gitlab.com/pyda-group/spicypy/-/issues/new?issue%5Bmilestone_id%5D=).\nFor other enquiries contact details are provided below.\n\n# Contact\n\n* Artem Basalaev (artem.basalaevATpmDOTme)\n* Christian Darsow-Fromm (cdarsowfATphysnetDOTuni-hamburg.de)\n* Oliver Gerberding (oliver.gerberdingATphysikDOTuni-hamburg.de)\n* Martin Hewitson (martin.hewitsonATaeiDOTmpg.de)\n\n# Cite\n\nIf you wish to reference Spicypy in your publication, please use citation provided here: [https://doi.org/10.5281/zenodo.10033637](https://doi.org/10.5281/zenodo.10033637).\n\n# License\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)\n\n  Unless required by applicable law or agreed to in writing, software\n  distributed under the License is distributed on an "AS IS" BASIS,\n  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n  See the License for the specific language governing permissions and\n  limitations under the License.\n',
    'author': 'Artem Basalaev',
    'author_email': 'artem.basalaev@physikDOTuni-hamburg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/pyda-group/spicypy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.14',
}


setup(**setup_kwargs)
