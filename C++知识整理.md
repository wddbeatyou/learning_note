## C++知识整理

### 一、编译器安装

待定；

### 二、概念解答

#### 1.cmake与make的简介

```
CMake定义：
	CMake 是一个跨平台的构建系统生成工具。它不直接构建项目，而是生成适用于不同平台和编译器的构建文件（如 Makefile 或 Visual Studio 项目文件）。

Make定义：
	Make 是一个构建工具，通过读取 Makefile 文件来执行编译、链接等任务。

```

```
区别：
    功能层级:
        CMake 是构建系统生成器，生成 Makefile 或其他构建文件。
        Make 是构建工具，直接执行构建任务。
    跨平台支持:
        CMake 支持跨平台，生成适用于不同系统的构建文件。
        Make 通常用于类 Unix 系统，跨平台支持较弱。
    易用性:
        CMake 提供更高层次的抽象，简化跨平台构建。
        Make 需要手动编写 Makefile，适合对构建过程有精细控制需求的开发者。
```

```
典型工作流程：
    CMake:
        1.编写 CMakeLists.txt。
        2.运行 cmake 生成 Makefile 或其他构建文件。
        3.运行 make 或其他构建工具进行构建。
    Make:
        1.手动编写 Makefile。
        2.直接运行 make 进行构建。
```

```
适用场景：
    CMake： 
        更适合跨平台项目，简化构建系统生成。
    Make： 
        适合单平台项目，提供更直接的构建控制。
```

#### 2.动态库与静态库的简介

```
静态库(Static Library)定义：
	静态库在编译时会被完整地嵌入到可执行文件中，生成的可执行文件不依赖外部的库文件。
	文件扩展名: 在 Windows 上通常是 .lib，在 Linux 上通常是 .a。
	特点:
        1.编译时链接: 静态库的代码在编译时被复制到可执行文件中。
        2.独立性: 生成的可执行文件不依赖外部库，便于分发。
        3.体积较大: 因为库代码被复制到可执行文件中，所以可执行文件体积较大。
        4.更新困难: 如果库代码更新，需要重新编译整个项目。
动态库(Dynamic Library / Shared Library)定义：
	动态库在程序运行时被加载，可执行文件只包含对动态库的引用，而不是库代码本身。
	文件扩展名: 在 Windows 上通常是 .dll，在 Linux 上通常是 .so。
	特点:
        1.运行时链接: 动态库的代码在程序运行时加载，而不是编译时。
        2.体积较小: 可执行文件只包含对动态库的引用，体积较小。
        3.便于更新: 更新动态库时，只需替换库文件，无需重新编译可执行文件。
        4.依赖管理: 可执行文件需要依赖外部的动态库文件，分发时需要确保库文件存在。
```

```
区别：
                          特性	                   静态库	                               动态库
                        链接时机	             编译时链接	                              运行时链接
                        可执行文件体积	      较大（库代码被复制到可执行文件）	          较小（只包含对库的引用）
                        运行时依赖	               无依赖	                             需要外部的动态库文件
                        更新库代码	          需要重新编译整个程序	                    只需替换动态库文件
                        内存占用	        每个程序都包含库代码，内存占用高	        多个程序共享库代码，内存占用低
                        性能	               运行时无链接开销，性能略高	              运行时需要加载库，性能略低
```

```
应用场景:
	静态库:
        需要独立分发的程序，避免依赖外部库。
        对性能要求较高，希望减少运行时动态链接的开销。
        库的代码较小，且不经常更新。
    动态库:
        需要频繁更新库代码的场景。
        多个程序共享同一个库，减少磁盘和内存占用。
        插件化架构，支持运行时加载模块。
```

