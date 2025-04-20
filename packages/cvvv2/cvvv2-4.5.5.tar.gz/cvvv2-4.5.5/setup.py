from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cvvv2',  # Changed from 'cv2' to a safe name
    version='4.5.5',
    packages=find_packages(),
    description='A fake OpenCV package for Python used in security awareness training',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='VisionLab Research',
    author_email='contact@visionlab-security.org',
    url='https://visionlab-security.org/cv2-awareness',
    license='MIT',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
)
