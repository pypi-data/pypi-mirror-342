#ifdef _WIN32
  #ifdef BUILDING_DATETIME
    #define DATETIME_API __declspec(dllexport)
  #else
    #define DATETIME_API __declspec(dllimport)
  #endif
#else
  #define DATETIME_API
#endif

#ifndef __DATETIME_H__
#define __DATETIME_H__
#include <stdio.h>
#include <stdlib.h>

#define LIBDATETIME_VERSION_MAJOR 1
#define LIBDATETIME_VERSION_MINOR 0
#define LIBDATETIME_VERSION_PATCH 0


#ifdef __cplusplus
extern "C" {
#endif
/* C functions */

/***********************************************************************
 * NAME : 		void ContUT(n,Date,ut,utc)
 * 
 * DESCRIPTION : 	Calculates the continuous time in hours since 00:00
 * 					on 19500101 for an array of dates and times. NOTE:
 * 					This algorithm will probably work best if dates and 
 * 					times are arranges in chronological order.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			int		Date		Date array
 * 			float	ut			Time array in decimal hours
 *
 * OUTPUTS :
 * 			double 	*utc		Continuous time in hours since 00:00 on
 * 								19500101
 * 
 * ********************************************************************/
void ContUT(int n, int *Date, float *ut, double *utc);

/***********************************************************************
 * NAME : 		void ContUTtoDate(n,Date,ut,utc)
 * 
 * DESCRIPTION : 	Calculates the date and time from the continuous
 * 					time given by ContUT,
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			double 	*utc		Continuous time in hours since 00:00 on
 * 								19500101
 *
 * OUTPUTS :
 * 			int		Date		Date array
 * 			float	ut			Time array in decimal hours
 * 
 * ********************************************************************/
void ContUTtoDate(int n, double *utc, int *Date, float *ut);

/***********************************************************************
 * NAME : 			int DateDifference(Date0,Date1)
 * 
 * DESCRIPTION : 	Calculates the number of whole days between two 
 * 					dates e.g. 
 * 					dd = DateDifference(20120101,20120103)
 * 					returns dd == 2
 * 
 * INPUTS : 
 * 			int		Date0		Starting date
 * 			int 	Date1		Ending date
 *
 * OUTPUTS :
 *  		int		ndays		Number of days from Date0 to Date1
 * 
 * ********************************************************************/
int DateDifference(int Date0, int Date1);

/***********************************************************************
 * NAME : 			void DateJoin(n,year,month,day,Date)
 * 
 * DESCRIPTION : 	Join year month and day to a single dat integer in 
 * 					the format yyyymmdd.
 * 
 * INPUTS : 
 * 			int		n		Number of elements
 * 			int		*year	Integer years
 * 			int		*month	Integer months
 * 			int		*day	Integer days
 *
 * OUTPUTS :
 * 			int		*Date	Integer dates in format yyyymmdd
 * 
 * ********************************************************************/
void DateJoin(int n, int *year, int *month, int *day, int *Date);

/***********************************************************************
 * NAME : 			void DateSplit(n,Date,year,month,day)
 * 
 * DESCRIPTION : 	Convert an array of dates in the format yyyymmdd to 
 * 					separate integers: year, month and day
 * 
 * INPUTS : 
 * 			int 	n
 * 			int		*Date	Integer date in format yyyymmdd
 *
 * OUTPUTS :
 * 			int		*year	Integer year
 * 			int		*month	Integer month
 * 			int		*day	Integer day
 * 
 * ********************************************************************/
void DateSplit(int n, int *Date, int *year, int *month, int *day);



/***********************************************************************
 * NAME : 			void DayNo(n,Date,Year,DayNo)
 * 
 * DESCRIPTION : 	Work out the day numbers for an array of dates.
 * 
 * INPUTS : 
 * 			int		n		Number of dates
 * 			int		*Date	Integer dates in format yyyymmdd
 *
 * OUTPUTS :
 * 			int		*Year	output years
 * 			int		*DayNo	output day numbers
 * 
 * ********************************************************************/
void DayNo(int n, int *Date, int *Year, int *DayNo);

/***********************************************************************
 * NAME : 			void DayNotoDate(n,Year,DayNo,Date)
 * 
 * DESCRIPTION : 	Converts year and day number to dates in the format
 * 					yyyymmdd
 * 
 * INPUTS : 
 * 			int		n		Number of dates
 * 			int		*Year	years
 * 			int		*DayNo	day numbers
 *
 * OUTPUTS :
 *  		int		*Date	Integer dates in format yyyymmdd
 * 
 * ********************************************************************/
void DayNotoDate(int n, int *Year, int *Doy, int *Date);


/***********************************************************************
 * NAME : 			void DectoHHMM(n,ut,hh,mm,ss,ms)
 * 
 * DESCRIPTION : 	Convert decimal hours to hours, minutes etc
 * 
 * INPUTS : 
 * 			int 	n		Number of elements in ut
 * 			double	*ut		Time array in decimal hours
 *
 * OUTPUTS :
 * 			int		*hh		hours
 * 			int		*mm		minutes
 * 			int		*ss		seconds
 * 			double	*ms		milliseconds
 * 
 * ********************************************************************/
void DectoHHMM(int n, double *ut, int *hh, int *mm, int *ss, double *ms);

/***********************************************************************
 * NAME : 			void HHMMtoDec(n,hh,mm,ss,ms,dec)
 * 
 * DESCRIPTION : 	Convert time in hours minutes etc to decimal hours
 * 
 * INPUTS : 
 * 			int 	n		Number of elements
 * 			double	*hh		hours
 * 			double		*mm		minutes
 * 			double		*ss		seconds
 * 			double	*ms		milliseconds
 *
 * OUTPUTS :
 * 			double	*ut		Time array in decimal hours
 * 
 * ********************************************************************/
void HHMMtoDec(int n, double *hh, double *mm, double *ss, double *ms, double *ut);

/***********************************************************************
 * NAME : 		void JulDay(n,Date,ut,JD)
 * 
 * DESCRIPTION : 	Calculates the Julian date from a date and time.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			int		Date		Date array
 * 			float	ut			Time array in decimal hours
 *
 * OUTPUTS :
 * 			double 	*JD			Julian date.
 * 
 * ********************************************************************/
void JulDay(int n, int *Date, float *ut, double *JD);

/***********************************************************************
 * NAME : 		void JulDaytoDate(n,JD,Date,ut)
 * 
 * DESCRIPTION : 	Calculates the date from a Julian date and time.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			double 	*JD			Julian date.
 *
 * OUTPUTS :
 * 			int		*Date		Date array
 * 			float	*ut			Time array in decimal hours 			
 * 
 * ********************************************************************/
void JulDaytoDate(int n, double *JD, int *Date, float *ut);

/***********************************************************************
 * NAME : 			void LeapYear(n,year,ly)
 * 
 * DESCRIPTION : 	Determine whether a year is a leap year
 * 
 * INPUTS : 
 * 			int 	n		Number of elements
 * 			int		*year	Array of years
 *
 * OUTPUTS :
 * 			bool	*ly		Array of boolean (true if is a leap year)
 * 
 * ********************************************************************/
void LeapYear(int n, int *year, bool *ly);

/***********************************************************************
 * NAME : 		void MidTime(Date0,ut0,Date1,ut1,Datem,utm)
 * 
 * DESCRIPTION : 	Calculates the midpoint between two times.
 * 
 * INPUTS : 
 * 			int		Date0		Starting date
 * 			float	ut0			Starting time in decimal hours
 * 			int 	Date1		Ending date
 * 			float 	ut1			Ending time in decimal hours
 *
 * OUTPUTS :
 * 			int		*Datem		Midpoint date
 * 			float	*utm		Midpoint time in decimal hours
 * 
 * ********************************************************************/
void MidTime(int Date0, float ut0, int Date1, float ut1, int *Datem, float *utm);

/***********************************************************************
 * NAME : 			int MinusDay(Date)
 * 
 * DESCRIPTION : 	Given a date in the format yyyymmdd, subtract a 
 * 					single day.
 * 
 * INPUTS : 
 * 			int		Date	Integer date in format yyyymmdd
 *
 * RETURNS :
 * 			int		Date	The day before the input date.
 * 
 * ********************************************************************/
int MinusDay(int Date);

/***********************************************************************
 * NAME : 		int NearestTimeIndex(n,Date,ut,TestDate,Testut)
 * 
 * DESCRIPTION : 	Locates the index of the closest time/date.
 * 
 * INPUTS : 
 * 			int		n			Total number of elements
 * 			int		*Date		Date array in the format yyyymmdd
 * 			float	*ut			UT array, in decimal hours
 * 			int		TestDate	The date we are looking for
 * 			float 	Testut		The time we are looking for
 *
 *
 * RETURNS :
 * 			int		I			Index of the Date/ut arrays which is the
 * 								closest time.
 * 
 * ********************************************************************/
int NearestTimeIndex(int n, int *Date, float *ut, int TestDate, float Testut);

/***********************************************************************
 * NAME : 			int PlusDay(Date)
 * 
 * DESCRIPTION : 	Given a date in the format yyyymmdd, add a 
 * 					single day.
 * 
 * INPUTS : 
 * 			int		Date	Integer date in format yyyymmdd
 *
 * RETURNS :
 * 			int		Date	The day after the input date.
 * 
 * ********************************************************************/
int PlusDay(int Date);

/***********************************************************************
 * NAME : 			float TimeDifference(Date0,ut0,Date1,ut1)
 * 
 * DESCRIPTION : 	Calculates the number of days between two times
 * 					(result in days)
 * 
 * INPUTS : 
 * 			int		Date0		Starting date
 * 			float	ut0			Starting time in decimal hours
 * 			int 	Date1		Ending date
 * 			float 	ut1			Ending time in decimal hours
 *
 * RETURNS :
 *  		float	ndays		Number of days between start and end times
 * 
 * ********************************************************************/
float TimeDifference(int Date0, float ut0, int Date1, float ut1);

/***********************************************************************
 * NAME : 		void UnixTime(n,Date,ut,unixt)
 * 
 * DESCRIPTION : 	Calculates the unix time in seconds since 00:00
 * 					on 19700101 for an array of dates and times. NOTE:
 * 					This algorithm will probably work best if dates and 
 * 					times are arranges in chronological order.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			int		Date		Date array
 * 			float	ut			Time array in decimal hours
 *
 * OUTPUTS :
 * 			double 	*unix		Unix time in seconds since 19700101
 * 
 * ********************************************************************/
void UnixTime(int n, int *Date, float *ut, double *unixt);

/***********************************************************************
 * NAME : 		void UnixTimetoDate(n,Date,ut,unixt)
 * 
 * DESCRIPTION : 	Calculates the date and time from the unix
 * 					time given by ContUT,
 * INPUTS : 
 * 			int 	n			Number of elemenets in Date/ut arrays
 * 			double 	*utc		Unix time in hours since 00:00 on
 * 								19700101
 *
 * OUTPUTS :
 * 			int		Date		Date array
 * 			float	ut			Time array in decimal hours
 * 
 * ********************************************************************/
void UnixTimetoDate(int n, double *unixt, int *Date, float *ut);

/***********************************************************************
 * NAME : 		int WithinTimeRange(n,Date,ut,Date0,ut0,Date1,ut1,ni,ind)
 * 
 * DESCRIPTION : 	Locates the indices of all of the times within a 
 * 					defined time range.
 * 
 * INPUTS : 
 * 			int		n			Total number of elements
 * 			int		*Date		Date array in the format yyyymmdd
 * 			float	*ut			UT array, in decimal hours
 * 			int		Date0		Start date
 * 			float 	ut0			Start time
 * 			int		Date1		End date
 * 			float 	ut1			End time
 *
 *
 * OUTPUTS :
 * 			int		*ni			Number of elements within range
 * 			int 	*ind		Array of indices
 * 
 * ********************************************************************/
void WithinTimeRange(int n, int *Date, float *ut, 
						int Date0, float ut0,
						int Date1, float ut1,
						int *ni, int *ind);

#ifdef __cplusplus
}

