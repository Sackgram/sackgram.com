# sackgram.com

The public website for Sackgram Labs, Inc. Plain static HTML and one CSS file
— no build step, no JavaScript, no external requests (no fonts, no analytics,
no CDN). Open any `.html` file in a browser to preview it exactly as it will
be served.

## ⚠️ Fill these in before publishing

Five placeholders are deliberately left as `[[TOKENS]]` rather than guessed.
**A registered address and a jurisdiction on a legal page are not details to
invent** — Apple's entity verification and the app stores both check them, and
a wrong one is worse than a missing one.

| Token | Appears in | What it is |
|---|---|---|
| `[[REGISTERED_ADDRESS]]` | company, privacy, terms | The company's real registered address. Not a PO box if Apple's verification is the goal. |
| `[[JURISDICTION_OF_INCORPORATION]]` | company | e.g. "Delaware, United States" |
| `[[EFFECTIVE_DATE]]` | privacy, terms | The date you actually publish, e.g. "26 August 2026" |
| `[[GOVERNING_LAW_JURISDICTION]]` | terms §12 | e.g. "the State of Delaware, United States" |
| `[[VENUE_JURISDICTION]]` | terms §12 | Where disputes are heard |

Find them all with:

```bash
grep -rn '\[\[' *.html
```

**These documents have not been reviewed by a lawyer.** They describe what the
app actually does, accurately and conservatively, which is the right starting
point — but the liability, indemnity and governing-law sections in particular
should be reviewed by counsel in your jurisdiction before launch.

## Files

```
index.html     Home — what the app does, company name
privacy.html   Privacy Policy   (required URL for both app stores)
terms.html     Terms of Service
support.html   Support          (required URL for both app stores)
company.html   Legal entity and address
style.css      All styling
CNAME          Custom domain for GitHub Pages — do not delete
.nojekyll      Serve files as-is, skip Jekyll processing
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
