#!/usr/bin/env python3
"""Phase 2 验证脚本（临时，不入库）：
1. 在临时 sqlite 库上生成并执行 resume/music 的 migration
2. 填充含 EN/JA 翻译的示例数据
3. 用 Django test Client 冒烟 ?lang= 参数（zh/en/ja/缺省回退）
用法：cd backend && python3 ../scripts/verify_i18n_backend.py
"""
import os
import sys
import tempfile

# 确保能从任意 cwd 启动（backend 目录需在 sys.path 中才能 import config.*）
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# 强制使用临时 sqlite 库（本机 MySQL 未运行）
from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(tempfile.gettempdir(), 'pltgg_i18n_verify.sqlite3'),
}

import django
django.setup()

# 测试客户端使用 testserver 作为 Host，需放行
from django.conf import settings as _s
_s.ALLOWED_HOSTS = ['*']

from django.core.management import call_command
from datetime import date

print('== 1. makemigrations resume music ==')
call_command('makemigrations', 'resume', 'music', verbosity=1)

print('== 2. migrate ==')
call_command('migrate', verbosity=0)

print('== 3. 填充双语示例数据 ==')
from resume.models import BasicInfo, Experience
from music.models import MusicWork

bi, _ = BasicInfo.objects.get_or_create(
    email='test@example.com',
    defaults=dict(
        name='李佳', title='全栈开发工程师', location='北京',
        summary_experience='十年云上经验',
        summary_skills='Kubernetes / Terraform / Python',
    ),
)
bi.title_en = 'Full-Stack Developer'
bi.title_ja = 'フルスタック開発者'
bi.location_en = 'Beijing'
bi.location_ja = '北京'
bi.summary_experience_en = 'Ten years of cloud-native experience'
bi.summary_experience_ja = 'クラウドネイティブ経験10年'
bi.save()

Experience.objects.get_or_create(
    company='云科技', position='SRE工程师',
    defaults=dict(start_date=date(2020, 1, 1), description='负责大规模集群稳定性和成本优化。'),
)
exp = Experience.objects.get(company='云科技')
exp.company_en = 'CloudTech Inc.'
exp.company_ja = 'クラウドテック社'
exp.position_en = 'SRE Engineer'
exp.position_ja = 'SREエンジニア'
exp.description_en = 'Owned stability and cost optimization of large-scale clusters.'
exp.description_ja = '大規模クラスターの安定性とコスト最適化を担当。'
exp.save()

MusicWork.objects.get_or_create(
    title='未命名Demo',
    defaults=dict(
        work_type='audio',
        description='一段即兴小样',
        title_en='Untitled Demo',
        title_ja='無題デモ',
        description_en='An improvised demo track',
        description_ja='即興のデモ音源',
    ),
)

print('== 4. API 冒烟（?lang 参数） ==')
from django.test import Client
c = Client()

def check(label, url, expect_field, expect_contains):
    r = c.get(url)
    assert r.status_code == 200, f'{label}: unexpected status {r.status_code}'
    ok = False
    body = r.json()
    parts = body if isinstance(body, list) else body.values()
    for part in parts:
        if isinstance(part, list):
            for item in part:
                if isinstance(item, dict) and expect_contains in str(item.get(expect_field, '')):
                    ok = True
        elif isinstance(part, dict) and expect_contains in str(part.get(expect_field, '')):
            ok = True
    print(f'  [{"PASS" if ok else "FAIL"}] {label}: {expect_field} contains "{expect_contains}"')
    return ok

all_ok = True
all_ok &= check('resume 缺省 lang -> 中文', '/api/resume/', 'title', '全栈开发工程师')
all_ok &= check('resume lang=zh -> 中文', '/api/resume/?lang=zh', 'title', '全栈开发工程师')
all_ok &= check('resume lang=en -> English', '/api/resume/?lang=en', 'title', 'Full-Stack Developer')
all_ok &= check('resume lang=ja -> 日本語', '/api/resume/?lang=ja', 'position', 'SREエンジニア')
all_ok &= check('resume lang=非法值 -> 回退中文', '/api/resume/?lang=xx', 'title', '全栈开发工程师')
all_ok &= check('music lang=en -> English', '/api/music/works/?lang=en', 'title', 'Untitled Demo')
all_ok &= check('music lang=ja -> 日本語', '/api/music/works/?lang=ja', 'title', '無題デモ')

# _en/_ja 变体字段不应外泄到响应
r = c.get('/api/resume/?lang=en')
body = r.json()
leaked = []
def find_leaks(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.endswith('_en') or k.endswith('_ja'):
                leaked.append(k)
            find_leaks(v)
    elif isinstance(obj, list):
        for item in obj:
            find_leaks(item)
find_leaks(body)
if leaked:
    print(f'  [FAIL] 响应中残留翻译变体字段: {sorted(set(leaked))}')
    all_ok &= False
else:
    print('  [PASS] 响应不含 _en/_ja 变体字段')
    all_ok &= True

print()
print('ALL PASS' if all_ok else 'SOME FAILED')
sys.exit(0 if all_ok else 1)