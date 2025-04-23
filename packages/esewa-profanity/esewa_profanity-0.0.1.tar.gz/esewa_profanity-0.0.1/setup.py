from setuptools import setup, find_packages

setup(name='esewa-profanity',
       version='0.0.1',
       author='Ankit Lamsal',
       author_email='ankit.lamsal@esewa.com.np',
       description='A library for detecting profanity from different languages.',
       long_description= open('README.md').read(),
       long_description_content_type='text/markdown',
       packages = ['profanity'],
       classifiers=["Programming Language :: Python :: 3.8",
                #     "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"],
        python_requires='>=3.8'
)