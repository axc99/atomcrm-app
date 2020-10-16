from flask_babel import _
from flaskr import db
import enum
from sqlalchemy import Integer, Enum, Column


# Card currencies
from flaskr.data.currencies import currencies


class CardCurrencies(enum.Enum):
    usd = 1
    cad = 2
    eur = 3
    aed = 4
    afn = 5
    all = 6
    amd = 7
    ars = 8
    aud = 9
    azn = 10
    bam = 11
    bdt = 12
    bgn = 13
    bhd = 14
    bif = 15
    bnd = 16
    bob = 17
    brl = 18
    bwp = 19
    byn = 20
    bzd = 21
    cdf = 22
    chf = 23
    clp = 24
    cny = 25
    cop = 26
    crc = 27
    cve = 28
    czk = 29
    djf = 30
    dkk = 31
    dop = 32
    dzd = 33
    eek = 34
    egp = 35
    ern = 36
    etb = 37
    gbp = 38
    gel = 39
    ghs = 40
    gnf = 41
    gtq = 42
    hkd = 43
    hnl = 44
    hrk = 45
    huf = 46
    idr = 47
    ils = 48
    inr = 49
    iqd = 50
    irr = 51
    isk = 52
    jmd = 53
    jod = 54
    jpy = 55
    kes = 56
    khr = 57
    kmf = 58
    krw = 59
    kwd = 60
    kzt = 61
    lbp = 62
    lkr = 63
    ltl = 64
    lvl = 65
    lyd = 66
    mad = 67
    mdl = 68
    mga = 69
    mkd = 70
    mmk = 71
    mop = 72
    mur = 73
    mxn = 74
    myr = 75
    mzn = 76
    nad = 77
    ngn = 78
    nio = 79
    nok = 80
    npr = 81
    nzd = 82
    omr = 83
    pab = 84
    pen = 85
    php = 86
    pkr = 87
    pln = 88
    pyg = 89
    qar = 90
    ron = 91
    rsd = 92
    rub = 93
    rwf = 94
    sar = 95
    sdg = 96
    sek = 97
    sgd = 98
    sos = 99
    syp = 100
    thb = 101
    tnd = 102
    top = 103
    tru = 104
    ttd = 105
    twd = 106
    tzs = 107
    uah = 108
    ugx = 109
    uyu = 110
    uzs = 111
    vef = 112
    vnd = 113
    xaf = 114
    xof = 115
    yer = 116
    zar = 117
    zmk = 118
    zwl = 119


# Installation card settings
class InstallationCardSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    amount_enabled = db.Column(db.Boolean, default=False, nullable=False)

    currency = Column(Enum(CardCurrencies), nullable=False, default='string')

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)

    # Format amount
    def format_amount(self, amount):
        if not self.amount_enabled:
            return 0

        currency = self.getCurrency()

        amount = int(amount) if amount % 1 == 0 else amount
        fmt_amount = '{:,}'.format(amount) if amount else '0'

        return currency['format_string'].format(fmt_amount)

    # Get currency by key
    def getCurrency(self):
        return currencies.get(self.currency.name)
