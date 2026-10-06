#!/usr/bin/env python3
"""Builds the twelve-language pages of sackgram.com.

    python3 tools/build_pages.py /path/to/Sackgram-app

Writes, for each of en ko de es fr id it ja pt ru zh ar:
  home            /  and  /<lang>/                 from tools/home/<lang>.json
  privacy, terms  /privacy/ /terms/ and /<lang>/…  from the app repository's
                  docs/legal sources, converted verbatim
  delete-account  /delete-account/ (English, hand-written, kept as is apart
                  from its header and footer) and /<lang>/delete-account/,
                  built from that language's Privacy Policy 6-1~6-3, 6-8~6-10,
                  7-2 and 7-3, quoted verbatim
and adds the language list to the English-only pages (support/, company/,
i/, 404.html).

ADDED 2026-10-06 (Eric): twelve languages of equal weight. Every page lists all
twelve by their own names, at one size, in one order; nothing redirects by
browser language — the reader chooses. The English addresses Google Play
points at (/privacy/, /delete-account/) do not move.

⚠ The legal text is never edited here. Change the Markdown in the app
repository (docs/legal/privacy-en.md, terms-en.md, review-ko/*-ko.md,
i18n-drafts/<lang>/*.md) and run this again. The home text lives in
tools/home/<lang>.json; ko is the original (docs/website/
SACKGRAM-소개문구-초안.docx part 2 in the app repository) and every other
language is its translation — change ko first, then the rest.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://sackgram.com/'

LANGS = ['en', 'ko', 'de', 'es', 'fr', 'id', 'it', 'ja', 'pt', 'ru', 'zh', 'ar']
NAMES = {'en': 'English', 'ko': '한국어', 'de': 'Deutsch', 'es': 'Español', 'fr': 'Français',
         'id': 'Bahasa Indonesia', 'it': 'Italiano', 'ja': '日本語', 'pt': 'Português',
         'ru': 'Русский', 'zh': '中文', 'ar': 'العربية'}
RTL = {'ar'}
# hreflang values: zh is Simplified, pt is Brazilian Portuguese (the app's).
HREFLANG = {'zh': 'zh-Hans', 'pt': 'pt-BR'}

# Header, footer and delete-account labels. Account/settings words are the
# app's own ARB strings (deleteAccountTitle, settingsTitle).
T = {
 'en': dict(home='Home', privacy='Privacy', terms='Terms', support='Support', company='Company',
            privacy_policy='Privacy Policy', terms_of_service='Terms of Service', delete_account='Delete account',
            contact='Contact', languages='Languages'),
 'ko': dict(home='홈', privacy='개인정보', terms='약관', support='지원', company='회사',
            privacy_policy='개인정보처리방침', terms_of_service='이용약관', delete_account='계정 삭제',
            contact='문의', languages='언어',
            del_title='SACKGRAM 계정 삭제', del_meta='SACKGRAM은 Sackgram Labs,&nbsp;Inc.가 개발합니다.',
            del_lede='SACKGRAM 계정을 삭제하는 방법과, 삭제되는 정보와 남는 정보, 그리고 남는 기간입니다. 아래 내용은 <a href="{privacy}">개인정보처리방침</a> 제6조와 제7조의 해당 문장을 그대로 옮긴 것입니다.',
            del_how='계정 삭제와 삭제 요청', del_deleted='바로 삭제되는 정보', del_kept='삭제 후에도 남는 정보와 기간',
            del_partial='계정을 유지하면서 일부 정보만 삭제하기',
            del_desc='SACKGRAM 계정을 삭제하는 방법(앱 안에서, 앱 없이)과 삭제·보존되는 정보. SACKGRAM은 Sackgram Labs, Inc.가 개발합니다.'),
 'de': dict(home='Start', privacy='Datenschutz', terms='Bedingungen', support='Support', company='Unternehmen',
            privacy_policy='Datenschutzrichtlinie', terms_of_service='Nutzungsbedingungen', delete_account='Konto löschen',
            contact='Kontakt', languages='Sprachen',
            del_title='SACKGRAM-Konto löschen', del_meta='SACKGRAM wird von Sackgram Labs,&nbsp;Inc. entwickelt.',
            del_lede='So löschen Sie Ihr SACKGRAM-Konto, was gelöscht wird und was wie lange erhalten bleibt. Der folgende Text ist der Wortlaut der entsprechenden Absätze aus Abschnitt 6 und 7 unserer <a href="{privacy}">Datenschutzrichtlinie</a>.',
            del_how='Konto löschen oder die Löschung beantragen', del_deleted='Sofort gelöscht', del_kept='Was nach der Löschung erhalten bleibt und wie lange',
            del_partial='Einzelne Daten löschen und das Konto behalten',
            del_desc='Wie Sie ein SACKGRAM-Konto löschen – in der App oder ohne App – und was gelöscht und was aufbewahrt wird. SACKGRAM wird von Sackgram Labs, Inc. entwickelt.'),
 'es': dict(home='Inicio', privacy='Privacidad', terms='Términos', support='Soporte', company='Empresa',
            privacy_policy='Política de Privacidad', terms_of_service='Términos del Servicio', delete_account='Eliminar cuenta',
            contact='Contacto', languages='Idiomas',
            del_title='Eliminar su cuenta de SACKGRAM', del_meta='SACKGRAM es desarrollado por Sackgram Labs,&nbsp;Inc.',
            del_lede='Cómo eliminar su cuenta de SACKGRAM, qué se elimina y qué se conserva y durante cuánto tiempo. El texto siguiente reproduce literalmente los apartados correspondientes de las secciones 6 y 7 de nuestra <a href="{privacy}">Política de Privacidad</a>.',
            del_how='Eliminar la cuenta o solicitar su eliminación', del_deleted='Se elimina de inmediato', del_kept='Qué se conserva tras la eliminación y durante cuánto tiempo',
            del_partial='Eliminar parte de sus datos y conservar la cuenta',
            del_desc='Cómo eliminar una cuenta de SACKGRAM, con o sin la app, y qué se elimina y qué se conserva. SACKGRAM es desarrollado por Sackgram Labs, Inc.'),
 'fr': dict(home='Accueil', privacy='Confidentialité', terms='Conditions', support='Assistance', company='Entreprise',
            privacy_policy='Politique de confidentialité', terms_of_service="Conditions d'utilisation", delete_account='Supprimer le compte',
            contact='Contact', languages='Langues',
            del_title='Supprimer votre compte SACKGRAM', del_meta='SACKGRAM est développé par Sackgram Labs,&nbsp;Inc.',
            del_lede='Comment supprimer votre compte SACKGRAM, ce qui est supprimé, et ce qui est conservé et pendant combien de temps. Le texte ci-dessous reprend mot pour mot les paragraphes correspondants des sections 6 et 7 de notre <a href="{privacy}">Politique de confidentialité</a>.',
            del_how='Supprimer le compte ou en demander la suppression', del_deleted='Supprimé immédiatement', del_kept='Ce qui est conservé après la suppression, et pendant combien de temps',
            del_partial='Supprimer une partie de vos données et garder votre compte',
            del_desc="Comment supprimer un compte SACKGRAM, avec ou sans l'application, et ce qui est supprimé ou conservé. SACKGRAM est développé par Sackgram Labs, Inc."),
 'id': dict(home='Beranda', privacy='Privasi', terms='Ketentuan', support='Dukungan', company='Perusahaan',
            privacy_policy='Kebijakan Privasi', terms_of_service='Syarat Layanan', delete_account='Hapus akun',
            contact='Kontak', languages='Bahasa',
            del_title='Hapus akun SACKGRAM Anda', del_meta='SACKGRAM dikembangkan oleh Sackgram Labs,&nbsp;Inc.',
            del_lede='Cara menghapus akun SACKGRAM Anda, apa yang dihapus, serta apa yang disimpan dan berapa lama. Teks di bawah ini dikutip apa adanya dari bagian terkait Pasal 6 dan 7 <a href="{privacy}">Kebijakan Privasi</a> kami.',
            del_how='Menghapus akun atau meminta penghapusan', del_deleted='Langsung dihapus', del_kept='Yang tetap disimpan setelah penghapusan, dan berapa lama',
            del_partial='Menghapus sebagian data dan tetap mempertahankan akun',
            del_desc='Cara menghapus akun SACKGRAM, dengan atau tanpa aplikasi, serta apa yang dihapus dan disimpan. SACKGRAM dikembangkan oleh Sackgram Labs, Inc.'),
 'it': dict(home='Home', privacy='Privacy', terms='Condizioni', support='Assistenza', company='Azienda',
            privacy_policy='Informativa sulla privacy', terms_of_service='Condizioni di servizio', delete_account="Elimina l'account",
            contact='Contatti', languages='Lingue',
            del_title='Eliminare il suo account SACKGRAM', del_meta='SACKGRAM è sviluppato da Sackgram Labs,&nbsp;Inc.',
            del_lede="Come eliminare il suo account SACKGRAM, che cosa viene eliminato e che cosa viene conservato e per quanto tempo. Il testo che segue riporta alla lettera i paragrafi corrispondenti delle sezioni 6 e 7 della nostra <a href=\"{privacy}\">Informativa sulla privacy</a>.",
            del_how="Eliminare l'account o chiederne l'eliminazione", del_deleted='Eliminato immediatamente', del_kept="Che cosa resta dopo l'eliminazione, e per quanto tempo",
            del_partial="Eliminare una parte dei dati e mantenere l'account",
            del_desc="Come eliminare un account SACKGRAM, con o senza l'app, e che cosa viene eliminato o conservato. SACKGRAM è sviluppato da Sackgram Labs, Inc."),
 'ja': dict(home='ホーム', privacy='プライバシー', terms='利用規約', support='サポート', company='会社情報',
            privacy_policy='プライバシーポリシー', terms_of_service='利用規約', delete_account='アカウントを削除',
            contact='お問い合わせ', languages='言語',
            del_title='SACKGRAMアカウントの削除', del_meta='SACKGRAMはSackgram Labs,&nbsp;Inc.が開発しています。',
            del_lede='SACKGRAMアカウントの削除方法と、削除される情報、残る情報とその期間です。以下は<a href="{privacy}">プライバシーポリシー</a>第6条・第7条の該当箇所をそのまま掲載したものです。',
            del_how='アカウントの削除と削除の依頼', del_deleted='すぐに削除される情報', del_kept='削除後も残る情報とその期間',
            del_partial='アカウントを残したまま一部の情報だけを削除する',
            del_desc='SACKGRAMアカウントの削除方法(アプリ内・アプリなし)と、削除・保存される情報。SACKGRAMはSackgram Labs, Inc.が開発しています。'),
 'pt': dict(home='Início', privacy='Privacidade', terms='Termos', support='Suporte', company='Empresa',
            privacy_policy='Política de Privacidade', terms_of_service='Termos de Serviço', delete_account='Excluir conta',
            contact='Contato', languages='Idiomas',
            del_title='Excluir sua conta do SACKGRAM', del_meta='O SACKGRAM é desenvolvido pela Sackgram Labs,&nbsp;Inc.',
            del_lede='Como excluir sua conta do SACKGRAM, o que é excluído e o que é mantido e por quanto tempo. O texto abaixo reproduz literalmente os trechos correspondentes das seções 6 e 7 da nossa <a href="{privacy}">Política de Privacidade</a>.',
            del_how='Excluir a conta ou pedir a exclusão', del_deleted='Excluído imediatamente', del_kept='O que é mantido após a exclusão, e por quanto tempo',
            del_partial='Excluir parte dos seus dados e manter a conta',
            del_desc='Como excluir uma conta do SACKGRAM, com ou sem o app, e o que é excluído e mantido. O SACKGRAM é desenvolvido pela Sackgram Labs, Inc.'),
 'ru': dict(home='Главная', privacy='Конфиденциальность', terms='Условия', support='Поддержка', company='Компания',
            privacy_policy='Политика конфиденциальности', terms_of_service='Условия обслуживания', delete_account='Удалить аккаунт',
            contact='Контакты', languages='Языки',
            del_title='Удаление аккаунта SACKGRAM', del_meta='SACKGRAM разрабатывает Sackgram Labs,&nbsp;Inc.',
            del_lede='Как удалить аккаунт SACKGRAM, что удаляется, а что сохраняется и как долго. Ниже дословно приведены соответствующие пункты разделов 6 и 7 нашей <a href="{privacy}">Политики конфиденциальности</a>.',
            del_how='Удаление аккаунта или запрос на удаление', del_deleted='Удаляется сразу', del_kept='Что сохраняется после удаления и как долго',
            del_partial='Удалить часть данных и сохранить аккаунт',
            del_desc='Как удалить аккаунт SACKGRAM — в приложении или без него — и что удаляется и сохраняется. SACKGRAM разрабатывает Sackgram Labs, Inc.'),
 'zh': dict(home='首页', privacy='隐私', terms='条款', support='支持', company='公司',
            privacy_policy='隐私政策', terms_of_service='服务条款', delete_account='删除账号',
            contact='联系', languages='语言',
            del_title='删除你的 SACKGRAM 账号', del_meta='SACKGRAM 由 Sackgram Labs,&nbsp;Inc. 开发。',
            del_lede='如何删除你的 SACKGRAM 账号,哪些信息会被删除,哪些信息会保留以及保留多久。以下内容原文摘自我们的<a href="{privacy}">隐私政策</a>第6条和第7条的相关条款。',
            del_how='删除账号或申请删除', del_deleted='立即删除的信息', del_kept='删除后保留的信息及保留期限',
            del_partial='保留账号,仅删除部分信息',
            del_desc='如何删除 SACKGRAM 账号(在应用内或不使用应用),以及哪些信息会被删除或保留。SACKGRAM 由 Sackgram Labs, Inc. 开发。'),
 'ar': dict(home='الرئيسية', privacy='الخصوصية', terms='الشروط', support='الدعم', company='الشركة',
            privacy_policy='سياسة الخصوصية', terms_of_service='شروط الخدمة', delete_account='حذف الحساب',
            contact='التواصل', languages='اللغات',
            del_title='حذف حسابك في SACKGRAM', del_meta='تطوّر SACKGRAM شركةُ Sackgram Labs,&nbsp;Inc.',
            del_lede='كيفية حذف حسابك في SACKGRAM، وما الذي يُحذف، وما الذي يُحتفظ به ولأي مدة. النص التالي منقول حرفيًا من البنود ذات الصلة في القسمين 6 و7 من <a href="{privacy}">سياسة الخصوصية</a>.',
            del_how='حذف الحساب أو طلب حذفه', del_deleted='ما يُحذف فورًا', del_kept='ما يُحتفظ به بعد الحذف ومدته',
            del_partial='حذف جزء من بياناتك مع الإبقاء على الحساب',
            del_desc='كيفية حذف حساب SACKGRAM، من داخل التطبيق أو من دونه، وما الذي يُحذف وما الذي يُحتفظ به. تطوّر SACKGRAM شركةُ Sackgram Labs, Inc.'),
}

LEGAL_DESC = {
 'privacy': {'en': 'How Sackgram Labs, Inc. handles information in the SACKGRAM app.'},
 'terms': {'en': 'The terms that apply when you use the SACKGRAM app, provided by Sackgram Labs, Inc.'},
}


def esc(t):
    return html.escape(t, quote=False)


# ---------- Markdown (the app's legal sources) ----------

def inline(t):
    t = esc(t).replace('"', '"')
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'(?<![\w.@/:">])([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)',
               r'<a href="mailto:\1">\1</a>', t)
    return t


def render_list(items):
    def rec(level, i):
        s = '<ul>'
        while i < len(items) and items[i][0] >= level:
            ind, txt = items[i]
            if ind > level:
                break
            s += '<li>' + inline(txt)
            i += 1
            if i < len(items) and items[i][0] > level:
                sub, i = rec(items[i][0], i)
                s += sub
            s += '</li>'
        return s + '</ul>', i
    return rec(items[0][0], 0)[0]


LIST_ITEM = re.compile(r'^(\s*)[-*] (.*)$')


def blocks(lines, base):
    """Renders Markdown lines (no title, no date line) to HTML blocks."""
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        m = re.match(r'^(#{2,6}) (.*)$', l)
        if m:
            lv = len(m.group(1)) - base + 2
            out.append(f'<h{lv}>{inline(m.group(2).strip())}</h{lv}>')
            i += 1
            continue
        if LIST_ITEM.match(l):
            items = []
            while i < len(lines) and LIST_ITEM.match(lines[i]):
                m = LIST_ITEM.match(lines[i])
                items.append((len(m.group(1)), m.group(2)))
                i += 1
            out.append(render_list(items))
            continue
        if l.strip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], rows[2:]
            t = ('<div class="table-scroll"><table>\n<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head)
                 + '</tr></thead>\n<tbody>\n'
                 + '\n'.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
                 + '\n</tbody></table></div>')
            out.append(t)
            continue
        if l.startswith('#'):
            raise SystemExit('unhandled line: ' + l)
        para = []
        while (i < len(lines) and lines[i].strip() and not lines[i].startswith('#')
               and not lines[i].strip().startswith('|') and not LIST_ITEM.match(lines[i])):
            para.append(lines[i].strip())
            i += 1
        out.append('<p>' + inline(' '.join(para)) + '</p>')
    return out


def parse_legal(md, lang):
    lines = md.split('\n')
    title = next(l[2:].strip() for l in lines if l.startswith('# '))
    if lang == 'en':
        title = re.sub(r'^SACKGRAM ', '', title)
    meta_i = next(i for i, l in enumerate(lines[:8]) if ('·' in l or '・' in l) and not l.startswith('#'))
    meta = lines[meta_i].strip().replace('**', '')
    body_lines = [l for i, l in enumerate(lines) if not l.startswith('# ') and i != meta_i]
    base = min(len(re.match(r'^(#+)', l).group(1)) for l in body_lines if re.match(r'^#{2,6} ', l))
    return title, meta, blocks(body_lines, base)


def legal_source(app, lang, doc):
    if lang == 'en':
        return os.path.join(app, 'docs/legal', f'{doc}-en.md')
    if lang == 'ko':
        return os.path.join(app, 'docs/legal/review-ko', f'{doc}-ko.md')
    return os.path.join(app, 'docs/legal/i18n-drafts', lang, f'{doc}.md')


def paragraphs_by_number(md):
    """{'6-8': [lines…]} — each numbered paragraph with everything up to the next."""
    out, cur = {}, None
    for l in md.split('\n'):
        m = re.match(r'^\*\*(\d{1,2}-\d{1,2})\b', l)
        if m:
            cur = m.group(1)
            out[cur] = [l]
        elif l.startswith('#'):
            cur = None
        elif cur:
            out[cur].append(l)
    return out


# ---------- page shell ----------

def page_path(lang, page):
    """Site-relative directory of a page: '' / 'privacy/' / 'ko/' / 'ko/privacy/'."""
    return ('' if lang == 'en' else f'{lang}/') + (f'{page}/' if page else '')


def rel(from_dir, to_dir):
    depth = from_dir.count('/')
    up = '../' * depth
    target = up + to_dir
    return target if target else './'


def lang_list(cur_dir, cur_lang, targets, tl):
    """targets: {lang: site-relative dir}."""
    items = []
    for l in LANGS:
        attrs = f' hreflang="{HREFLANG.get(l, l)}" lang="{l}"'
        if l in RTL:
            attrs += ' dir="rtl"'
        if l == cur_lang:
            attrs += ' aria-current="page"'
        items.append(f'<li><a href="{rel(cur_dir, targets[l])}"{attrs}>{NAMES[l]}</a></li>')
    return (f'        <nav class="lang-list" aria-label="{tl["languages"]}">\n          <ul>\n          '
            + '\n          '.join(items) + '\n          </ul>\n        </nav>\n')


def header(cur_dir, lang, current):
    tl = T[lang]
    home, priv, terms = page_path(lang, ''), page_path(lang, 'privacy'), page_path(lang, 'terms')
    nav = [('home', home), ('privacy', priv), ('terms', terms), ('support', 'support/'), ('company', 'company/')]
    lis = []
    for key, d in nav:
        cur = ' aria-current="page"' if key == current else ''
        lis.append(f'<li><a href="{rel(cur_dir, d)}"{cur}>{tl[key]}</a></li>')
    return ('    <header class="site-header">\n      <div class="wrap">\n'
            f'        <a class="brand" href="{rel(cur_dir, home)}">SACK<span>GRAM</span></a>\n'
            f'        <nav aria-label="Main">\n          <ul>\n          ' + '\n          '.join(lis)
            + '\n          </ul>\n        </nav>\n')


def footer(cur_dir, lang):
    tl = T[lang]
    links = [(tl['privacy_policy'], page_path(lang, 'privacy')), (tl['terms_of_service'], page_path(lang, 'terms')),
             (tl['support'], 'support/'), (tl['delete_account'], page_path(lang, 'delete-account')),
             (tl['company'], 'company/')]
    lis = '\n'.join(f'          <li><a href="{rel(cur_dir, d)}">{t}</a></li>' for t, d in links)
    return ('    <footer class="site-footer">\n      <div class="wrap">\n        <ul>\n' + lis + '\n        </ul>\n'
            '        <p>&copy; 2026 Sackgram Labs, Inc. All rights reserved.<br>\n'
            f'        {tl["contact"]}: <a href="mailto:info@sackgram.com">info@sackgram.com</a></p>\n'
            '      </div>\n    </footer>\n')


def alternates(page):
    out = []
    for l in LANGS:
        out.append(f'    <link rel="alternate" hreflang="{HREFLANG.get(l, l)}" href="{SITE}{page_path(l, page)}">')
    out.append(f'    <link rel="alternate" hreflang="x-default" href="{SITE}{page_path("en", page)}">')
    return '\n'.join(out) + '\n'


def write_page(lang, page, title, description, current, main_html, hero=''):
    d = page_path(lang, page)
    dir_attr = ' dir="rtl"' if lang in RTL else ''
    targets = {l: page_path(l, page) for l in LANGS}
    s = ('<!DOCTYPE html>\n'
         f'<html lang="{HREFLANG.get(lang, lang)}"{dir_attr}>\n  <head>\n'
         '    <meta charset="utf-8">\n'
         '    <meta name="viewport" content="width=device-width, initial-scale=1">\n'
         f'    <title>{title}</title>\n'
         f'    <meta name="description" content="{html.escape(description)}">\n'
         '    <meta name="theme-color" content="#3BC3DE">\n'
         f'    <link rel="stylesheet" href="{rel(d, "")}style.css">\n'
         + alternates(page) +
         '  </head>\n  <body>\n'
         + header(d, lang, current) + lang_list(d, lang, targets, T[lang]) +
         '      </div>\n    </header>\n'
         + hero +
         '    <main>\n      <div class="wrap">\n' + main_html + '      </div>\n    </main>\n'
         + footer(d, lang) + '  </body>\n</html>\n')
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    with open(os.path.join(ROOT, d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(s)


# ---------- the four page kinds ----------

HOME_NOTE = ('        <!-- Generated by tools/build_pages.py from tools/home/{lang}.json. The Korean\n'
             '             (/ko/) is the original: Sackgram-app docs/website/\n'
             '             SACKGRAM-소개문구-초안.docx, part 2, approved by Eric on 2026-10-05.\n'
             '             Every other language is its translation; all twelve must say the\n'
             '             same thing. Terms follow each language\'s app strings (ARB). -->\n')


def build_home(lang):
    d = json.load(open(os.path.join(ROOT, 'tools/home', f'{lang}.json'), encoding='utf-8'))
    hero = ('    <div class="hero">\n      <div class="wrap">\n'
            f'        <h1>{d["hero_h1"]}</h1>\n        <p>{d["hero_p"]}</p>\n'
            '      </div>\n    </div>\n')
    body = d['body_html']
    if lang == 'en':
        # The English home sits at the root; the translations one level down.
        body = body.replace('href="../', 'href="')
    main = HOME_NOTE.format(lang=lang) + '        ' + body.strip() + '\n'
    write_page(lang, '', d['title'], d['description'], 'home', main, hero)


def build_legal(app, lang, doc):
    md = open(legal_source(app, lang, doc), encoding='utf-8').read()
    title, meta, body = parse_legal(md, lang)
    src = os.path.relpath(legal_source(app, lang, doc), app)
    main = (f'        <!-- Generated by tools/build_pages.py from Sackgram-app main ({src}) by converting the Markdown verbatim. Edit the source document in the app repository, not this file. -->\n'
            f'        <h1>{inline(title)}</h1>\n        <p class="meta">{inline(meta)}</p>\n' + '\n'.join(body) + '\n')
    tl = T[lang]
    page_title = f'{inline(title)} — SACKGRAM' if lang == 'en' else inline(title)
    desc = LEGAL_DESC[doc].get(lang) or (tl['privacy_policy'] if doc == 'privacy' else tl['terms_of_service']) + ' — SACKGRAM'
    write_page(lang, doc, page_title, desc, 'privacy' if doc == 'privacy' else 'terms', main)


def build_delete_translated(app, lang):
    md = open(legal_source(app, lang, 'privacy'), encoding='utf-8').read()
    P = paragraphs_by_number(md)
    tl = T[lang]
    priv = rel(page_path(lang, 'delete-account'), page_path(lang, 'privacy'))

    def render(*nums):
        out = []
        for n in nums:
            out += blocks(P[n], 2)
        return '\n'.join(out) + '\n'

    main = (f'        <!-- Required by Google Play\'s account deletion policy. Generated by tools/build_pages.py: the\n'
            f'             headings are this page\'s own; every paragraph under them is the {lang} Privacy Policy\'s\n'
            f'             own text (7-2, 7-3, 6-8, 6-9, 6-10, 6-1, 6-2, 6-3), quoted verbatim from\n'
            f'             {os.path.relpath(legal_source(app, lang, "privacy"), app)}. Change the policy first. -->\n'
            f'        <h1>{tl["del_title"]}</h1>\n        <p class="meta">{tl["del_meta"]}</p>\n'
            f'        <p class="lede">{tl["del_lede"].format(privacy=priv)}</p>\n\n'
            f'        <h2>{tl["del_how"]}</h2>\n' + render('7-2', '7-3') +
            f'\n        <h2>{tl["del_deleted"]}</h2>\n' + render('6-8') +
            f'\n        <h2>{tl["del_kept"]}</h2>\n' + render('6-9', '6-10') +
            f'\n        <h2>{tl["del_partial"]}</h2>\n' + render('6-1', '6-2', '6-3'))
    write_page(lang, 'delete-account', f'{tl["del_title"]} — SACKGRAM', tl['del_desc'], None, main)


def rewrap_english_delete():
    """The English delete page is hand-written (Play links to it); only its
    header and footer are regenerated."""
    p = os.path.join(ROOT, 'delete-account/index.html')
    s = open(p, encoding='utf-8').read()
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
    main = re.search(r'    <main>\n      <div class="wrap">\n(.*?)      </div>\n    </main>\n', s, re.S).group(1)
    write_page('en', 'delete-account', title, desc, None, main)


def add_list_to_english_only(path):
    """support/, company/, i/, 404.html exist in English only: the list links
    each language's home. Inserted (or replaced) right after the main nav."""
    p = os.path.join(ROOT, path)
    s = open(p, encoding='utf-8').read()
    d = os.path.dirname(path) + '/' if os.path.dirname(path) else ''
    if path == '404.html':
        d = ''
    s = re.sub(r'        <nav class="lang-list".*?</nav>\n', '', s, flags=re.S)
    targets = {l: page_path(l, '') for l in LANGS}
    block = lang_list(d, 'en', targets, T['en'])
    s, n = re.subn(r'(        <nav aria-label="Main">.*?</nav>\n)', lambda m: m.group(1) + block, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('no main nav in ' + path)
    open(p, 'w', encoding='utf-8').write(s)


def main():
    app = sys.argv[1]
    for lang in LANGS:
        build_home(lang)
        build_legal(app, lang, 'privacy')
        build_legal(app, lang, 'terms')
        if lang != 'en':
            build_delete_translated(app, lang)
    rewrap_english_delete()
    for p in ('support/index.html', 'company/index.html', 'i/index.html', '404.html'):
        add_list_to_english_only(p)


if __name__ == '__main__':
    main()
