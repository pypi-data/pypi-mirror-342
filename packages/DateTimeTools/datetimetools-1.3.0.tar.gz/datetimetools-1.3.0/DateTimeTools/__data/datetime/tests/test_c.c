#include <check.h>
#include <stdbool.h>
#include <math.h>
#include "datetime.h"

#define EPSILON 1e-6

START_TEST(test_midtime)
{
    int Date0 = 20010324, Date1 = 20020324, Datem;
    float ut0 = 3.0, ut1 = 12.0, utm;

    MidTime(Date0, ut0, Date1, ut1, &Datem, &utm);

    ck_assert_int_eq(Datem, 20010922);
    ck_assert(fabs(utm - 19.5) < EPSILON);
}
END_TEST

START_TEST(test_minus_day)
{
    int Date = 20040301;
    Date = MinusDay(Date);
    ck_assert_int_eq(Date, 20040229);
}
END_TEST

START_TEST(test_time_index)
{
    int Date[] = {20010101, 20010101, 20010103, 20010104};
    float ut[] = {12.0, 23.0, 15.0, 4.0};
    int tDate = 20010102;
    float tut = 3.0;

    int ind = NearestTimeIndex(4, Date, ut, tDate, tut);
    ck_assert_int_eq(ind, 1);
}
END_TEST

START_TEST(test_plus_day)
{
    int Date = 20040228;
    Date = PlusDay(Date);
    ck_assert_int_eq(Date, 20040229);
}
END_TEST

START_TEST(test_time_diff)
{
    int Date0 = 20010324, Date1 = 20020324;
    float ut0 = 3.0, ut1 = 12.0;
    float dt = TimeDifference(Date0, ut0, Date1, ut1);
    ck_assert(fabs(dt - 365.375) < EPSILON);
}
END_TEST

START_TEST(test_unix_time)
{
    int Date = 20010405;
    float ut = 19.0;
    double unixt;

    UnixTime(1, &Date, &ut, &unixt);
    ck_assert(fabs(unixt - 986497200.0) < EPSILON);

    UnixTimetoDate(1, &unixt, &Date, &ut);
    ck_assert_int_eq(Date, 20010405);
    ck_assert(fabs(ut - 19.0) < EPSILON);
}
END_TEST

START_TEST(test_within)
{
    int Date[] = {20010101, 20010101, 20010103, 20010104, 20010105};
    float ut[] = {12.0, 23.0, 15.0, 4.0, 12.0};
    int Date0 = 20010102, Date1 = 20010105;
    float ut0 = 12.0, ut1 = 6.0;
    int ind[5], ni;
    int expected[] = {2, 3};

    WithinTimeRange(5, Date, ut, Date0, ut0, Date1, ut1, &ni, ind);

    ck_assert_int_eq(ni, 2);
    ck_assert_int_eq(ind[0], expected[0]);
    ck_assert_int_eq(ind[1], expected[1]);
}
END_TEST

START_TEST(test_leap_year) 
{
    int year;
    bool ly;

    year = 2001;
    LeapYear(1,&year,&ly);
    ck_assert(!ly);

    year = 2004;
    LeapYear(1,&year,&ly);
    ck_assert(ly);
}
END_TEST

START_TEST(test_jul_day)
{
	double jd;
	int Date;
	float ut;

	Date = 20041230;
	ut = 12.0;
	JulDay(1,&Date,&ut,&jd);
    ck_assert_double_eq(jd,2453370.0);

	jd = 2413370.0;
	JulDaytoDate(1,&jd,&Date,&ut);
    ck_assert_int_eq(Date, 18950625);
    ck_assert_float_eq(ut, 12.0);
}
END_TEST

START_TEST(test_hours_to_hhmm) 
{
	double ut, ms;
	int hh, mm, ss;

	ut = 22.25;
	DectoHHMM(1,&ut,&hh,&mm,&ss,&ms);
    ck_assert_int_eq(hh, 22);
    ck_assert_int_eq(mm, 15);
    ck_assert_int_eq(ss, 22);
    ck_assert_int_eq(ms, 22);
}
END_TEST

START_TEST(test_hhmm_to_hours) 
{
	double ut;
    double hh, mm, ss, ms;
    hh = 22;
    mm = 15;
    ss = 0;
    ms = 0;

	HHMMtoDec(1,&hh,&mm,&ss,&ms,&ut);
    ck_assert_double_eq(ut, 22.25);
}
END_TEST

Suite *datetime_suite(void)
{
    Suite *s = suite_create("Datetime");
    TCase *tc = tcase_create("Core");

    // Add tests here
    tcase_add_test(tc, test_midtime);
    tcase_add_test(tc, test_minus_day);
    tcase_add_test(tc, test_time_index);
    tcase_add_test(tc, test_plus_day);
    tcase_add_test(tc, test_time_diff);
    tcase_add_test(tc, test_unix_time);
    tcase_add_test(tc, test_within);

    suite_add_tcase(s, tc);
    return s;
}

int main(void)
{
    int number_failed;
    Suite *s = datetime_suite();
    SRunner *sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);

    return (number_failed == 0) ? 0 : 1;
}
