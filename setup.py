from distutils.core import setup
import os

setup(
    name='jackfrost',
    version='0.5.4',
    packages=['jackfrost'],
    package_data={'jackfrost': [os.path.join('static', 'css', 'themes', 'base', 'images', '*.png'),
                                os.path.join('static', 'css', 'themes', 'base', '*.css'),
                                os.path.join('static', 'css', '*.js')]},
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
