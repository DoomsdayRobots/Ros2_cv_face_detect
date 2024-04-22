from setuptools import find_packages, setup

package_name = 'cv_face_detect'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dop-t530',
    maintainer_email='kup1977@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'img_publisher = cv_face_detect.webcam_pub:main',
        'img_subscriber = cv_face_detect.webcam_sub:main',
        ],
    },
)