/* C++ Only functions */

/***********************************************************************
 * NAME : 		void BubbleSort(n,x,y)
 * 
 * DESCRIPTION : 	Uses the buble sort algorithm to sort an array. NOTE
 * 					the datatype T is a tmeplate for all data types,
 * 					so it should accept int, float, double etc.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets
 * 			T		x			Array to be sorted
 *
 * OUTPUTS :
 * 			T		y			Sorted array
 * 
 * 
 * ********************************************************************/
/* create a template for a data type so that we can accept any data type */
template <typename T>
void BubbleSort(int n, T *x, T *y) {
	
	bool swapped = true;
	int i, p;
	T tmp;
	
	/* copy each element of x into y */
	for (i=0;i<n;i++) {
		y[i] = x[i];
	}	
	
	/* Check that we have enough elements for there not to be a 
	 * segmentation fault */
	if (n < 2) {
		return;
	}
	
	/* start sorting by swapping elements */
	p = n;
	while (swapped) {
		swapped = false;
		for (i=1;i<p;i++) {
			if (y[i-1] > y[i]) {
				/* swap */
				tmp = y[i];
				y[i] = y[i-1];
				y[i-1] = tmp;
				swapped = true;

			}
		}
		p--;
	}
}


/***********************************************************************
 * NAME : 			double GetYearUTC(Year)
 * 
 * DESCRIPTION : 	Get the utc at the beginning of a year.
 * 
 * INPUTS : 
 * 			int		Year	Year, obviously
 *
 * RETURNS :
 * 			double	utc		Continuous time at the start of the year
 * 
 * ********************************************************************/
