call compileobj.bat

mkdir ..\lib
g++ -lm -fPIC -std=c++17 -Wextra -O3 ..\build\*.o -shared -o ..\lib\libdatetime.dll
