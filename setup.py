from setuptools import setup

setup(
    name='samplyser',
    version='0.0.01',
    license='MIT',
    description='Automatic analysis of soundfiles.',
    author='Levin Eric Zimmermann',
    author_email='levin-eric.zimmermann@folkwang-uni.de',
    url='https://github.com/uummoo/samplyser',
    packages=['samplyser', 'samplyser.pitch',
              'samplyser.duration', 'samplyser.amplitude'],
    setup_requires=[''],
    tests_require=['nosetests'],
    install_requires=[''],
    extras_require={},
    python_requires='>=3.6'
)
