# sackgram.com

The public website for Sackgram Labs, Inc. Plain static HTML and one CSS file
— no build step, no external requests (no fonts, no analytics, no CDN). Open
any `.html` file in a browser to preview it exactly as it will be served.

⚠ **One page has JavaScript, since 2026-09-30: `i/index.html`** — one inline
script that shows the Android *Open in Sackgram* button and, inside
KakaoTalk's in-app browser, hands the link to KakaoTalk once so Android can
open the app. It makes no request, and the page's Content-Security-Policy
(`connect-src 'none'`, `script-src` pinned to that script's SHA-256) refuses
one if it ever tried. **Editing that script means recomputing the hash in the
same change**, or the browser refuses the script and the button never shows.
Every other page still has no JavaScript.

## Company details as published

| Field | Value |
|---|---|
| Company name | Sackgram Labs, Inc. |
| Mailing address | PO Box 40401, North Charleston, SC 29423, United States |
| State of incorporation | Delaware, United States |
| Effective date on legal pages | October 7, 2026 (filled in the app repository's `docs/legal/` on 2026-10-06, Sackgram-app #601, and regenerated here). The privacy policy's EU/UK representative paragraph is an interim sentence until the representative contracts are signed (app release checklist item 41) |
| Governing law | State of Delaware, United States |
| Venue | State of Delaware, United States |

**The website publishes a contact mailing address; Google Play, Apple,
D-U-N-S and the USPTO get the physical address each of them requires. The two
differing is by design** (2026-09-28).

### ⚠️ Use the business address, never the registered agent's

The Delaware registered agent address (251 Little Falls Drive, Wilmington —
Corporation Service Company) must **not** appear anywhere on this site. Apple
and Google both want the real place of business, and **Google explicitly
rejects registered-agent addresses**. The company page was labelled
"Principal place of business" for exactly this reason — the term "registered
address" means the agent's Delaware address to a US reader, which is the
opposite of what is wanted here. ⚠ Since 2026-09-28 it is labelled "Mailing
address" and shows the PO Box (see the note above): a PO Box is not a place of
business, so the old label would have been false. The rule about the
registered agent's address still stands everywhere.

### ⚠️ Venue jurisdiction needs a lawyer's decision — flagged, not settled

Terms §12 currently names the **State of Delaware** for both governing law and
venue. Governing law in Delaware is the ordinary choice for a Delaware
corporation. **Venue is a separate question and was not decided on the
merits** — it was set to match.

The trade-off, which counsel should weigh:

- **Delaware venue** keeps disputes in the state of incorporation and is
  familiar to corporate counsel — but it means *the company* also litigates
  there, away from its actual operations in South Carolina.
- **South Carolina venue** puts disputes where the business actually is.
- Either way, consumer-protection law in many jurisdictions gives individual
  users the right to sue locally regardless of what the terms say. §12 already
  carves that out, but the carve-out's wording should be reviewed too.

**These documents have not been reviewed by a lawyer.** They describe what the
app actually does, accurately and conservatively, which is the right starting
point — but the liability, indemnity and governing-law sections in particular
should be reviewed by counsel in your jurisdiction before launch.

## Files

```
index.html            Home — the long introduction (English), company name
ko/index.html         Home in Korean — the original of the introduction -> /ko
<lang>/…               ko de es fr id it ja pt ru zh ar: home, privacy/, terms/,
                      delete-account/ in that language (generated — see
                      "Twelve languages")
tools/build_pages.py  Generates the pages above; tools/home/<lang>.json = home text
privacy/index.html    Privacy Policy   -> /privacy   (required by both app stores)
terms/index.html      Terms of Service -> /terms
delete-account/index.html  Account deletion -> /delete-account (required by Google Play)
support/index.html    Support          -> /support   (required by both app stores)
company/index.html    Legal entity and address -> /company
i/index.html          Invite landing -> /i   (see below)
style.css             All styling
CNAME                 Custom domain for GitHub Pages — do not delete
.nojekyll             Serve files as-is, skip Jekyll processing
.well-known/assetlinks.json   Android Digital Asset Links — see below
```

### `.well-known/assetlinks.json` — read this before editing it

This is the file Android fetches to decide two separate things, and they are
easy to conflate:

| `relation` | What it lets the app do | Broken by |
|---|---|---|
| `delegate_permission/common.get_login_creds` | Use a **passkey** bound to `sackgram.com` for account recovery | A missing fingerprint → recovery fails on those builds |
| `delegate_permission/common.handle_all_urls` | Open `https://sackgram.com/...` links **directly in the app** instead of a browser (Android App Links) | A missing fingerprint → links open in the browser |

**`sha256_cert_fingerprints` is a list and must hold ALL THREE release keys** (two Google app signing keys — see the 2026-10-03 note below the table — and the upload key). Under Play
App Signing the certificate a real user's installed app carries is **Google's
app signing key**, not the upload key you sign with locally. Listing only the
upload key means everything works in a locally built release APK and fails for
every single person who installs from the Play Store — the worst shape this
failure can take, because testing does not reveal it.

| Key | Fingerprint starts | What carries it |
|---|---|---|
| Google app signing key — **current** | `E9:D4:1E:AC…` | Play-installed builds since Play's key upgrade |
| Google app signing key — **previous (KEEP)** | `E3:82:D2:EB…` | Play-installed builds still served with the previous signer |
| Upload key | `C5:0F:A8:AD…` | A release APK built and installed locally |

Both come from **Play Console → Test and release → Setup → App integrity →
App signing**, in the same colon-hex form `keytool` prints.

⚠ **2026-10-03: Play's app signing key had been UPGRADED.** Play Console →
Protected with Play → App signing shows `E9:D4:1E:AC…` as the current key and
`E3:82:D2:EB…` under "Previous app signing keys". With only `E3:82` listed, the
first passkey recovery on a Play-installed build failed. **Keep both Google
keys here permanently**: after a rotation Play can still serve the previous
signer to Android versions that do not honour the rotated one, and a missing
key breaks passkeys and App Links on exactly those devices. The app's server
accept-list (`WEBAUTHN_ANDROID_CERT_SHA256` in Sackgram-app's
`backend/signaling/.env`) must hold the same two.

#### ⚠️ A DEBUG FINGERPRINT IS IN THIS FILE RIGHT NOW AND MUST COME OUT BEFORE RELEASE

Added **2026-09-16**, deliberately and temporarily, overriding the rule that
used to stand here. That rule is quoted below rather than deleted, because it
is still the right default and this is an exception to it with an end date.

| Key | Fingerprint starts | Relations | Added | Removed |
|---|---|---|---|---|
| Debug keystore (development machine) | `96:A5:2A:57…` | `handle_all_urls` only | 2026-09-16 | **before the first store release** |

Removing it is deleting the **second statement object** in its entirety — the
one with a single fingerprint in it. Nothing in the first statement changes.

**Why it went in.** Android verifies App Links **at install time** against the
certificate the installed build carries. A debug build (`flutter run`, or a
locally installed debug APK) carries the debug key, so with only the two
release fingerprints listed, every `https://sackgram.com/i/…` link on a
development phone fell through to this site's landing page instead of opening
the app. Confirmed on a device on 2026-09-16: a card's QR decoded correctly and
opened `/i/` in a browser. That made the one path the digital business card
exists for untestable before release.

**It is scoped to App Links ONLY, in its own statement object.** The file now
holds two statements: the two release keys carry both relations, and the debug
key carries `handle_all_urls` alone. So a debug build opens
`https://sackgram.com/…` links in the app, and **cannot** be handed a passkey
bound to this domain.

⚠ **Do not merge it back into the first statement, and do not give it
`get_login_creds` "since the server already trusts it".** That was considered
and rejected on 2026-09-16. The server does accept this exact fingerprint in
its own private allow-list (`WEBAUTHN_ANDROID_CERT_SHA256`), which is a
different surface: a private list on our own backend, versus a public
declaration that anything signed with a widely-shared key may ask this domain
for credentials. Widening it would buy a debug build the ability to test
passkey recovery, and cost exactly the protection the rule below exists for.

**What the original rule said, and it is still true:**

> ⚠ **Never add the debug keystore's fingerprint here.** The debug key is
> unprotected by design and sits on every machine that has ever built the app;
> treating it as proof of identity for this domain is not a trade worth making.
> (The app's *server* accepts a debug fingerprint in its own private allow-list
> for `flutter run` testing — a different surface, not this one.)

**The risk, stated precisely rather than waved at.** A debug keystore is
generated per machine with a published password and alias, so this fingerprint
is not a universally known key — it is the one on the development machine. If
that file leaks, someone could build an app under the package name
`com.sackgram.labs` and have it claim `sackgram.com` links — intercepting a
link the victim taps, and showing them whatever it likes. It requires them to
sideload it first, which it cannot do over a Play install (different
signature). **It does NOT reach passkeys**, because the debug statement carries
`handle_all_urls` alone; that is the whole reason for the split above, and it
is the difference between a link-interception risk and a credential one.
Narrow, real, and not worth carrying past the point where it stops paying for
itself.

**Removing it is deleting the second statement object** — the one whose only
fingerprint is `96:A5:2A:57…` — leaving a file with one statement, exactly as
it was before 2026-09-16. Do it before the first store release; the removal is
tracked in the app repository's `CLAUDE.md` release checklist so it cannot be
lost with this file.

**Serving requirements, all three of which GitHub Pages already satisfies:**
HTTPS, `Content-Type: application/json`, and **no redirect** — Android's
verifier does not follow one.

**To check it without a device**, ask Google's own verifier what it parsed:

```
curl.exe -sS "https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://sackgram.com&relation=delegate_permission/common.handle_all_urls"
```

It answers with the statements as the verifier sees them, so a successful
parse also proves the content type and the absence of a redirect. Note the
`maxAge` in the response: Google caches for **about an hour**, so a change can
take that long to show up there.

**To check it on a phone** — PowerShell, one command per line (PowerShell has
no `&&`), and `-s <serial>` is not optional when two devices are attached:

```powershell
adb -s <serial> shell pm verify-app-links --re-verify com.sackgram.labs
adb -s <serial> shell pm get-app-links com.sackgram.labs
```

The second prints the domain and its state. **`verified` is the answer**;
`legacy_failure` or `1024` means the verifier did not match the installed
build's certificate against this file. The first command only asks Android to
try again — it does not change what is in this file, so run it AFTER a change
here has gone live, allowing for Google's own cache above.

⚠ **A re-verify does not clear a user's manual choice.** If the domain was
approved by hand (Settings → the app → Open by default → Add link) it stays
approved regardless of what this file says, which is how a build can appear to
work while the file is still wrong. On a phone that has been used for testing,
clear that first or the check proves nothing.

### `i/index.html` — where a scanned Sackgram code lands

A Sackgram QR code or invite link points at this domain. On a phone that has
the app, Android's App Link verification (the `handle_all_urls` relation
above) opens the app directly and this page is never seen. It exists for the
other case: **a stranger who scanned a code off a printed sign or a business
card and does not have Sackgram.** Without it that scan leads nowhere at all —
a custom `sackgram://` scheme simply fails on a phone with no app installed,
and does not offer the store.

That makes it the first thing some people will ever read about Sackgram, so it
is written like print: no build-progress wording, no in-app vocabulary, and
nothing that goes stale on a card somebody is still carrying a year from now.

#### ⚠ THE URL MUST BE `/i/` WITH THE CODE AFTER `#`, NOT `/i/{code}`

GitHub Pages serves static files and does not rewrite paths. `/i/{code}` is
not a file, so Pages answers it with **`404.html` and an HTTP 404** — this
page would never be reached. `/i/` is a real directory with an `index.html`
and answers 200.

So a link has to be shaped `https://sackgram.com/i/#CODE`. Two independent
reasons land on the same shape, which is why it is not a workaround:

1. **It is the only shape this host will serve.** (The alternative would be
   making `404.html` detect `/i/` paths and render invite content — a page
   that returns 404 while pretending to be a real page, and one file doing two
   unrelated jobs.)
2. **The fragment is never sent to a server.** Everything after `#` stays in
   the browser, so the code is absent from web server logs, from the `Referer`
   header, and from anything the hosting provider sees — by construction, not
   by policy. The app's `AndroidManifest.xml` already records this as the
   reason the token belongs in the fragment.

The Android intent filter matches on `pathPrefix="/i/"`, which `/i/#CODE`
satisfies, and `Intent.getData()` keeps the fragment.

⚠ **The page says out loud that we never receive the code.** Moving the code
into the path would make that sentence false on the page a stranger reads
first. If the link format ever changes, the sentence goes in the same change.

⚠ **If the app ever emits a longer path** such as `/i/g/#CODE`, that directory
needs its own `index.html` here first, for the same reason — otherwise it 404s.

#### Only `/i/` is intercepted by the app, not the whole site

`handle_all_urls` sounds broader than it behaves. It verifies the app for the
**domain**; what the app actually opens is decided by its own intent filters,
and there is exactly one for this site, with `pathPrefix="/i/"`. So
`/privacy`, `/terms`, `/support` and `/company` always open in a browser, which
is what the app stores require of those links. The app *could* claim more
paths later by adding a filter, with no change to this site — worth knowing,
since nothing here would show it.

### URLs are extensionless, on purpose

Each page is a directory with an `index.html`, so the public URLs are
`/privacy`, `/terms`, `/support`, `/company` — not `/privacy.html`. That was
chosen before anything was submitted to the app stores, because **changing a
Privacy Policy or Support URL after submission means resubmitting**, and
because an extensionless URL survives a move to any other static host, while
`.html` bakes today's implementation into an address you then have to
redirect forever.

Links between pages are **relative** (`../privacy/`), not root-absolute
(`/privacy/`). Relative works in all three contexts this site gets viewed in:
the real domain, the `github.io/sackgram.com/` preview before DNS is
connected, and a local checkout. Root-absolute would break the middle one.

To preview locally, serve it rather than opening files directly — `file://`
does not resolve a bare directory to its `index.html`:

```bash
cd sackgram.com && python3 -m http.server 8000   # then open localhost:8000
```

## Twelve languages, and where every page comes from

⚠ **2026-10-06 (Eric): the site is in twelve languages of equal weight** — en,
ko, de, es, fr, id, it, ja, pt, ru, zh, ar. SACKGRAM ships in 170 countries in
these twelve at once, and an English home with one Korean page beside it made
it look like a local Korean app.

- **Every page lists all twelve languages**, by their own names (English,
  한국어, Deutsch, Español, Français, Bahasa Indonesia, Italiano, 日本語,
  Português, Русский, 中文, العربية), in that fixed order, at one size and
  weight. The current one is marked by an underline only. **Do not make one
  language bigger, bolder or first-by-visitor.** There is **no automatic
  redirect** by browser language — the reader chooses.
- **Home, Privacy, Terms and Delete account exist in all twelve**: English at
  `/`, `/privacy/`, `/terms/`, `/delete-account/` (**these English addresses
  are what Google Play points at and must not move**), the others under
  `/<lang>/`. Each carries `hreflang` alternates for all twelve plus
  `x-default` (English). `zh` is `zh-Hans`, `pt` is `pt-BR`. Arabic pages are
  `dir="rtl"` with Western digits; the stylesheet uses logical properties
  (`margin-inline-end`, `padding-inline-start`, …) so both directions work.
- **Support, Company and the invite page (`i/`) stay English.** Their language
  list links each language's home.

**These pages are GENERATED — edit the sources, then run**
`python3 tools/build_pages.py /path/to/Sackgram-app`:

| Page | Source |
|---|---|
| Home `/`, `/<lang>/` | `tools/home/<lang>.json`. **ko is the original** (Sackgram-app `docs/website/SACKGRAM-소개문구-초안.docx`, part 2); every other language is its translation and must say the same thing — change ko first. Terms follow each language's app strings (ARB). Cross-review copies for the translations are in Sackgram-app `docs/website/` |
| Privacy, Terms | the app repository's `docs/legal/privacy-en.md`, `terms-en.md`, `review-ko/*-ko.md` and `i18n-drafts/<lang>/*.md`, converted to HTML verbatim — the same text the app ships in `apps/mobile/assets/legal/`. **Edit the Markdown there, never the HTML here** |
| Delete account (`/<lang>/delete-account/`) | that language's Privacy Policy 7-2, 7-3, 6-8, 6-9, 6-10, 6-1, 6-2 and 6-3, quoted verbatim under the page's own headings |
| Delete account (English, `/delete-account/`) | hand-written from the English policy's 6-8, 6-9, 6-10, 7-2 and 7-3; the build regenerates only its header and footer. It must change when those paragraphs do |

The header and footer labels (and the delete page's headings) are the `T`
table at the top of `tools/build_pages.py`; account words there are the app's
own ARB strings.

## Content rules used here, worth keeping

⚠ **2026-10-06: the "Why Sackgram exists" section below is RETIRED.** The app's
About screen was restructured on 2026-10-05 (#578) and no longer carries it,
and the home page now carries the long introduction Eric approved on
2026-10-05 instead (the Korean original at `/ko/`; English at `/` and ten more
languages since 2026-10-06 — see "Twelve languages" above). All twelve home
pages must say the same thing. The note is kept as the record of why the
section existed.

- **The "Why Sackgram exists" section is one statement kept in three places.**
  It is on this page under the hero, at the top of the app's About screen, and
  in section **J** of the app repo's `docs/legal/claims-register.md`. The site
  carries only the English; the Korean of the same statement lives in the app
  and in that register, and its title is **"SACKGRAM은 왜 존재하는가"** — with
  the product name in Latin letters, never `색그램`, because Korean
  user-facing copy was unified on SACKGRAM on 2026-09-20 and the glossary
  marks it DO NOT TRANSLATE. Named here so that a Korean page added to this
  site later starts from the right spelling. Editing
  one copy without the other two does not produce a better sentence, it
  produces three different claims — which is the thing the register exists to
  prevent. Approved as a whole on 2026-09-22; quote it whole.
  ⚠ Two things in it are deliberate and were argued over. It says what you
  **say** should be seen by no one — not who you talked to, because the server
  does see which accounts share a room (register H1), and the sentence after it
  claims the structure delivers the belief. And it says the content **stays**
  on our servers only as ciphertext, not that it "reaches" them that way: both
  were true, but the two languages were then making claims of different width.

- **What a feature does, never how it does it.** "End-to-end encrypted
  messages", not the key exchange or cipher.
- **No overclaiming.** Nothing says you cannot be tracked, or that no logs
  exist. The Privacy Policy explicitly states that infrastructure providers
  receive IP addresses, that message *metadata* is visible to us, and that a
  lost device is unrecoverable. A policy that omitted those would be
  misleading, and misleading is the one thing that actually creates risk here.
- **"No phone number or email address required" is stated,** because it is true.
  ⚠ Both halves, always. Signing up asks for neither, and saying only "phone
  number" is an UNDERSTATEMENT — which is still an inaccuracy, because it
  describes the product as asking for more than it does. The body copy on the
  site already said both; the meta description, the `<h1>` and the bold lead-in
  did not, and those are the three lines people actually quote. Fixed
  2026-09-21. See the app repo's `docs/legal/claims-register.md` B1.

## Colours

Brand cyan `#3BC3DE`, matching the app icon. It measures 2.09:1 against white,
so it is **never** used for text on a light background — only as a filled
block (dark text on it measures 7.07:1) or as a rule. Links use `#0B6B7C`
(6.16:1). Do not "fix" the links to brand cyan; that would fail contrast.
