from setuptools import setup, find_packages

setup(name='esewa-profanity',
       version='0.0.10',
       author='Ankit Lamsal',
       author_email='ankit.lamsal@esewa.com.np',
       description='A library for detecting profanity from different languages.',
       long_description= open('README.md').read(),
       long_description_content_type='text/markdown',
       packages = find_packages(),
       classifiers=["Programming Language :: Python :: 3.8",
                #     "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"],
        package_data={
            'esewa-profanity':['files/encoded_files/*','files/json/*', 'files/keys/*']
        },
        python_requires='>=3.8'
)