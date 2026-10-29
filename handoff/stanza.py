import math
def split(b_lead, qb_lead, k, stages, amax=180, lead=-1):
    """stages: [(age_start_months, Z)]; returns (B, QB) per stage, scaled to the leading stage."""
    ends = [s[0] for s in stages[1:]] + [amax]
    lw, lw23 = [], []
    for (a0, z), a1 in zip(stages, ends):
        s1 = s2 = 0.0
        for a in range(a0, a1):
            surv = math.exp(-sum(zz * (min(a, e) - st) / 12 for (st, zz), e in zip(stages, ends) if a > st))
            w = (1 - math.exp(-k / 12 * a)) ** 3
            s1 += surv * w; s2 += surv * w ** (2 / 3)
        lw.append(s1); lw23.append(s2)
    sb = b_lead / lw[lead]; sq = qb_lead * b_lead / lw23[lead]
    return [(sb * x, sq * y / (sb * x)) for x, y in zip(lw, lw23)]
if __name__ == "__main__":
    print(split(3.5, 6.3, 0.48, [(0, 1.5), (24, 0.7)]))
