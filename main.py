today = datetime.today()
before = today - timedelta(days=365 * 3)

start_dt = before.strftime('%Y%m%d')
end_dt = today.strftime('%Y%m%d')

api = DartApi(start_dt, end_dt, corp_cls='K')

all_major_reports = api.get_list(
    pblntf_ty='B',
    pblntf_detail_ty='B001',
    label='주요사항보고서(B001)'
)

all_exchange_reports = api.get_list(
    pblntf_ty='I',
    pblntf_detail_ty='I001',
    label='거래소공시(I)'
)

print(all_major_reports.head())
print(all_exchange_reports.head())

all_major_reports.to_excel(r"C:\Users\user\Desktop\주식\cb_right.xlsx")
all_exchange_reports.to_excel(r"C:\Users\user\Desktop\주식\major.xlsx")
