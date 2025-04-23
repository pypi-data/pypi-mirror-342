from setuptools import setup, find_packages

setup(
    name='chembioml',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn==1.3.2',
        'numpy',
        'matplotlib',
        'sklearn-genetic',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'chembioml=chembioml.cli:main'
        ],
    },
    author='Viacheslav Muratov',
    author_email='support@chembioml.com',
    description='ChemBioML Platform for machine learning in chemistry and biology',
    url='https://github.com/chembiodev/ChemBioML-Platform-OS',
    license='GNU General Public License v3.0 (see https://www.gnu.org/licenses/gpl-3.0.en.html)',  # Or your chosen license
    python_requires='>=3.8',
)
