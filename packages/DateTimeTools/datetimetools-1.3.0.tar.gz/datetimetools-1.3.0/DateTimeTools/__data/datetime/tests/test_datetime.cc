#include <datetime.h>
#include <gtest/gtest.h>

TEST(DateTimeTests, MidTimeCalculation) {
    int Date0 = 20010324;
    int Date1 = 20020324;
    float ut0 = 3.0;
    float ut1 = 12.0;
    int Datem;
    float utm;

    MidTime(Date0, ut0, Date1, ut1, &Datem, &utm);

    EXPECT_EQ(Datem, 20010922);
    EXPECT_FLOAT_EQ(utm, 19.5);
}

TEST(DateTimeTests, TestMinusDay) {
    int Date = 20040301;
    Date = MinusDay(Date);

    EXPECT_EQ(Date, 20040229);
}


TEST(DateTimeTests, TestAddDay) {
    int Date = 20040228;
    Date = PlusDay(Date);

    EXPECT_EQ(Date, 20040229);
}


TEST(DateTimeTests, FindNearestTimeIndex) {
	int Date[] = {20010101,20010101,20010103,20010104};
	float ut[] = {12.0,23.0,15.0,4.0};
	int testDate = 20010102;
	float testUt = 3.0;

    int ind = NearestTimeIndex(4,Date,ut,testDate,testUt);

    EXPECT_EQ(ind, 1);
}

TEST(DateTimeTests, CalculateTimeDifference) {
    int Date0 = 20010324;
    int Date1 = 20020324;
    float ut0 = 3.0;
    float ut1 = 12.0;
    float dt;
    dt = TimeDifference(Date0,ut0,Date1,ut1);

    EXPECT_FLOAT_EQ(dt, 365.375);
}

TEST(DateTimeTests, UniqueFunction) {

    float x[] = {1.0,2.0,2.3,4.2,4.2,6.3,6.3};
    float expected[] = {1.0,2.0,2.3,4.2,6.3};
    int nu;
    float ux[7];

    Unique(7,x,&nu,ux);

    ASSERT_EQ(nu, 5);  // Confirm correct number of unique elements
    for (int i = 0; i < nu; ++i) {
        EXPECT_FLOAT_EQ(ux[i], expected[i]);
    }
}

TEST(DateTimeTests, DateToUnixTime) {
	int Date;
	float ut;
	double unixt;

	Date = 20010405;
	ut = 19.0;
	UnixTime(1,&Date,&ut,&unixt);

    EXPECT_FLOAT_EQ(unixt, 986497200.0);
}

TEST(DateTimeTests, UnixTimeToDate) {
	int Date;
	float ut;
	double unixt;

    unixt = 986497200.0;
	UnixTimetoDate(1,&unixt,&Date,&ut);

    EXPECT_EQ(Date, 20010405);
    EXPECT_FLOAT_EQ(ut, 19.0);
}

TEST(DateTimeTests, TestWhereEqual) {
	double x[] = {1.0,4.0,2.0,4.0,1.0,2.0,2.0};
	int ni;
	int ind[7];
	int test[] = {2,5,6};

    WhereEq(7,x,2.0,&ni,ind);
    ASSERT_EQ(ni, 3);
    for (int i=0; i<ni; i++) {
        EXPECT_EQ(ind[i], test[i]);
    }
}

TEST(DateTimeTests, TestWithin) {

	int Date[] = {20010101,20010101,20010103,20010104,20010105};
	float ut[] = {12.0,23.0,15.0,4.0,12.0};
	int Date0 = 20010102;
	float ut0 = 12.0;
	int Date1 = 20010105;
	float ut1 = 6.0;

	int ni, i;
	int ind[5];
	int test[] = {2,3};

	WithinTimeRange(5,Date,ut,Date0,ut0,Date1,ut1,&ni,ind);
    ASSERT_EQ(ni, 2);
    for (int i=0; i<ni; i++) {
        EXPECT_EQ(ind[i], test[i]);
    }
}

TEST(DateTimeTests, TestLeapYear) {
	bool ly;
	int year;

	year = 2001;
	LeapYear(1,&year,&ly);
	EXPECT_FALSE(ly);

	year = 2004;
	LeapYear(1,&year,&ly);
    EXPECT_TRUE(ly);
}

