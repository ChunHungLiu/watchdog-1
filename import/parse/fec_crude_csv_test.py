#!/usr/bin/python
# -*- coding: utf-8 -*-
import fec_crude_csv, doctest, cgitb

def records(inputstring):
    return list(fec_crude_csv.readstring(inputstring))

def test_endtext():
    """
    >>> records(filing_207928)
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [{...'fec_ver': '5.3'...},
     {...'filer_id': 'C00410761', 'original_data': {...}...
      'committee': 'Castor for Congress'...}]
    >>> records(truncated_filing)       # same
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [{...'fec_ver': '5.3'...},
     {...'filer_id': 'C00410761', 'original_data': {...}...
      'committee': 'Castor for Congress'...}]
    """

# Note the extra quote mark on the [ENDTEXT] line.
filing_207928 = '''"HDR","FEC","5.3","NGP Campaign Office(R)","1.0e","","","0",""
"F99","C00410761","Castor for Congress","P.O. Box 5419","","Tampa","FL","33675","Amy Martin","20060322","MST"
[BEGINTEXT]
March 22, 2006

Christopher A. Whyrick
Senior Campaign Finance Analyst
Federal Elections Commission
999 E Street, NW
Washington, DC 20463

Identification Number: C00410761

Reference: Year End Report (10/1/05-12/31/05)

Dear Mr. Whyrick,

	This letter is in response to the FEC request for additional information dated February 23, 2006.  As instructed in your letter, we have amended our Year End Report and corrected the discrepancy on Line 2 of FEC Form 3Z-1.

	If you need further assistance, please contact me at (813)251-5094.


Sincerely,



Amy Martin, Treasurer
Castor for Congress

[ENDTEXT]"
'''

# This is an invalid filing but it shouldn’t hang the importer.  (It
# did at one point; it would loop endlessly looking for [ENDTEXT].)
truncated_filing = '''"HDR","FEC","5.3","NGP Campaign Office(R)","1.0e","","","0",""
"F99","C00410761","Castor for Congress","P.O. Box 5419","","Tampa","FL","33675","Amy Martin","20060322","MST"
[BEGINTEXT]
March 22, 2006
'''

def test_v2_02_data():
    """We can’t handle version 2.x data yet, so we should just skip
    it until we find a spec for it.  Raising an exception is not
    acceptable.

    >>> records(filing_30458_truncated)
    []
    """

filing_30458_truncated = '''/* Header
FEC_Ver_# = 2.02
Soft_Name = Vocus, Inc. PACPRO
Soft_Ver# = 6.16.040
DEC/NODEC = DEC
Date_Fmat = CCYYMMDD
NameDelim = ^
Form_Name = F3XN
FEC_IDnum = C00238725
Committee = National Air Traffic Controllers Association PAC
Schedule_Counts:
SA11ai   = 00002
SB23     = 00023
/* End Header
"F3XN","C00238725","National Air Traffic Controllers Association PAC","1325 Massachusetts Ave., NW","","Washington","DC","20005","","X","M3","",,"",20020201,20020228,290018.35,45558.46,335576.81,23000,312576.81,0,0,332,45226.46,45558.46,0,0,45558.46,0,0,0,0,0,0,0,45558.46,45558.46,0,0,0,0,0,23000,0,0,0,0,0,0,0,0,0,23000,23000,45558.46,0,45558.46,0,0,0,250065.32,2002,91011.49,341076.81,28500,312576.81,534,90477.49,91011.49,0,0,91011.49,0,0,0,0,0,0,0,91011.49,91011.49,0,0,0,0,0,28500,0,0,0,0,0,0,0,0,0,28500,28500,91011.49,0,91011.49,0,0,0,"Mr. John Carr",20020323
"SA11ai","C00238725","IND","Glasserman^John^Mr.^Glasserman","4 Spruce Lane","","Essex Junction","VT","054524387","","","Federal Aviation Administration","Air Traffic Controller",404,,202,"15","","","","","","","","","","","","","","","Payroll Deduction ($101.00 Biweekly)","","10000072200300002"
'''