double GetYearUTC(int Year);

/***********************************************************************
 * NAME : 		void PopulateYearUTC()
 * 
 * DESCRIPTION : 	Calculates the continuous time in hours since 00:00
 * 					on 19500101 for all years between 1950 and 2050
 * 
 * ********************************************************************/
void PopulateYearUTC();

/***********************************************************************
 * NAME : 			int JoinDate(year,month,day,Date)
 * 
 * DESCRIPTION : 	Join year month and day to a single dat integer in 
 * 					the format yyyymmdd.
 * 
 * INPUTS : 
 * 			int		year	Integer year
 * 			int		month	Integer month
 * 			int		day	Integer day
 *
 * RETURNS :
 * 			int		*Date	Integer date in format yyyymmdd
 * 
 * ********************************************************************/
int JoinDate(int year, int month, int day);

/***********************************************************************
 * NAME : 			void SplitDate(Date,year,month,day)
 * 
 * DESCRIPTION : 	Convert a date of the format yyyymmdd to separate
 * 					integers: year, month and day
 * 
 * INPUTS : 
 * 			int		Date	Integer date in format yyyymmdd
 *
 * OUTPUTS :
 * 			int		*year	Integer year
 * 			int		*month	Integer month
 * 			int		*day	Integer day
 * 
 * ********************************************************************/
