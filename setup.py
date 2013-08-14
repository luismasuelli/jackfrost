from distutils.core import setup

setup(
    name='jackfrost',
    version='0.5',
    packages=['jackfrost'],
    url='',
    license='GPL',
    author='Luis Masuelli',
    author_email='luismasuelli@hotmail.com',
    description='Autocomplete feature for django. Allows you to serve a channel as a datasource to select an option from a large amounth without need to hit the whole DB set.',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers'
    ]
)