def test_windows_1252_characters():
    r"""The FEC claims that filings containing non-ASCII characters will be
    rejected, but here we have an example of a filing that wasn’t.  It
    contains a Windows-1252 byte.  Note that it is an en dash, not an
    em dash, sigh.  I am arbitrarily deciding that the result should
    be encoded in UTF-8, in part because the Python `csv` module is
    documented to be UTF-8-safe.

    Note that this test doesn’t pass yet; the SKIP option to doctest
    was added in Python 2.5, so this test will barf 'has an invalid
    option' on 2.4.

    >>> records(filing_181941_truncated)[-1]
    ... #doctest: +ELLIPSIS
    {...'occupation': 'Team Ldr \xe2\x80\x93 HRIS'...}
    """

filing_181941_truncated = u'''"HDR","FEC","5.2","Vocus PAC Management","3.00.1828","","",0,""
"F3XN","C00083857","Occidental Petroleum Corporation Political Action Committee","10889 Wilshire Blvd.","","Los Angeles","CA","90024","","X","MY","",,"",20050101,20050630,48873.88,113149.90,162023.78,97411.13,64612.65,0.00,0.00,96058.37,16874.30,112932.67,0.00,0.00,112932.67,0.00,0.00,0.00,0.00,0.00,217.23,0.00,113149.90,113149.90,0.00,0.00,0.00,0.00,0.00,97000.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,411.13,97411.13,97411.13,112932.67,0.00,112932.67,0.00,0.00,0.00,48873.88,2005,113149.90,162023.78,97411.13,64612.65,96058.37,16874.30,112932.67,0.00,0.00,112932.67,0.00,0.00,0.00,0.00,0.00,217.23,0.00,113149.90,113149.90,0.00,0.00,0.00,0.00,0.00,97000.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,411.13,97411.13,97411.13,112932.67,0.00,112932.67,0.00,0.00,0.00,"Dominick^S.P.^^",20050722,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00
"SA11ai","C00083857","IND","","16919 PRESTON BEND DR","","DALLAS","TX","75248","","","Occidental Chemical Corp.","GM NGO/Laurel",400.00,20050429,400.00,"15","","","","","","","","","","","","","","","","","11109795","","","","","","SEWELL","LAWRENCE","R","",""
"SA11ai","C00083857","IND","","4001 VIA SOLANA","","P VERDES ESTATES","CA","90274","","","Occidental Petroleum Corp.","Dir Internal Audit",600.00,20050429,600.00,"15","","","","","","","","","","","","","","","","","11109790","","","","","","MISTRY","MARZI","J","",""
"SA11ai","C00083857","IND","","322 FAIRHAVEN CT","","NEWBURY PARK","CA","91320","","","Occidental Petroleum Corp.","Team Ldr  HRIS",350.00,20050429,350.00,"15","","","","","","","","","","","","","","","","","11109794","","","","","","PLACANICA","VINCENT","J","",""
'''.encode('iso-8859-1')
assert chr(0x96) in filing_181941_truncated # not really an ISO-8859-1
                                            # character! Windows-1252.

def cover_record(data, name):
    return fec_crude_csv.read_filing(data, name)[0]

def test_candidate_name():
    """There are a variety of fields from which we can extract
    candidate names.  This tests some of them.

    This is from the committee name 'KT McFarland for Congress':
    >>> cover_record(filing_230174_truncated, '230174.fec')['candidate']
    'KT McFarland'

    This is from committee name 'Friends of Tyson Pratcher':
    >>> cover_record(filing_230176_truncated, '230176.fec')['candidate']
    'Tyson Pratcher'

    This one is from an actual `candidate_name` field in form F6:
    >>> cover_record(filing_230177_truncated, '230177.fec')['candidate']
    'Rick ODonnell'

    In this case there is a `candidate_name` field, but it is empty,
    because instead they used the `candidate_first_name`,
    `candidate_middle_name`, and `candidate_last_name` fields.  The
    `committee_name_(pcc)` field would give us 'Sue Kelly'.

    >>> cover_record(filing_230179, '230179.fec')['candidate']
    'Sue W. Kelly'

    In this case, `candidate_name` contains a ^-separated name, which
    needs to be properly reordered.
    >>> cover_record(filing_230185, '230179.fec')['candidate']
    'HOWARD KALOOGIAN'

    In this case, there is a more specific candidate name 'JOHN
    T. DOOLITTLE' to be extracted from the committee name, but we
    don’t yet do it.
    >>> cover_record(filing_181904_truncated, '181904.fec')['candidate']
    'JOHN DOOLITTLE'

    """

