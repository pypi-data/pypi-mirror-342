from setuptools import setup

setup(
    name='SetMail',
    version='0.1',
    author='Your Name',
    author_email='your@email.com',
    description='Minimalist email sending for Python — just import and send',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/SetMail/',
    packages=['setmail'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
