from setuptools import setup, find_packages

setup(
    name='at_general_purpose_terminal_chatbot',
    version='1.9',
    packages=find_packages(),
    install_requires=[
        "langchain_openai>=0.2.14",
        "dotenv",
        "rich"
    ],
    author='Arthur Timoteo',
    author_email='arthur.timoteo@gmail.com',
    description='Chatbot for general purpose tasks using LangChain and OpenAI API',
    license='MIT',
    long_description_content_type='text/markdown',
    url='https://github.com/arthur-timoteo/general_purpose_terminal_chatbot/tree/feature-python_31012-langchain_0214/python/3.10.12/langchain/0.2.14',
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "cbcli=atgeneralpurposeterminalchatbot.main:main",
        ],
    },
)