def test_format_6():
    r"""Format 6.x is a little tricky to decode.

    The header line has changed, the separator is now `\x1c`, presumably
    there are no quotes any more, and the official rule on amounts now
    treats '500' as meaning '$500' and not '$5.00' (which XXX is still
    not supported in the code!)

    This is a very minimal test ensuring that we don’t completely
    break the ability to read version 6.x files again.  (Apparently
    Unicode thinks that `\x1c` is a kind of paragraph separator, so if
    you’re doing a `.readline()` on an instance of the `streamreader`
    of the Windows-1252 codec, it will give you the bytes up to the
    next `\x1c`, and so I accidentally broke reading 6.x files by
    introducing a `streamreader` into the pipeline.)

    >>> cover_record(filing_333594_truncated, '333594.fec')['committee']
    'Amerigroup Corporation Political Action Committee (Amerigroup PAC)'
    >>> cover_record(filing_333600_truncated, '333600.fec')['committee']
    'Dan Grant for Congress'

    """

def test_report_id():
    """The report ID ties together the original filing and its amendments.

    Filing 230176 is a new filing.
    >>> cover_record(filing_230176_truncated, '230176.fec')['report_id']
    '230176'

    But filing 230174 is an amendment of filing 211016.
    >>> cover_record(filing_230174_truncated, '230174.fec')['report_id']
    '211016'

    The original report ID is in a different position in the 6.x header.
    >>> cover_record(filing_333600_truncated, '333600.fec')['report_id']
    '306890'

    """

def test_strange_headers():
    """Filing 184656 doesn’t include all of the header fields.

    >>> cover_record(filing_184656, '184656.fec')['committee']
    'Hewlett Packard Company PAC'

    Filing 184693’s report_id has an extraneous space character at the
    end, which should *not* be considered part of the report ID:
    >>> cover_record(filing_184693_truncated, '184693.fec')['report_id']
    '180927'

    Filing 19538 specifies a Name Delim character of “ ”, but it
    doesn’t really mean it, because it delimits its names with “^”
    just like all the other filings.  So I'm going to assume that
    blanks in this field are extraneous.  To verify that the delimiter
    is being properly parsed, I’m going to verify that names are
    parsed correctly.
    >>> [rec.get('contributor') for rec in
    ...       fec_crude_csv.read_filing(filing_19538_truncated, '19538.fec')[1]]
    [None, None, 'Mrs. Jean Abernathy', 'Mrs. Renee Abraham']

    """

filing_230174_truncated = '''HDR,FEC,5.3,CMDI FEC FILER,5.3.0,,FEC-211016,1,
F3A,C00415620,"KT McFarland for Congress","954 Lexington Avenue","Box 135","New York",NY,10021,,NY,14,Q1,P2006,20061101,NY,X,,,,20060101,20060331,172080.00,1000.00,171080.00,135651.09,0.00,135651.09,24293.78,0.00,0.00,168150.00,3930.00,172080.00,0.00,0.00,0.00,172080.00,0.00,0.00,0.00,0.00,0.00,0.00,172080.00,135651.09,400000.00,0.00,0.00,0.00,1000.00,0.00,0.00,1000.00,2000.00,538651.09,390864.87,172080.00,562944.87,538651.09,24293.78,602005.00,1000.00,601005.00,174691.47,0.00,174691.47,572075.00,3930.00,576005.00,0.00,1000.00,25000.00,602005.00,0.00,0.00,0.00,0.00,0.00,0.00,602005.00,174691.47,400000.00,0.00,0.00,0.00,1000.00,0.00,0.00,1000.00,2000.00,577691.47,"Alan McFarland",20060721,,,,,,,,,
SA11A1,C00415620,IND,,"219 East 69th Street","Apt 5-D","New York",NY,10021,P2006,,"Auda Private Equity LLC","Investment Manager",1000.00,20060201,1000.00,15,"Receipt",,,,,,,,,,,,,,,,60314.C590,,,,,,"Andryc","David",,,
SA11A1,C00415620,IND,,"219 East 69th Street","Apt 5-D","New York",NY,10021,P2006,,"Auda Private Equity LLC","Investment Manager",500.00,20060201,-500.00,15,"Reattribution Memo",,,,,,,,,,,,,X,"REATTRIBUTION TO SPOUSE",,60314.C591,60314.C590,SA11A1,,,,"Andryc","David",,,
'''

