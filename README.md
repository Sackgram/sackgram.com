# sackgram.com

The public website for Sackgram Labs, Inc. Plain static HTML and one CSS file
— no build step, no JavaScript, no external requests (no fonts, no analytics,
no CDN). Open any `.html` file in a browser to preview it exactly as it will
be served.

## Company details as published

| Field | Value |
|---|---|
| Company name | Sackgram Labs, Inc. |
| Principal place of business | 156 Botany Bay Blvd, North Charleston, SC 29418, United States |
| State of incorporation | Delaware, United States |
| Effective date on legal pages | August 26, 2026 |
| Governing law | State of Delaware, United States |
| Venue | State of Delaware, United States |

### ⚠️ Use the business address, never the registered agent's

The Delaware registered agent address (251 Little Falls Drive, Wilmington —
Corporation Service Company) must **not** appear anywhere on this site. Apple
and Google both want the real place of business, and **Google explicitly
rejects registered-agent addresses**. The company page is labelled
"Principal place of business" for exactly this reason — the term "registered
address" means the agent's Delaware address to a US reader, which is the
opposite of what is wanted here.

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
index.html            Home — what the app does, company name
privacy/index.html    Privacy Policy   -> /privacy   (required by both app stores)
terms/index.html      Terms of Service -> /terms
support/index.html    Support          -> /support   (required by both app stores)
company/index.html    Legal entity and address -> /company
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

**`sha256_cert_fingerprints` is a list and must hold BOTH keys.** Under Play
App Signing the certificate a real user's installed app carries is **Google's
app signing key**, not the upload key you sign with locally. Listing only the
upload key means everything works in a locally built release APK and fails for
every single person who installs from the Play Store — the worst shape this
failure can take, because testing does not reveal it.

| Key | Fingerprint starts | What carries it |
|---|---|---|
| Google app signing key | `E3:82:D2:EB…` | Every Play-installed build |
| Upload key | `C5:0F:A8:AD…` | A release APK built and installed locally |

Both come from **Play Console → Test and release → Setup → App integrity →
App signing**, in the same colon-hex form `keytool` prints.

⚠ **Never add the debug keystore's fingerprint here.** The debug key is
unprotected by design and sits on every machine that has ever built the app;
treating it as proof of identity for this domain is not a trade worth making.
(The app's *server* accepts a debug fingerprint in its own private allow-list
for `flutter run` testing — a different surface, not this one.)

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

## Content rules used here, worth keeping

- **What a feature does, never how it does it.** "End-to-end encrypted
  messages", not the key exchange or cipher.
- **No overclaiming.** Nothing says you cannot be tracked, or that no logs
  exist. The Privacy Policy explicitly states that infrastructure providers
  receive IP addresses, that message *metadata* is visible to us, and that a
  lost device is unrecoverable. A policy that omitted those would be
  misleading, and misleading is the one thing that actually creates risk here.
- **"No phone number required" is stated,** because it is true.

## Colours

Brand cyan `#3BC3DE`, matching the app icon. It measures 2.09:1 against white,
so it is **never** used for text on a light background — only as a filled
block (dark text on it measures 7.07:1) or as a rule. Links use `#0B6B7C`
(6.16:1). Do not "fix" the links to brand cyan; that would fail contrast.
