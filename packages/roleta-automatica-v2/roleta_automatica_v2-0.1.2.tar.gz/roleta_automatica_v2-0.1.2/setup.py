from setuptools import setup, find_packages

setup(
    name='roleta-automatica-v2',
    version='0.1.2',
    author='Auto Dev',
    author_email='autodev331@gmail.com',
    description='Automatização do site Blaze usando Selenium para jogar roleta.',
    keywords='selenium, automação, roleta, blaze',
    license='MIT',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/autodev/automacao-blaze',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
        'webdriver-manager>=3.8.0',
        "automacao_blaze_cassino>=0.1.0",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
