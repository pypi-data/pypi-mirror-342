from setuptools import setup, find_packages

setup(
    name='phi_decoding',
    version='0.0.2',
    author='Fangzhi Xu, Hang Yan',
    author_email='fangzhixu98@gmail.com',
    description='Adaptive Foresight Sampling',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xufangzhi/phi-Decoding',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
