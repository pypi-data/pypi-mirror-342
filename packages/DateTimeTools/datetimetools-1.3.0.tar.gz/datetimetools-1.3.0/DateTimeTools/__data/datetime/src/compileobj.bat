mkdir ../build


g++ -c -O3 -std=c++17 -Wextra -fPIC hhmm.cc -o ..\build\hhmm.o
g++ -c -O3 -std=c++17 -Wextra -fPIC LeapYear.cc -o ..\build\LeapYear.o
g++ -c -O3 -std=c++17 -Wextra -fPIC DateSplit.cc -o ..\build\DateSplit.o
g++ -c -O3 -std=c++17 -Wextra -fPIC DateJoin.cc -o ..\build\DateJoin.o
g++ -c -O3 -std=c++17 -Wextra -fPIC DayNo.cc -o ..\build\DayNo.o
g++ -c -O3 -std=c++17 -Wextra -fPIC PlusDay.cc -o ..\build\PlusDay.o
g++ -c -O3 -std=c++17 -Wextra -fPIC MinusDay.cc -o ..\build\MinusDay.o
g++ -c -O3 -std=c++17 -Wextra -fPIC DateDifference.cc -o ..\build\DateDifference.o
g++ -c -O3 -std=c++17 -Wextra -fPIC TimeDifference.cc -o ..\build\TimeDifference.o
g++ -c -O3 -std=c++17 -Wextra -fPIC MidTime.cc -o ..\build\MidTime.o
g++ -c -O3 -std=c++17 -Wextra -fPIC ContUT.cc  -o ..\build\ContUT.o
g++ -c -O3 -std=c++17 -Wextra -fPIC UnixTime.cc -o ..\build\UnixTime.o
g++ -c -O3 -std=c++17 -Wextra -fPIC NearestTimeIndex.cc -o ..\build\NearestTimeIndex.o
g++ -c -O3 -std=c++17 -Wextra -fPIC WithinTimeRange.cc -o ..\build\WithinTimeRange.o
g++ -c -O3 -std=c++17 -Wextra -fPIC JulDay.cc -o ..\build\JulDay.o
g++ -c -O3 -std=c++17 -Wextra -fPIC JulDaytoDate.cc -o ..\build\JulDaytoDate.o
