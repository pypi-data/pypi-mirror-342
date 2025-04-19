from setuptools import setup, find_packages

setup(
    name='gc_temp_tables',
    version='1.1.0',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description= "Python utility for creating and querying temporary tables in Google Cloud Environments.",
    long_description= """
`gc_temp_tables` lets you easily create and query temporary tables within Google Cloud environments. The user has the option to work within a session and/or use external tables. The functions in `gc_temp_tables` are below:

 * `create_bq_session()`.
 * `get_external_table_config(filename_in_bucket)`.
 * `create_temp_table(query)`
 * `query_temp_table()`
 * `delete_temp_table()`.

`gc_temp_tables` was originally written to be used within the All of Us Researcher Workbench environment but can be used in other Google Cloud Environments.

More details, including **code snippet**, at: https://github.com/AymoneKouame/data-science-utilities/blob/main/README.md#1---package-gc_temp_tables

""",

    long_description_content_type="text/markdown",
    url = 'https://github.com/AymoneKouame/data-science-utilities',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)