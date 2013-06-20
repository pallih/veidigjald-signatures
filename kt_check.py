import scraperwiki

truecount = []
falsecount = []


def check_kt(kt):
    kt = kt.replace('-', '').strip()
    kt = kt.replace(' ', '').strip()
    kt = kt.replace('=', '').strip()
    try:
        if len(kt) == 10:
            check = [3, 2, 7, 6, 5, 4, 3, 2, 1, 0]
            return sum([int(kt[i]) * check[i] for i in range(10)]) % 11 == 0
        else:
            return False
    except ValueError:
        return False


totalcount = scraperwiki.sqlite.select('count(*) from veidigjald')
total_anon = scraperwiki.sqlite.select('count(*) from veidigjald where \
    name = "The signatory decided not to show his/her name on the Internet."')
total_empty_but_name = scraperwiki.sqlite.select('count(*) from veidigjald\
 where kt LIKE ""')
selection_statement = 'kt from veidigjald where "kt" is not "null" and kt is not ""'
kts = scraperwiki.sqlite.select(selection_statement)


for kt in kts:
    if kt['kt'] is None:
        pass
    else:
        check = check_kt(kt['kt'])
        if check is True:
            truecount.append(kt['kt'])
        if check is False:
            falsecount.append(kt['kt'])

print 'Count of true: ', len(truecount)
print 'Count of False: ', len(falsecount)
print 'Total checked: ', len(truecount)+len(falsecount)
print '======='
print 'Total signatures with a name but without a kt: ',\
        total_empty_but_name[0]['count(*)']
print 'Total anonymous in db: ', total_anon[0]['count(*)']
print 'Total in db: ', totalcount[0]['count(*)']
