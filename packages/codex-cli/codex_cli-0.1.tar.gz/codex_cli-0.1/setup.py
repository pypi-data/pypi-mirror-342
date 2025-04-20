from setuptools import setup, find_packages

setup(
    name='codex_cli',  # Your tool's name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',  # For interacting with Google's Gemini API
        'Pillow',                # For working with images (PIL)
        'python-dotenv',         # To load environment variables from .env file
    ],
    entry_points={
        'console_scripts': [
            'codex-cli=codex_cli.codex_cli:main',  # Replace with your main function path
        ],
    },
    author='Chinnapothula Akhil',
    author_email='your.email@example.com',  # Replace with your email
    description='A CLI tool powered by OpenAI for various functionalities like code generation, explanation, etc.',
    long_description=open('README.md').read(),  # Link to your README for detailed description
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/codex_cli',  # Replace with your project URL
    license='MIT',  # Add MIT license here
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
