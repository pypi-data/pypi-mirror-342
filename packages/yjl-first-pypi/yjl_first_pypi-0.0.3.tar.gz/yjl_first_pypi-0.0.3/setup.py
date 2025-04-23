from setuptools import setup, find_packages            #这个包没有的可以pip一下
print(find_packages())

setup(
    name = "yjl-first-pypi",      #这里是pip项目发布的名称
    version = "0.0.3",  #版本号，数值大的会优先被pip
    keywords = ("pip", "yjl-first-pypi"),
    description = "A successful sign for python setup",
    long_description = "A successful sign for python setup",
    license = "MIT Licence",

    url = "http://python4office.cn/upload-pip/",     #项目相关文件地址，一般是github
    author = "yjl-first-pypi",
    author_email = "yaojiuox@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []    ,      #这个项目需要的第三方库

     data_files=[
        ("data", ["volcengine-sdk-java-rec-master.zip"]), 
     ] 
)