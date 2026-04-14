import time
from datetime import datetime, timedelta
import requests
import pandas as pd


class DartApi:
    def __init__(self, start_dt, end_dt, corp_cls='K'):
        self.start_dt = pd.to_datetime(str(start_dt), format='%Y%m%d')
        self.end_dt = pd.to_datetime(str(end_dt), format='%Y%m%d')
        self.corp_cls = corp_cls

        txt_path = r"C:\Users\user\Desktop\주식\buythehouse.txt"
        with open(txt_path, 'r', encoding='utf-8') as f:
            self.api_key = f.read().strip()
        print('api_key 받기 성공')

        self.session = requests.Session()
        self.base_url = "https://opendart.fss.or.kr/api/list.json"

    def call(self, params):
        response = self.session.get(self.base_url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()

    def get_list(self, pblntf_ty=None, pblntf_detail_ty=None, label='공시'):
        data_list = []
        sdt = self.start_dt

        while sdt < self.end_dt:
            edt = min(sdt + timedelta(days=90), self.end_dt)

            bgn_de = sdt.strftime('%Y%m%d')
            end_de = edt.strftime('%Y%m%d')

            print(f'\n[{label}] 수집 구간: {bgn_de} ~ {end_de}')

            params = {
                'crtfc_key': self.api_key,
                'bgn_de': bgn_de,
                'end_de': end_de,
                'last_reprt_at': 'Y',
                'corp_cls': self.corp_cls,
                'sort': 'date',
                'sort_mth': 'asc',
                'page_no': 1,
                'page_count': 100
            }

            if pblntf_ty is not None:
                params['pblntf_ty'] = pblntf_ty
            if pblntf_detail_ty is not None:
                params['pblntf_detail_ty'] = pblntf_detail_ty

            first = self.call(params)

            if first.get('status') == '013':
                print(f'[{label}] 데이터 없음')
                sdt = edt
                continue

            total_page = int(first.get('total_page', 1))
            now_list = first.get('list', [])
            data_list.extend(now_list)

            print(f'[{label}] 1 / {total_page} 페이지, {len(now_list)}건')

            for page in range(2, total_page + 1):
                params['page_no'] = page
                tmp = self.call(params)
                page_list = tmp.get('list', [])
                data_list.extend(page_list)

                if page % 10 == 0 or page == total_page:
                    print(f'[{label}] {page} / {total_page} 페이지')

                time.sleep(0.03)

            sdt = edt

        df = pd.DataFrame(data_list)

        if not df.empty:
            df['rcept_dt'] = pd.to_datetime(df['rcept_dt'], format='%Y%m%d', errors='coerce')

        return df
