from setuptools import setup

setup(
    name='tk-animations',
    version='0.1.0',
    py_modules=['tk_animations'],  # Refers to your single .py file
    author='itsDevLune',
    author_email='officaldevanarayan@gmail.com',
    description='A Tkinter animation library with 10 reusable animations.',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itsDevlune/TkAnimator',  # Update with your real repo
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',
)