```
在C++开发中，程序直接编译成可执行文件，为什么还要生成静态库或者动态库，这样做有什么好处和意义？
1. 代码复用
    好处: 将常用的功能封装成库，可以在多个项目中复用，避免重复编写代码。
    意义: 提高开发效率，减少代码冗余，确保功能的一致性。
2. 减少编译时间
    好处: 如果某些模块不经常修改，可以将它们编译成库，避免每次编译整个项目时重新编译这些模块。
    意义: 加快编译速度，特别是在大型项目中效果显著。
3. 节省磁盘和内存空间
    好处: 动态库可以被多个程序共享，减少磁盘和内存占用。
    意义: 在多个程序使用相同库时，避免每个程序都包含一份库代码。
4. 跨平台和兼容性
    好处: 将平台相关的代码封装成库，可以更方便地实现跨平台支持。
    意义: 提高代码的可移植性，减少跨平台开发的复杂性。
5. 隐藏实现细节
    好处: 将核心算法或敏感代码封装成库，只暴露接口，隐藏实现细节。
    意义: 保护知识产权，提高代码的安全性。
```

### 三、CMake的使用

#### 3.1  CMake的安装

```
sudo apt install cmake    # Ubuntu或Debian上
cmake -version            # 查看安装情况
```

#### 3.2 CMake的语法

1.注释

```
一行注释：# 
	例子：
		#这是一行注释
多行注释：#[[ ]]
    例子：
        #[[这是一段注释
            这是一段注释
            这是一段注释
            这是一段注释]]
```

2.版本指定

```
	在CMake的版本更新中会更新新的命令，这些命令在低版本并不兼容，所以需要通过cmake_minimum_required 指定需要的最低版本。这并不是必须的，但如果不加可能会有警告。
语法：
	cmake_minimum_required(VERSION [版本号])
示例：
	cmake_minimum_required(VERSION 3.0)
```

3.工程描述

```
	使用 project 定义工程名称，工程的版本、工程描述、web主页地址、支持的语言（默认情况支持所有语言），如果不需要这些都是可以忽略的，只需要指定出工程名字即可。
解释：
	定义项目名称: project(<PROJECT_NAME>) 这是最基本的用法，只需要指定项目名称。
    版本信息: VERSION <major>[.<minor>[.<patch>[.<tweak>]]] 可以指定项目的版本号。
    项目描述: DESCRIPTION "<description>" 可以为项目添加描述。
    Web主页地址: HOMEPAGE_URL "<url>" 可以指定项目的主页URL。
    支持的语言: LANGUAGES <lang> [<lang>...] 可以指定项目支持的编程语言。如果不指定，默认情况下CMake支持多种语言，如C和C++。
语法：
    project(<PROJECT-NAME>
           [VERSION <major>[.<minor>[.<patch>[.<tweak>]]]]
           [DESCRIPTION <project-description-string>]
           [HOMEPAGE_URL <url-string>]
           [LANGUAGES <language-name>...])
示例：
    #定义项目名称，版本，描述，主页URL，以及支持的语言
    project(
        MyProject
        VERSION 1.0.0
        DESCRIPTION "这是一个示例项目"
        HOMEPAGE_URL "http://www.example.com"
        LANGUAGES CXX
    )
```

4.生成可执行程序

```
使用 add_executable 定义工程生成的可执行程序。
语法：
	add_executable(可执行程序名 源文件名称)
示例：
	add_executable(program main.cpp add.cpp sub.cpp mul.cpp div.cpp)
```

```
使用cmake命令构筑项目。
语法：
	cmake CMakeLists.txt文件所在路径
示例：
	cmake .
```

5.定义变量

