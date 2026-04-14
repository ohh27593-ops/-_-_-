patterns_cb = r'cb|전환.?사채|전환.?청구'
patterns_right = r'유상.?증자|3.?자.?배정'
pattern_major = (
    r"(?:"
    r"최대주주.?변경"
    r"|최대주주.?등.?변경"
    r"|변경.?후.?최대주주"
    r"|최대주주.?지분.?변동"
    r"|최대주주.?주식.?변동"
    r"|최대주주.?변동"
    r"|최대주주가.?변경"
    r"|최대주주.?변경을.?수반"
    r"|경영권.?변경"
    r"|경영권.?양수도"
    r"|지배구조.?변경"
    r")"
)

cb_reports = all_major_reports[
    all_major_reports['report_nm'].str.contains(patterns_cb, case=False, na=False)
].drop_duplicates(subset=['corp_code'], keep='last')

right_reports = all_major_reports[
    all_major_reports['report_nm'].str.contains(patterns_right, case=False, na=False)
].drop_duplicates(subset=['corp_code'], keep='last')

major_reports = all_exchange_reports[
    all_exchange_reports['report_nm'].str.contains(pattern_major, case=False, na=False)
].drop_duplicates(subset=['corp_code'], keep='last')

right_reports = right_reports.set_index('corp_code')
cb_reports = cb_reports.set_index('corp_code')
major_reports = major_reports.set_index('corp_code')