filing_230176_truncated = '''"HDR","FEC","5.3","NGP Campaign Office(R)","1.0e","","","0",""
"F3N","C00421578","Friends of Tyson Pratcher","454 North Willett","","Memphis","TN","38112","","TN","09","12P","P2006","20060803","TN","X","","","","20060401","20060714","3955.00","4200.00","-245.00","57578.74","171.00","57407.74","15078.20","0","0","2750.00","1205.00","3955.00","0","0","0","3955.00","0","0","0","0","171.00","0","4126.00","57578.74","0","0","0","0","0","0","4200.00","4200.00","5000.00","66778.74","77730.94","4126.00","81856.94","66778.74","15078.20","88064.44","4200.00","83864.44","63957.24","171.00","63786.24","76810.00","6054.44","82864.44","0","5200.00","0","88064.44","0","0","0","0","171.00","0","88235.44","63957.24","0","0","0","0","0","0","4200.00","4200.00","5000.00","73157.24","Horne^Allison","20060721","","","","","","","","",""
"SA11AI","C00421578","IND","","341 West 11th Street #8E","","New York","NY","10014","P2006","","Self-Employed","Attorney","500.00","20060519","500.00","","","","","","","","","","","","","","","","","","C350641","","","","","","Jones","Gregory","Davis","",""
'''

filing_230177_truncated = '''"HDR","FEC","5.3","Aristotle International CM4 PM4","Version 4.2.1","^","",""
"F6","C00374777","Coloradans for Rick ODonnell","PO Box 260693","","Lakewood","CO","80226   ","H2CO07055","Rick ODonnell","H","CO","07",20060721
"F65","C00374777","IND","ONeill^Timothy","2191 Baldy Lane","","Evergreen","CO","80439","Snell & Wilmer","Attorney",20060720,1000.00,"","","","","",,"","","","","","","","60721.C2980"
"F65","C00374777","IND","Kauffman^Kevin","K.P. Kauffman Company, In","1675 Broadway, Suite 28 ","Denver","CO","80202","K.P. Kauffman Company, In","Chairman, CEO",20060720,1600.00,"","","","","",,"","","","","","","","60721.C2977"
'''

filing_230179 = '''HDR,FEC,5.3,FILPAC,4.23,"^",,
F2N,H4NY19073,,187 Jay Street,,Katonah,NY,10536,REP,,NY,19,2006,C00294900,Sue Kelly for Congress,PO Box 599,,Katonah,NY,105360599,,ROMP IV 2006,"228 S. Washington St., Ste. 115",,Alexandria,VA,22314,Sue Kelly,20060721,0.00,0.00,Kelly,Sue,W.,,
'''

filing_230185 = '''HDR,FEC,5.3,FECfile,5.3.1.0(f16),,,
F1MN,C00400937,VETERANS FOR VICTORY PAC,"2245 148TH AVENUE, NE",,BELLEVUE,WA,98007,N,,,-,H4ND00038,SAND^DUANE^^,H,ND,00,20040810,H2CA39102,ESCOBAR^TIM^^,H,CA,39,20040817,H2KY04071,DAVIS^GEOFFREY C^^,H,KY,04,20040824,S6VT00111,PARKE^GREGORY TARL^^,S,VT,00,20041012,S4CA00282,KALOOGIAN^HOWARD^^,S,CA,00,20060329,20040617,20040510,20060329,MCCURDY^RUSSELL^^,20060722
'''

