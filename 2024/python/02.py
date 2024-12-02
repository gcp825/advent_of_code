def ordered(report):

    return True if sorted(report) in (report, report[::-1]) else False


def within_limits(report):

    diffs = [abs(report[i]-report[i-1]) for i in range(1,len(report))]

    return True if min(diffs) >= 1 and max(diffs) <= 3 else False


def safe(report, dampening):

    reports = [report[:i] + report[i+1:] for i in range(len(report))] if dampening else [report]
    allowed = [x for x in reports if ordered(x) and within_limits(x)]

    return report if allowed else None


def main(filepath):

    reports = [list(map(int, line.split())) for line in open(filepath).read().split('\n')]

    return len([x for x in reports if safe(x, False)]), len([x for x in reports if safe(x, True)])

print(main('02.txt'))