```
	在add_executable(program main.cpp add.cpp sub.cpp mul.cpp div.cpp)中，我们使用了五个源文件。如果这些源文件需要反复使用，我们每次都需要将他们的名称写出来，这是非常低效的。cmake为我们提供了 set 指令来定义变量与设置宏。
语法：
    set(VARIABLE_NAME value [CACHE_TYPE [CACHE_VARIABLE]])
    解释：
        VARIABLE_NAME：变量的名称。
        value：为变量赋予的值。
        CACHE_TYPE（可选）：指定缓存变量的类型，如 FILEPATH、PATH、STRING、BOOL 等。
        CACHE_VARIABLE（可选）：如果指定，变量将被存储在 CMake 缓存中，而不是只限于当前的 CMakeLists.txt 文件。
示例：
    #定义一个变量SOURCE_FILE，存储源文件名。
    set(SOURCE_FILE main.cpp add.cpp sub.cpp div.cpp mul.cpp)
    如果要取变量中的值语法格式为：
    							${变量名}
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211165959770.png" alt="image-20250211165959770" style="zoom: 80%;" />

6.指定输出路径

```
	CMake为我们提供了一个宏EXECUTABLE_OUTPUT_PATH，我们可以通过设置这个宏指定输出路径。这里的输出路径支持相对路径与绝对路径。我们可以使用 set命令设置宏。
	例子：
        #定义一个变量存储路径,输出路径为上一级的bin目录
        set(OUTPATH  ../bin)
        #设置宏
        set(EXECUTABLE_OUTPUT_PATH ${OUTPATH})
    注意：如果输出路径中的子目录不存在，会自动生成。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211170906731.png" alt="image-20250211170906731" style="zoom:80%;" />

7.指定C++标准

```
	在CMake中想要指定C++标准有两种方式：通过set命令指定和在执行cmake指令时指定。
通过set命令指定：
	set(CMAKE_CXX_STANDARD 11)
执行cmake指令时指定：
	cmake .. -DCMAKE_CXX_STANDARD=11
```

8.搜索文件

```
	在上面的示例文件中只有五个源文件，如果有大量源文件，那么需要一个一个罗列出来十分繁琐。cmake中同样提供了搜索文件的命令 aux_source_directory 与 file 命令。
	
```

```
aux_source_directory 命令可以查找某个路径下的所有源文件，
语法：
    aux_source_directory(<directory> <variable>)
    解释：
        <directory>: 要搜索源文件的目录的路径。这可以是相对路径或绝对路径。
        <variable>: 用于存储找到的源文件列表的变量名。
示例：
    #搜索上一级目录的源文件
    aux_source_directory(.. SOURCE_FILE)
注意：
	CMAKE_CURRENT_SOURCE_DIR 是 CMake 中的一个预定义变量，它指向当前正在处理的 CMakeLists.txt 文件所在的目录。注意：如果使用相对路径，相对路径是相对于CMakeLists.txt 文件所在的目录，而非执行cmake命令的目录。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211172355552.png" alt="image-20250211172355552" style="zoom:80%;" />

```
file 命令用于对文件和目录进行操作，包括检查文件属性、读取和写入文件内容、复制文件、删除文件等。在这里我们只介绍一种用法搜索文件。语法：
    file(<GLOB/GLOB_RECURSE> <VARIABLE> <PATH>)
    解释：
        <GLOB/GLOB_RECURSE>选择非递归搜索(GLOB)还是递归搜索(GLOB_RECURSE)，递归搜索会搜索路径下的所有目录。
        <VARIABLE>存储搜索结果的变量。
        <PATH>搜索的路径与搜索的文件名。
    file使用相对路径时同样相对于CMakeLists.txt 文件所在的目录，而非执行cmake命令的目录。 
