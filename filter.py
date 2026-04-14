cb_set = set(cb_reports.index)
right_set = set(right_reports.index)

redflag = []

for code in major_reports.index:
    if code in cb_set and code in right_set:
        date_major = major_reports.loc[code, 'rcept_dt']
        date_cb = cb_reports.loc[code, 'rcept_dt']
        date_right = right_reports.loc[code, 'rcept_dt']

        if date_major < date_cb and date_major < date_right:
            name = major_reports.loc[code, 'corp_name']
            redflag.append([code, name, date_major, date_cb, date_right])

redflag_df = pd.DataFrame(
    redflag,
    columns=['corp_id', 'corp_name', 'date_major', 'date_cb', 'date_right']
)

print(redflag_df)
redflag_df.to_excel(r"C:\Users\user\Desktop\주식\redflag_corp.xlsx", index=False)
