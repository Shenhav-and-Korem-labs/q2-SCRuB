

# Copyright (c) 2022, SCRuB development team.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import versioneer
from setuptools import setup, find_packages

setup(
    name="SCRuB",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="George Austin",
    author_email="gia2105@columbia.edu",
    description="Source-tracking for Contamination Removal in microBiomes (SCRuB)",
    license='cc-by-sa-4.0',
    url="https://github.com/korem-lab/SCRuB",
    entry_points={
        'qiime2.plugins': ['q2-SCRuB=q2_SCRuB.plugin_setup:plugin']
    },
    scripts=['q2_SCRuB/assets/run_SCRuB.R'],
    package_data={
        "q2_SCRuB": ['citations.bib'],
	'q2_SCRuB.tests': ['data/*']
    },
    zip_safe=False,
)
