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
