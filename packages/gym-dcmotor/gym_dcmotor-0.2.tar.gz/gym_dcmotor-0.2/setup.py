from setuptools import setup

setup(name='gym_dcmotor',
      version='0.2',
      author="LlewynS",  
      author_email="algos251@gmail.com",  
      description="A simple DC motor environment for reinforcement learning",
      long_description=open("README.md").read(),  
      long_description_content_type="text/markdown",
      url="https://github.com/llewynS/dcmotorenv",   
      install_requires=['gymnasium',
                        'numpy',
                        'matplotlib',],
      license='GNUAGPLv3',
      zip_safe=False,
)