filing_181904_truncated = '''HDR,FEC,5.2,NetFile,1967,^,FEC-180228,001,Report Generated: 07/22/2005 11:18:27
F3A,C00242768,JOHN T. DOOLITTLE FOR CONGRESS,2150 RIVER PLAZA DR. #150,,SACRAMENTO,CA,95833,,CA,4,Q2,P2006,20060606,CA,,,,,20050401,20050630,151947.33,0.00,151947.33,99667.66,0.00,99667.66,215344.09,0.00,15468.80,105249.60,20172.73,125422.33,0.00,26525.00,0.00,151947.33,0.00,0.00,0.00,0.00,0.00,0.00,151947.33,99667.66,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,99667.66,163064.42,151947.33,315011.75,99667.66,215344.09,280515.83,0.00,280515.83,197866.25,3745.00,194121.25,182756.60,40384.23,223140.83,0.00,57375.00,0.00,280515.83,0.00,0.00,0.00,0.00,3745.00,0.00,284260.83,197866.25,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,27499.86,225366.11,David Bauer,20050722,H0CA14042,DOOLITTLE^JOHN,D31,259532.33,0.00,259532.33,5875.00,0.00,5875.00
SA11AI,C00242768,IND,,748 E. HILLCREST AVE.,,Yuba City,CA,95991,P2006,,,NONE,1200.00,20050417,1000.00,15,,,,,,,,,,,,,,,,,INC:A:63552,,,,,,BOYER,KARNA J.,,,
SA11AI,C00242768,IND,,2150 PROFESSIONAL DRIVE,,ROSEVILLE,CA,95661,P2006,,self,Property Management,350.00,20050417,350.00,15,,,,,,,,,,,,,,,,,INC:A:63536,,,,,,BRYANT,ERIC,,MR.,
'''

filing_333594_truncated = '''HDR\x1cFEC\x1c6.1\x1cAristotle International CM5 PM5\x1cVersion 5.2\x1c\x1c0\x1c\x1c
F3XN\x1cC00428102\x1cAmerigroup Corporation Political Action Committee (Amerigroup PAC)\x1c\x1c4425 Corporation Lane\x1c\x1cVirginia Beach\x1cVA\x1c23462   \x1cQ1\x1c\x1c\x1c\x1c20080101\x1c20080331\x1cX\x1cLittel\x1cJohn\x1cE.\x1c\x1c\x1c20080415\x1c29749.49\x1c34461.13\x1c64210.62\x1c9039.97\x1c55170.65\x1c0.00\x1c0.00\x1c31467.51\x1c2993.62\x1c34461.13\x1c0.00\x1c0.00\x1c34461.13\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c34461.13\x1c34461.13\x1c0.00\x1c0.00\x1c39.97\x1c39.97\x1c0.00\x1c6500.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c2500.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c9039.97\x1c9039.97\x1c34461.13\x1c0.00\x1c34461.13\x1c39.97\x1c0.00\x1c39.97\x1c29749.49\x1c2008\x1c34461.13\x1c64210.62\x1c9039.97\x1c55170.65\x1c31467.51\x1c2993.62\x1c34461.13\x1c0.00\x1c0.00\x1c34461.13\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c34461.13\x1c34461.13\x1c0.00\x1c0.00\x1c39.97\x1c39.97\x1c0.00\x1c6500.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c2500.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c9039.97\x1c9039.97\x1c34461.13\x1c0.00\x1c34461.13\x1c39.97\x1c0.00\x1c39.97
SA11AI\x1cC00428102\x1c80413.C183\x1c\x1c\x1cIND\x1c\x1cAncona\x1cVincent\x1c\x1c\x1c\x1c6640 Towering Oak Path\x1c\x1cColumbia\x1cMD\x1c21044\x1c\x1c\x1c20080111\x1c38.50\x1c38.50\x1c15\x1cReceipt\x1c\x1cAMERIGROUP Maryland  Inc.\x1cCOO - Health Plan\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1cPayroll Deduction: (38.50/Pay Period          )\x1c\x1c
SA11AI\x1cC00428102\x1c80413.C223\x1c\x1c\x1cIND\x1c\x1cAncona\x1cVincent\x1c\x1c\x1c\x1c6640 Towering Oak Path\x1c\x1cColumbia\x1cMD\x1c21044\x1c\x1c\x1c20080125\x1c288.45\x1c326.95\x1c15\x1cReceipt\x1c\x1cAMERIGROUP Maryland  Inc.\x1cCOO - Health Plan\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1cPayroll Deduction: (57.69/Pay Period          )\x1c\x1c
'''