示例：
    #搜索CMakeLists.txt路径下所有源文件并存储在SOURCE_FILE
    file(GLOB SOURCE_FILE ./*.cpp)
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211172819019.png" alt="image-20250211172819019" style="zoom:80%;" />

9.包含头文件

```
	在我们调整了工程结构后头文件与源文件不在同一目录，我们又没有指定头文件搜素路径。所以找不到头文件。我们可以使用include_directories指定头文件搜索路径。
语法：
	include_directories([headpath])
示例：
	include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211173028728.png" alt="image-20250211173028728" style="zoom:80%;" />

10.生成动静态库

```
	在Linux中，静态库名字分为三部分：lib+库名+.a，命令需要指出的是中间部分，另外两部分在生成库文件时会自动补全。命令的第二个选项代表生成的是静态库（STATIC）还是动态库（SHARED）。
语法：
	add_library([库名称] SHARED/STATIC [源文件1] [源文件2] ...) 
示例：
	#生成一个名为libmymath.a的静态库
	add_library(mymath STATIC add.cpp sub.cpp mul.cpp div.cpp) 
	#生成一个名为libmymath.so的动态库
	add_library(mymath STATIC add.cpp sub.cpp mul.cpp div.cpp) 
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211173603761.png" alt="image-20250211173603761" style="zoom:80%;" />

11.指定库文件的输出路径

```
指定库文件的输出路径有两种方法：设置 EXECUTABLE_OUTPUT_PATH指定输出路径，设置 LIBRARY_OUTPUT_PATH指定输出路径。
注意：
	使用 EXECUTABLE_OUTPUT_PATH 指定输出路径只对动态库有效，因为Linux下生成的动态库默认是有执行权限的，而静态库没有。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211173822696.png" alt="image-20250211173822696" style="zoom:80%;" />

12.链接动静态库

```
cmake 链接库的命令为target_link_libraries 。target_link_libraries 可以链接动态库与静态库。
语法：
	target_link_libraries(<target>  <PRIVATE|PUBLIC|INTERFACE> <item>...)
解释：
    <target>：要链接库的目标名称，可以是可执行文件或库。
    <PRIVATE|PUBLIC|INTERFACE>：指定链接库的可见性：PRIVATE：链接库仅对当前目标有效，不会传递给依赖该目标的其他目标。PUBLIC：链接库对当前目标及其依赖者都有效，链接属性会传递给依赖该目标的其他目标。 INTERFACE：指定仅对依赖该目标的其他目标可见的接口链接库，不包括其实现细节。
    <item>...：一个或多个库的名称或目标名称，可以是库文件的路径、目标名称，或者是使用 find_package 或 find_library 找到的库名称。
    关于可见性问题可能不太好理解，我们举例说明。现在有以下CMake命令
例子：
    # 库A依赖B和C
    target_link_libraries(A PUBLIC B PUBLIC C)
    # 动态库D链接库A
    target_link_libraries(D PUBLIC A)
解释：
    在这个例子中：
        A链接了B和C，并且使用了PUBLIC关键字，所以任何链接到A的库（包括D）也会链接B和C。
        由于D链接了A，并且同样使用了PUBLIC关键字，D的任何依赖者也将链接A、B和C。
    如果将PUBLIC更改为PRIVATE或INTERFACE，链接行为将相应改变：
        使用PRIVATE，D将链接A，但D的依赖者不会链接A、B或C。
        使用INTERFACE，D将不会链接A的实际实现，但D的依赖者将能够使用A定义的接口。
注意：
    如果target_link_libraries 链接的是第三方库，需要用 link_directories 指定库所在的路径。
    语法：
    	link_directories(<libpath>)
```

13.日志

```
在CMake中，我们可以使用message命令记录日志或输出信息到控制台。这个命令允许输出不同级别的信息，包括普通消息、警告和错误。
语法：
	message([STATUS|WARNING|AUTHOR_WARNING|FATAL_ERROR|SEND_ERROR] "message")
解释：
    STATUS：显示状态消息，通常不是很重要。
    WARNING：显示警告消息，编译过程会继续执行。
    AUTHOR_WARNING：显示作者警告消息，用于开发过程中，编译过程会继续执行。
    FATAL_ERROR：显示错误消息，终止所有处理过程。
    SEND_ERROR：显示错误消息，但继续执行，会跳过生成步骤。
CMake的命令行工具会在stdout上显示STATUS消息，在stderr上显示其他所有消息。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211174814779.png" alt="image-20250211174814779" style="zoom:80%;" />

14.宏

```
在CMake脚本中定义条件编译宏 。命令为 add_definitions 。
语法：
    #定义宏
    add_definitions(-D宏名称)
    #定义宏并赋值
    add_definitions(-DDEBUG=1)
```

15.CMake的嵌套

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211175547495.png" alt="image-20250211175547495" style="zoom:80%;" />

```
	当我们的项目很大时，项目中会有很多的源码目录，如果只使用一个CMakeLists.txt，会比较复杂，我们可以给每个源码目录都添加一个CMakeLists.txt文件，这样每个文件都不会太复杂，而且更灵活，更容易维护。
	嵌套的CMake是一个树状结构，最顶层的 CMakeLists.txt是根节点，其次是子节点。我们需要使用 add_subdirectory()命令在结点间建立父子关系。
语法：
	add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])
解释：
    source_dir：要添加的子目录的路径，相对于当前 CMakeLists.txt 文件的路径。
    binary_dir（可选）：构建输出的目录，如果未指定，CMake 会使用 source_dir 作为构建目录。
    EXCLUDE_FROM_ALL（可选）：如果指定，该子目录的构建目标不会包含在 all 目标中，即默认情况下不会在调用 make 时构建。
    后两项我们通常用不到可以忽略，在建立关系后，父节点的变量可以被子节点继承，执行cmake命令时，也会一起处理。
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211175803375.png" alt="image-20250211175803375" style="zoom:80%;" />

16.条件判断与循环

```
变量的判断有以下关键字：DEFINED、EXISTS、IS_DIRECTORY。
    1.DEFINED:用于检查变量是否已经被定义。它不检查变量的值，只检查变量是否存在。
    例子：
        if(DEFINED MY_VARIABLE)
          message(STATUS "MY_VARIABLE is defined.")
        endif()
	2.EXISTS:用于检查文件或目录是否存在。接受一个路径作为参数，并返回一个布尔值。
	例子：
        if(EXISTS "${CMAKE_SOURCE_DIR}/somefile.txt")
          message(STATUS "The file somefile.txt exists.")
        endif()
    3.IS_DIRECTORY:用于检查给定的路径是否是一个目录。如果路径是一个存在的目录，返回布尔值。
    例子：
        if(IS_DIRECTORY "${CMAKE_SOURCE_DIR}/somedir")
          message(STATUS "The path somedir is a directory.")
        endif()
逻辑运算：
	AND(同C语言 && )：逻辑与。两个条件都必须为真，整个表达式才为真。
    OR(同C语言 || )：逻辑或。两个条件中至少有一个为真，整个表达式就为真。
    NOT(同C语言 ! )：逻辑非。反转条件的真假。
比较：
	数值比较:
        LESS <: 检查左侧是否小于右侧。
        GREATER >: 检查左侧是否大于右侧。
        EQUAL ==: 检查两侧是否数值相等。
        NOTEQUAL !=: 检查两侧是否数值不相等。
    字符串比较:
        STRLESS: 字符串是否字典序较小。
        STRGREATER: 字符串是否字典序较大。
        STREQUAL: 字符串是否相等。
        NOT STREQUAL: 字符串是否不相等。
算术运算：
	加法：
    	set(counter 1) math(EXPR counter "${counter} + 1") # counter 现在是 2
    减法：
    	set(counter 5) math(EXPR counter "${counter} - 2") # counter 现在是 3
    乘法：
    	set(counter 3) math(EXPR counter "${counter} * 2") # counter 现在是 6
    除法：
    	set(counter 20) math(EXPR counter "${counter} / 4") # counter 现在是 5
    模运算：
    	set(counter 7) math(EXPR counter "${counter} % 3") # counter 现在是 1
    使用变量：
        set(a 10) 
        set(b 3) 
        math(EXPR result "${a} * ${b}") # result 是 30
循环：
    1.foreach循环的基本语法如下：
        foreach(<variable> IN <list>)
            # 命令
        endforeach()
    2.while循环比较简单，只需要指定出循环结束的条件。
        while(<condition>)
            # 命令序列
        endwhile()
```

<img src="C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250211180717284.png" alt="image-20250211180717284" style="zoom:80%;" />



