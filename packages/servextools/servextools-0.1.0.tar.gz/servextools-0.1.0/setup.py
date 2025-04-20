from setuptools import setup, find_packages

setup(
    name='ServexTools',
    version='0.1.0',
    author='Servextex',
    author_email='info@servextex.com.do',
    description='Librería de herramientas para Servextex',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Servextex/ServexTools',  # Opcional
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
)