filing_333600_truncated = '''HDR\x1cFEC\x1c6.1\x1cNGP Campaign Office(R)\x1c3.0\x1cFEC-306890\x1c1\x1c
F3A\x1cC00434621\x1cDan Grant for Congress\x1c\x1c6109 Rickey Drive\x1c\x1cAustin\x1cTX\x1c78757\x1cTX\x1c10\x1cQ3\x1c\x1c\x1c\x1c20070701\x1c20070930\x1cGrant\x1cBarbara\x1c\x1c\x1c\x1c20080415\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c45247.00\x1c250.00\x1c44997.00\x1c38096.51\x1c0.00\x1c38096.51\x1c72247.01\x1c0.00\x1c4128.92\x1c41677.00\x1c1070.00\x1c42747.00\x1c0.00\x1c2500.00\x1c0.00\x1c45247.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c45247.00\x1c38096.51\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c250.00\x1c0.00\x1c0.00\x1c250.00\x1c0.00\x1c38346.51\x1c65346.52\x1c45247.00\x1c110593.52\x1c38346.51\x1c72247.01\x1c118112.08\x1c250.00\x1c117862.08\x1c45615.07\x1c0.00\x1c45615.07\x1c114162.08\x1c1350.00\x1c115512.08\x1c0.00\x1c2500.00\x1c100.00\x1c118112.08\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c118112.08\x1c45615.07\x1c0.00\x1c0.00\x1c0.00\x1c0.00\x1c250.00\x1c0.00\x1c0.00\x1c250.00\x1c0.00\x1c45865.07\x1c\x1c\x1c\x1c\x1c\x1c
SA11AI\x1cC00434621\x1cC4068349\x1c\x1c\x1cIND\x1c\x1cAndries\x1cLarry\x1c\x1c\x1c\x1c1140 San Ysidro Dr\x1c\x1cBeverly Hills\x1cCA\x1c902102103\x1cP2008\x1c\x1c20070923\x1c50.00\x1c50.00\x1c\x1c\x1c\x1c20th Century Fox\x1cWriter\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c
SA11AI\x1cC00434621\x1cC4068348\x1c\x1c\x1cIND\x1c\x1cAtchity\x1cKenneth\x1c\x1c\x1c\x1c400 S Burnside No. 11B\x1c\x1cLos Angeles\x1cCA\x1c90036\x1cP2008\x1c\x1c20070923\x1c100.00\x1c100.00\x1c\x1c\x1c\x1cSelf\x1cProducer\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c
'''

filing_184656 = '''HDR,FEC,5.2,DemocracyDirect,Ver 6.5
F99,C00196725,Hewlett Packard Company PAC,3000 Hanover Street,20BX,Palo Alto,CA,94304,Ann Baskins,20050818,
[BEGINTEXT]
This amendment, filed in response to the letter from the FEC dated August 12, 2005, corrects the figures on Lines 11(a)(i) and 11(a)(ii), Column B of the Detailed Summary Page.
[ENDTEXT]
'''

