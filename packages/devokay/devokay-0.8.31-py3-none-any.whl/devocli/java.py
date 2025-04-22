

# brew install adoptopenjdk8
PKG_JDK_8 = 'adoptopenjdk8'

# brew install adoptopenjdk11
PKG_JDK_11 = 'adoptopenjdk11'

'''
cd /Library/Java/JavaVirtualMachines/  #进入这个目录

ls  #查看目录下的文件

下面是我的openjdk8的目录，也就是java8的安装目录

/Library/Java/JavaVirtualMachines/openjdk-8.jdk/Contents/Home

openjdk11的目录，也就是java11的安装目录

/Library/Java/JavaVirtualMachines/adoptopenjdk-11.jdk/Contents/Home
'''


'''
# openjdk8 
java8=/Library/Java/JavaVirtualMachines/openjdk-8.jdk/Contents/Home

# openjdk 11
java11=/Library/Java/JavaVirtualMachines/adoptopenjdk-11.jdk/Contents/Home

# default jdk8
export JAVA_HOME=$java8

alias java8="export JAVA_HOME=$java8"
alias java11="export JAVA_HOME=$java11"

'''
