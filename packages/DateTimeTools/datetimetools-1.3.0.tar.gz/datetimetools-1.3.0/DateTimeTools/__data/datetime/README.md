# datetime
A C++ library contianing some time-related tools.

## Installation

This library requires GNU-make and g++ to be built in Linux and Mac. In Windows, I use TDM-GCC to provide the C++ compiler.

Clone the repo:

```bash
git clone https://github.com/mattkjames7/datetime.git
cd datetime
```

For Linux or Mac:
```bash
# configure the build (default)
cmake -DCMAKE_INSTALL_PREFIX=/usr/local -B build

# or with tests
cmake -DCMAKE_INSTALL_PREFIX=/usr/local -B build -DBUILD_TESTING=true

# build the library
cmake --build build

# run tests (if built)
./build/tests/test_datetime
./build/tests/test_c

# install globally
sudo cmake --install build

# uninstall
cmake --build build --target uninstall
```

And for Windows (Visual Studio):
```powershell
# Configure the build (default)
cmake -DCMAKE_INSTALL_PREFIX="C:/install/dir" -B build -G "Visual Studio 17 2022"

# or with tests
cmake -DCMAKE_INSTALL_PREFIX="C:/install/dir" -DBUILD_TESTING=ON -B build -G "Visual Studio 17 2022"

# Build the library 
cmake --build build

# Run tests (if built)
.\build\tests\Release\test_datetime.exe
.\build\tests\Release\test_c.exe

# Install globally (run in elevated shell)
cmake --install build

# Uninstall
cmake --build build --target uninstall
```
or (MinGW):
```powerhsell
cmake -DCMAKE_INSTALL_PREFIX="C:/install/dir" -G "MinGW Makefiles" -B build
cmake --build build
cmake --install build
```

<details>
<summary> Old Build Instructions </summary>

For Linux or Mac:
```bash
#build the library
make

#optionally install globally
sudo make install
```

For Windows:
```cmd
> compile.bat
```
</details>

## Linking
 
To link to this library in C or C++, you should include the header for the library:
```cpp
#include <datetime.h>
```
then link to the library, e.g.:
```bash
#when installed globally
g++ $(CFLAGS) main.cc -o main -ldatetime

#otherwise
g++ $(CFLAGS) -I/path/to/header/ main.cc -o main -L/path/to/lib -ldatetime
```

## Testing

To check that all of the functions are working as expected, run the following tests in Linux/Mac:

```bash
make test
```
or in Windows:
```cmd
> test.bat
```

If the library has been installed globally then the following test will check that linking can be done to the globally installed lib/header:
```bash
make testinstall
```

## Summary of Functions

| Name | Description |
|:-----|:------------|
| [`ContUT()`](include/datetime.h#L34) | Converts Date and UT to a continuous value of hours since 19500101 00:00/ |
| [`ContUTtoDate()`](include/datetime.h#L51) | Converts output of `ContUT()` back to date and time. |
| [`DateDifference()`](include/datetime.h#L69) | Find the number of days between two dates. |
| [`DateJoin()`](include/datetime.h#L87) | Join the individual elements of a date (year, month and day) to a single integer with the format _yyyymmdd_. |
| [`DateSplit()`](include/datetime.h#L105) | Split the date integer into year, month and day. |
| [`DayNo()`](include/datetime.h#L123) | Converts a date of the format _yyyymmdd_ to year and day number. |
| [`DayNotoDate()`](include/datetime.h#L140) | Converts year and day number to a date with the format _yyyymmdd_. |
| [`DectoHHMM()`](include/datetime.h#L159) | Converts the time in decimal hours to hours, minutes, seconds and milliseconds. |
| [`HHMMtoDec()`](include/datetime.h#L177) | Converts hours, minutes, seconds and milliseconds to decimal hours. |
| [`JulDay()`](include/datetime.h#L193) | Converts a date and time to Julian day. |
| [`JulDaytoDate()`](include/datetime.h#L209) | Converts Julian day to date and time. |
| [`LeapYear()`](include/datetime.h#L224) | Determines whether a year is a leap year or not. |
| [`MidTime()`](include/datetime.h#L242) | Works out the time and date exactly in the middle of two dates/times. |
| [`MinusDay()`](include/datetime.h#L257) | Subtracts one day off a date. |
| [`NearestTimeIndex()`](include/datetime.h#L277) | Finds the index of a time array closest to a given date/time. |
| [`PlusDay()`](include/datetime.h#L292) | Adds a day onto a date. |
| [`TimeDifference()`](include/datetime.h#L310) | Calculates the time difference(in days) between two dates/times. |
| [`UnixTime()`](include/datetime.h#L329) | Calculate the Unix time given a date and time. |
| [`UnixTimetoDate()`](include/datetime.h#L346) | Convert Unix time back to date and UT. |
| [`WithinTimeRange()`](include/datetime.h#L369) | Find the indices of a time array which lie within two dates/times. |