filing_184693_truncated = '''HDR,FEC,5.2,"FECfile4",5.2,,FEC-180927 ,1
F3XA,C00093054,"Wal-Mart Stores Inc. PAC For Responsible Government","702 S.W. 8th Street","","Bentonville","AR","727160150","","X","M7","","","","20050601","20050630",513583.82,164630.83,678214.65,185500.00,492714.65,0.00,0.00,16783.90,146603.16,163387.06,0.00,0.00,163387.06,0.00,0.00,0.00,0.00,0.00,1243.77,0.00,164630.83,164630.83,0.00,0.00,0.00,0.00,0.00,125000.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,60500.00,185500.00,185500.00,163387.06,0.00,163387.06,0.00,0.00,0.00,301464.31,2005,719467.34,1020931.65,528217.00,492714.65,36939.60,674942.03,711881.63,0.00,0.00,711881.63,0.00,0.00,0.00,0.00,2500.00,5085.71,0.00,719467.34,719467.34,0.00,0.00,917.00,917.00,0.00,329500.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,197800.00,528217.00,528217.00,711881.63,0.00,711881.63,917.00,0.00,917.00,"Raymond W Bracy","20050818",0,0,0,0,0,0,0,0,0,0,0,0
SA11A1,C00093054,"IND",,"6 Canterbury Park","","Bentonville","AR","727124088","","","WAL-Mart Stores Inc.","Vice President Dmm",260,"20050616",20,"","","","","","","","","","","","","","","","","","WP2011866162005","","",,,,"Alderson",Art ,,,
SA11A1,C00093054,"IND",,"6 Canterbury Park","","Bentonville","AR","727124088","","","WAL-Mart Stores Inc.","Vice President Dmm",260,"20050602",20,"","","","","","","","","","","","","","","","","","WP188779622005","","",,,,"Alderson",Art ,,,
'''

filing_19538_truncated = '''HDR,"FEC","3.00","Proprietary","1.00"," ","FEC-12344",2,""
F3XA,"C00003418","REPUBLICAN NATIONAL COMMITTEE","310 FIRST STREET SE","","WASHINGTON","DC","20003"," ","X","M2","",20010101,"",20010101,20010131,24061917.05,10607884.29,34669801.34,9549466.96,25120334.38,1446.75,0.00,2056600.10,6193833.84,8250433.94,0.00,32500.00,8282933.94,0.00,0.00,0.00,37805.46,20360.00,94077.72,2172707.17,10607884.29,8435177.12,3515525.78,3698621.93,2313778.25,9527925.96,2876.00,0.00,0.00,0.00,0.00,0.00,18665.00,0.00,0.00,18665.00,0.00,9549466.96,5850845.03,8282933.94,18665.00,8264268.94,5829304.03,37805.46,5791498.57,24061917.05,2001,10607884.29,34669801.34,9549466.96,25120334.38,2056600.10,6193833.84,8250433.94,0.00,32500.00,8282933.94,0.00,0.00,0.00,37805.46,20360.00,94077.72,2172707.17,10607884.29,8435177.12,3515525.78,3698621.93,2313778.25,9527925.96,2876.00,0.00,0.00,0.00,0.00,0.00,18665.00,0.00,0.00,18665.00,0.00,9549466.96,5850845.03,8282933.94,18665.00,8264268.94,5829304.03,37805.46,5791498.57,"JAY C. BANNING Asstant Treasurer","20010905"
SD9,"C00003418","CAN","FRIENDS OF SENATOR DAVID KARNES","626 109TH PLAZA","","OMAHA","NE","68154","NEWS RELEASES",612.00,0.00,0.00,612.00,"","",""," ","","","","","","","",""," ","D09-01"
SD9,"C00003418","CAN","SENATOR KARNES CAMPAIGN","626 109TH PLAZA","","OMAHA","NE","68154","NEWS RELEASES",834.75,0.00,0.00,834.75,"","",""," ","","","","","","","",""," ","D09-02"
SA11A1,"C00003418","IND","Abernathy^Jean^Mrs.","50 Broad Cove Lane","","Montgomery","TX","77356","P2002","","","Retired",0.00,20001012,300.00,"15","","","",""," ","","","","","","","","","X","","C","31912284","","",""
SA11A1,"C00003418","IND","Abraham^Renee^Mrs.","1317 University Avenue","","Lubbock","TX","79401","P2002","","Self-employed","Office Manager",0.00,20001205,55.00,"15","","","",""," ","","","","","","","","","X","","C","32331751","","",""
'''

if __name__ == "__main__":
    cgitb.enable(format='text')
    doctest.testmod()