TEST(DateTimeTests, DateToJulDay) {
	double jd;
	int Date;
	float ut;

	Date = 20041230;
	ut = 12.0;
	JulDay(1,&Date,&ut,&jd);
	ASSERT_FLOAT_EQ(jd, 2453370.0);
}

TEST(DateTimeTests, JulDayToDate) {
	double jd;
	int Date;
	float ut;

	jd = 2413370.0;
	JulDaytoDate(1,&jd,&Date,&ut);
	EXPECT_EQ(Date,18950625);
    EXPECT_FLOAT_EQ(ut,12.0);
}

TEST(DateTimeTests, HoursToHHMM) {
	double ut, ms;
	int hh, mm, ss;

	ut = 22.25;
	DectoHHMM(1,&ut,&hh,&mm,&ss,&ms);
    EXPECT_EQ(hh, 22);
    EXPECT_EQ(mm, 15);
    EXPECT_EQ(ss, 0);
    EXPECT_EQ(ms, 0);   
}

TEST(DateTimeTests, HHMMToHours) {
    double ut;
    double hh, mm, ss, ms;
    hh = 22;
    mm = 15;
    ss = 0;
    ms = 0;

    HHMMtoDec(1,&hh,&mm,&ss,&ms,&ut);

    ASSERT_FLOAT_EQ(ut, 22.25);
}

TEST(DateTimeTests, TestDayNo) {

	int Date, Year, Doy;
	
	Date = 20010324;
	DayNo(1,&Date,&Year,&Doy);
    EXPECT_EQ(Year, 2001);
    EXPECT_EQ(Doy, 83);

	DayNotoDate(1,&Year,&Doy,&Date);
    EXPECT_EQ(Date, 20010324);

}

TEST(DateTimeTests, TestDateSplit) {
	int Date, year, month, day;
	Date = 20010503;
	DateSplit(1,&Date,&year,&month,&day);

    EXPECT_EQ(year, 2001);
    EXPECT_EQ(month, 5);
    EXPECT_EQ(day, 3);
}

TEST(DateTimeTests, TestDateJoin) {
	int Date, year, month, day;
	year = 2001;
	month = 12;
	day = 1;
	DateJoin(1,&year,&month,&day,&Date);

    EXPECT_EQ(Date, 20011201);
}

TEST(DateTimeTests, TestBubbleSort) {
	float arr0[] = {6.0,2.3,1.2,4.5,9.9};
	float arr1[5];
	float test[] = {1.2,2.3,4.5,6.0,9.9};

	BubbleSort(5,arr0,arr1);
    
    for (int i=0;i<5;i++) {
        EXPECT_EQ(arr1[i],test[i]);
    }
}

TEST(DateTimeTests, DateToContUT) {
	int Date;
	float ut;
	double utc;

	Date = 19500101;
	ut = 0.0;
	ContUT(1,&Date,&ut,&utc);
	EXPECT_FLOAT_EQ(utc, 0.0);

	Date = 20000101;
	ut = 0.0;
	ContUT(1,&Date,&ut,&utc);
	EXPECT_FLOAT_EQ(utc, 438288.0);
}

TEST(DateTimeTests, ContUTToDate) {
	int Date;
	float ut;
	double utc;

	utc = 0.0;
	ContUTtoDate(1,&utc,&Date,&ut);
    EXPECT_EQ(Date, 19500101);
    EXPECT_FLOAT_EQ(ut, 0.0);

	utc = 438288.0;
	ContUTtoDate(1,&utc,&Date,&ut);
    EXPECT_EQ(Date, 20000101);
    EXPECT_FLOAT_EQ(ut, 0.0);

	Date = 19960923;
	ut = 17.5;
	ContUT(1,&Date,&ut,&utc);
	ContUTtoDate(1,&utc,&Date,&ut);
    EXPECT_EQ(Date, 19960923);
    EXPECT_FLOAT_EQ(ut, 17.5);

}

TEST(DateTimeTests, DateDiff) {
    int diff = DateDifference(19950101,20220324);
    ASSERT_EQ(diff, 9944);
}