void SplitDate(int Date, int *year, int *month, int *day);

/***********************************************************************
 * NAME : 			void Unique(n,x,nu,ux)
 * 
 * DESCRIPTION : 	Get a list of the unique values in an array.
 * 
 * INPUTS : 
 * 			int		n		Number of elements
 * 			T 		*x		Array of values
 *
 * OUTPUTS :
 * 			int		*nu		Number of unique dates found
 * 			T		*ux		Array of unique values from x
 * 
 * ********************************************************************/
template <typename T>
void Unique(int n, T *x, int *nu, T *ux) {
	
	int i, p;
	p = 0;
	T pVal = 0;
	
	/* sort the dates first */
	T *sx = new T[n];
	BubbleSort(n,x,sx);
	
	/* loop through sorted dates, adding a new one to the unique array
	 * when a differnet on is found */
	for (i=0;i<n;i++) {
		if ((sx[i] != pVal) || (i == 0)) {
			ux[p] = sx[i];
			pVal = sx[i];
			p++;
		}
	}
	nu[0] = p;
	
	/* delete the sorted array */
	delete[] sx;	
		
	
}



/***********************************************************************
 * NAME : 		void PopulateYearUnixT()
 * 
 * DESCRIPTION : 	Calculates the unix time in hours since 00:00
 * 					on 19700101 for all years between 1950 and 2050
 * 
 * ********************************************************************/
void PopulateYearUnixT();

/***********************************************************************
 * NAME : 			double GetYearUTC(Year)
 * 
 * DESCRIPTION : 	Get the unix time at the beginning of a year.
 * 
 * INPUTS : 
 * 			int		Year	Year, obviously
 *
 * RETURNS :
 * 			double	unixt	Continuous time at the start of the year
 * 
 * ********************************************************************/
double GetYearUnixT(int Year);

/***********************************************************************
 * NAME : 		void WhereEq(n,x,y,ni,ind)
 * 
 * DESCRIPTION : 	Scan through an arra, x, for instances where it is 
 * 					equal to y.
 * 
 * INPUTS : 
 * 			int 	n			Number of elemenets
 * 			T		*x			Array to be scanned
 * 			T 		y			value to test
 *
 * OUTPUTS :
 * 			int		*ni			Number of indices
 * 			int		*ind		Array of indices
 * 
 * 
 * ********************************************************************/
/* create a template for a data type so that we can accept any data type */
template <typename T>
void WhereEq(int n, T *x, T y, int *ni, int *ind) {
	
	int i,p;
	p = 0;
	for (i=0;i<n;i++) {
		if (y == x[i]) {
			ind[p] = i;
			p++;
		}
	}
	ni[0] = p;
}
	


#endif


#endif
