from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='resistant_kafka_avataa',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        "confluent-kafka==2.8.2",
        "pydantic==1.10.21"
    ],
    long_description=description,
    long_description_content_type='text/markdown',
)
