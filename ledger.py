# -*- coding: utf-8 -*-
import pandas as pd


def initialize(data):

    df = pd.DataFrame(data, 
                      index=['Brokerage', 'Roth IRA', 'Company Retirement'],
                      columns=['SWISX', 'SWTSX', 'SWAGX', 'Cash']).T

    return update_totals(df)


def update_totals(df):
    # clear totals
    df.loc['Total'] = None
    df['Total'] = None

    # compute totals
    df.loc['Total']= df.sum()
    df['Total'] = df.sum(axis=1)

    return df.round(2)


def update_percentages(df):

    ret = (100.0 * df / df['Total']['Total']).round(2)
    ret['Target'] = [30, 60, 10, 0, 100]

    return ret


def assign_cash(df, account, fund, value):
    df[account][fund] += value
    df[account]['Cash'] -= value
    return update_totals(df)


def report(df):
    print(df)
    print()
    print(update_percentages(df))
    print('='*50)


def expected_future_worth(x, percent_return=0.07, years=20, annual_payment=None):
    """
    estimate the future value of a current investment given the percent rate of return,
    number of years, and optional annual payment amount

    :param x: the present value of your account 
    :param percent_return: the market historically delivers a typical 7 percent annually
    :param years: the number of years over which to compound interest
    :param annual_payment: optional constant annual contribution to account
    :return type: float
    """

    i = percent_return
    n = years

    f = x * (1 + i) ** n

    if annual_payment is not None:
        f += (annual_payment / i) * (((1 + i) ** n) - 1)
    else:
        annual_payment = 0

    print('\n'.join(['', 'With annual contribution of ${0:,.2f} and', 
                     '\t{1:.2}% rate of return,',
                     '\texpected account value in {2} years: ${3:,.2f}',
                     '']).format(annual_payment, i*100, n, f))

    return round(f, 2)
