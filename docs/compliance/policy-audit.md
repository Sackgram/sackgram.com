# Policy audit — published documents vs. implementation

Audited 2026-09-18 against `Sackgram/Sackgram-app` at `130e4a8` (all of that
day's merges) and `Sackgram/sackgram.com` at `d2c8b12`.

**What this document is.** Every claim below was checked by reading the
implementing code, not by recalling what the feature is supposed to do. Where
the code could not settle a question, the verdict is **확인 불가** and says what
would settle it.

**What it is not.** It is not a rewrite. No code was changed in this pass, and
the suggested wordings are drafts for a human to accept, edit or reject.

**⚠ Status of the findings.** The audit itself was run against the pages as
they stood at `d2c8b12`. The PR that adds this file also applies four of the
fixes — **2.3** (recovery), **4.5** (LiveKit), **2.2/2.4** (password reset) and
**5.1** (Voice Privacy wording). Every other finding below is **still open** and
the table in "Summary of findings" is the working list. This file is not
rewritten as fixes land: it is the record of what was found, and the summary
table says what has been done.

**Method note.** A claim about deletion was checked against the code that
deletes, and a claim about what is stored was checked against the code that
writes. Several findings below are cases where the document is *more modest
than the implementation* — those are listed too, because a privacy policy that
under-describes what is held is as wrong as one that over-promises, and it is
the kind that fails an audit rather than merely embarrasses.

**Verdict vocabulary**

| | |
|---|---|
| **정확** | The document matches the implementation. |
| **부정확** | The document says something the implementation does not do. |
| **과잉기재** | The document claims to hold or do more than it does. |
| **누락** | The implementation does something the document does not disclose. |
| **확인 불가** | Not decidable from the code alone; what would decide it is named. |

---

## 1. Contact removal — "deletes that conversation's history for both people"

### 1.1 The core claim

| | |
|---|---|
| **문장** | "remove a contact — which deletes that conversation's history for both people" |
| **위치** | Privacy §4 "How long we keep it"; Support "Deleting your data yourself" (3rd bullet, "Remove a contact, which also deletes that conversation's history for both people") |
| **실제 구현** | `FriendListRepository.removeFriend()` (`apps/mobile/lib/features/friends/domain/friend_list_repository.dart`). One batch deletes **both** friend documents and marks the conversation `dissolved: true`; then `EvaporationService.wipeConversation()` deletes **every message document and every Cloud Storage object** the conversation referenced; then the call documents and read receipts are purged; then the conversation document itself is deleted. All of it is **server-side**. There is no local message database in the app (no sqflite/hive/drift/isar in `pubspec.yaml`), so a message exists in exactly two places: Firestore, and each device's Firestore cache. |
| **판정** | **정확, 단 조건부** — the server-side deletion is real and complete, but "for both people" describes the *server*, and the peer's device catches up only when it next reaches Firestore. |
| **권고 문구** | Keep the promise; add the condition. See 1.2–1.4 for the three things it does not cover. |

### 1.2 Does it delete from the other person's device?

| | |
|---|---|
| **문장** | (implied by "for both people") |
| **위치** | Privacy §4; Support |
| **실제 구현** | Nothing in `removeFriend()` reaches the peer's device. The mechanism is that the peer's app renders from a Firestore stream, and the documents are gone. Firestore's on-device cache is not disabled anywhere (`persistenceEnabled` appears nowhere in `apps/mobile/lib`), so mobile default persistence is ON: the peer holds a local cached copy until their client syncs the deletions. |
| **판정** | **부정확 (정도의 문제)** — true once the peer syncs, not true at the moment you press the button. |
| **권고 문구** | "Removing a contact deletes that conversation from our servers — the messages, and any photos, videos or files in it. The other person's app removes its copy the next time it connects. Until then their device still has what it had already received." |

### 1.3 If the other person is offline

| | |
|---|---|
| **문장** | (not addressed) |
| **위치** | — |
| **실제 구현** | No expiry on the local cache, and no "tombstone" push. The peer keeps the cached conversation for as long as they stay offline. On reconnect the deletions arrive and the cache is emptied. If they never reconnect — the app is uninstalled, the phone is discarded — the cache dies with the app's data, not because Sackgram removed it. |
| **판정** | **누락** |
| **권고 문구** | Covered by the wording in 1.2 ("the next time it connects"). No separate sentence needed, but the policy must not say "immediately" or "for both people" without it. |

### 1.4 ⚠ Files the other person already opened

| | |
|---|---|
| **문장** | (not addressed) |
| **위치** | — |
| **실제 구현** | Opening a file attachment (`file_open_service_native.dart`) and playing a video (`video_playback_service_native.dart`) write the **decrypted** bytes to the device's temporary directory (`getTemporaryDirectory()` → Android `getCacheDir()`). `TempFileCleaner.wipe()` empties that directory, but it is called from exactly two places, both in `account_deletion_service.dart` — **account deletion only**. Removing a contact does not call it. |
| **판정** | **부정확** — a decrypted copy of any file or video the other person opened survives contact removal on their device. |
| **권고 문구** | "If the other person opened a file or played a video you sent, their phone may still hold the copy it made in order to open it. Deleting the conversation does not reach that copy." Same sentence belongs in Support, where the claim is phrased as advice. |

### 1.5 Suggested replacement, both locations

> **Remove a contact.** This deletes the conversation from our servers — every
> message in it, and any photos, videos or files it contained. The other
> person's app removes its copy the next time it connects to the internet;
> until then, their device still holds what it had already received. If they
> opened a file or played a video you sent, the copy their phone made in order
> to open it is not reached by this.

---

## 2. Authentication and recovery

### 2.1 "You choose a SACKGRAM ID and a password when you sign up"

| | |
|---|---|
| **문장** | "You choose a SACKGRAM ID and a password when you sign up. Both are held on your device" |
| **위치** | Terms §2 |
| **실제 구현** | Accurate. `AuthService._registerNewIdentity({sackgramId, password})` hashes the password and writes the hash to `flutter_secure_storage` under `password_hash`. Not a PIN; not biometric-only. Biometrics are a *resume* path on top (`BiometricAuthService` + `_tryBiometricResume` in `auth_screen.dart`), not the enrolment credential. |
| **판정** | **정확** |
| **권고 문구** | No change. |

### 2.2 ⚠ "we do not store your password and cannot reset it for you"

| | |
|---|---|
| **문장** | "we do not store your password and cannot reset it for you" |
| **위치** | Terms §2 |
| **실제 구현** | The first half is right: only a hash, only on the device. **The second half is not.** `same_phone_account_screen.dart` declares `enum SamePhoneAccountAction { biometric, resetPassword }`, and `auth_screen.dart` routes `SamePhoneAccountAction.resetPassword` → `_openRecovery()` → `PasskeyRestoreScreen`. A user who has forgotten their password, on the same phone, can get back into the account with their SACKGRAM ID and a fingerprint. |
| **판정** | **부정확** |
| **권고 문구** | "We never see your password — only your own device holds it, and only as a hash. **We** cannot reset it for you. If you set up a passkey, **you** can get back into your account on a phone that has it, using your SACKGRAM ID and your fingerprint, without the old password." |

### 2.3 ⚠ "We do not offer account recovery today"

| | |
|---|---|
| **문장** | "We do not offer account recovery today. If you lose your device, the account is gone with it. We may offer some form of it in future; if we do, this policy will say so before it becomes available." |
| **위치** | Privacy §8 |
| **실제 구현** | `PasskeyRestoreScreen` is real, reachable from two places in `auth_screen.dart`, and its own header states what returns: **the account, the SACKGRAM ID and the friend list**. Conversations do not, and groups need re-invitation. Server side, `backend/signaling/src/recovery_passkey.ts` implements `beginRecovery`/`completeRecovery`. |
| **판정** | **부정확** — and this is the one sentence in the published set that promises the *opposite* of what ships. Note the policy's own commitment: "if we do, this policy will say so **before** it becomes available." |
| **권고 문구** | Replace §8's second half with: "**Getting back into your account** is a separate question from getting your conversations back. If you set up a passkey, you can restore your account on a new phone with your SACKGRAM ID and your fingerprint: your identity, your SACKGRAM ID and your contact list come back. Your past conversations do not — their keys were on the lost phone — and groups have to invite you again. If you did not set up a passkey, or your phone or account cannot support one, there is no way back into the account." |
| **⚠ 부수 확인** | The same header records the accepted cost: Android below 9, iOS below 16, and anyone without a Google or Apple account cannot use a passkey and has **no route back at all**. The published documents say nothing about this, and the replacement wording above is written to carry it. |

### 2.4 "losing your device means losing your account and your conversation history permanently"

| | |
|---|---|
| **문장** | Terms §2, "Read this before you rely on Sackgram" |
| **위치** | Terms §2 |
| **실제 구현** | The conversation-history half is correct and is strongly supported by the code. The account half is contradicted by 2.3. |
| **판정** | **부정확 (부분)** |
| **권고 문구** | "losing your device means losing your conversation history permanently. We cannot restore it. Whether you can get the **account** back depends on whether you set up a passkey — see our Privacy Policy, section 8." |

---

## 3. Message and attachment metadata

### 3.1 What is actually unencrypted in a message document

`ConversationService.sendMessage()` writes these fields to
`conversations/{id}/messages/{id}`. Everything except `text` is plaintext:

| Field | Plaintext? | Disclosed in §1.2? |
|---|---|---|
| `senderId` | yes | yes ("which accounts are in a conversation") |
| `text` | **no** — ciphertext | yes ("stored only in encrypted form") |
| `type` | yes — `text`/`image`/`file`/`video`/`call_summary` | **no** |
| `storagePath`, `storagePaths`, `thumbnailStoragePath` | yes | no (harmless — see 3.3) |
| `fileName` | **yes** | yes |
| `fileSize` | yes | yes, but see 3.2 |
| `fileExtension` | **yes** | **no** |
| `timestamp` | yes | yes |
| `expiresAt` | **yes** | **no** |

For a `call_summary` row the server additionally writes `callerUid`,
`callOutcome` and `callDurationSeconds` in plaintext.

| | |
|---|---|
| **판정** | **누락** — three disclosable facts are missing: the message **type**, the **file extension**, and the **disappearing-message expiry time**. `type` is the most meaningful: it reveals whether a given message was text, a photo, a video, a file or a call. |
| **권고 문구** | Extend §1.2's second bullet: "…which accounts are in a conversation, when each message was sent, what kind of message it was (text, photo, video, file, or a record of a call), how large it is, when it is set to disappear if you set a timer, and — for file and video attachments — the original file name and extension. These are not encrypted." |

### 3.2 "roughly how large they are"

| | |
|---|---|
| **문장** | "roughly how large they are" |
| **위치** | Privacy §1.2 |
| **실제 구현** | For file and video attachments `fileSize` is the **exact** byte count, written as an integer. For other messages the size is whatever the ciphertext length implies. |
| **판정** | **부정확 (과소 기재)** — "roughly" understates it. This is the direction that matters in an audit: the policy claims to hold less than it does. |
| **권고 문구** | Fold into 3.1's replacement — "how large it is", and for attachments the exact size follows from `fileSize` being named. |

### 3.3 Cloud Storage paths and the original file name

| | |
|---|---|
| **문장** | "for file attachments the file name and size, which are not encrypted" |
| **위치** | Privacy §1.2 |
| **실제 구현** | Two separate facts, and they differ. **Storage object names carry no user data**: `ImageMessageService` uploads to `<prefix>/<conversationId>/<uuid v4>.enc`, and the bytes are ciphertext. **The Firestore document does carry the original name**: `chat_screen.dart` passes `fileName: picked.name` straight through, unencrypted. |
| **판정** | **정확** — the claim is true, and the part a reader might fear (the file name in the storage path) does not happen. |
| **권고 문구** | Optional, and worth it because it is a genuine strength stated modestly: "Attachments are stored under a random identifier, not under their file name; the file itself is encrypted. The original file name is recorded alongside the message and is not encrypted." |

### 3.4 Over-disclosure check

| | |
|---|---|
| **판정** | **과잉기재 없음.** Every category §1.2 claims is genuinely held. The errors in this section all run the other way. |

---

## 4. Calls

### 4.1 Call records held on the server

| | |
|---|---|
| **문장** | "We hold call records: who called whom, when the call started and ended, and whether it was answered." |
| **위치** | Privacy §1.4 |
| **실제 구현** | **1:1** — `conversations/{id}/calls/{callId}`: `callerUid`, `calleeUid`, `status`, `offer`, `answer`, `connectedAt`, `endedAt`, `callerSpeakerphoneOn`, `calleeSpeakerphoneOn`, plus `callerCandidates`/`calleeCandidates` subcollections. **Group** — `startedByUid`, `status`, `startedAt`, `firstJoinedAt`, `joinedIdentities`, `emptiedAt`. **Storefront** — the same plus `ownerUid`. **Thread summary** (survives the call) — `callerUid`, `callOutcome`, `callDurationSeconds`. |
| **판정** | **누락 (둘)** — (a) **`callerSpeakerphoneOn` / `calleeSpeakerphoneOn`**: whether each party had their loudspeaker on is held server-side during a call and is not mentioned anywhere; (b) **`joinedIdentities`**: for a group or storefront call the server records **who joined**, which is more than "who called whom". |
| **권고 문구** | "We hold call records: who called whom, when the call started and ended, whether it was answered, how long it lasted, and — for a group or shop call — which accounts joined. While a call is in progress we also hold whether each side has their loudspeaker on, so the other person can be shown it; it is cleared when the call ends." |

### 4.2 ⚠ `lastMissedCallAt`

| | |
|---|---|
| **문장** | (not addressed) |
| **위치** | — |
| **실제 구현** | Added 2026-09-18 and **deployed**. `finishCustomerCall()` in `backend/signaling/src/customer_call_session.ts` writes `lastMissedCallAt` onto `groups/{groupId}/customers/{customerUid}` when a shop call ends unanswered. It is **not** deleted when the call ends — it persists on the customer row until overwritten by the next unanswered call, and it is never cleared. |
| **판정** | **누락** — a persistent, dated record that a specific customer called a specific shop and was not answered, held indefinitely. §4 "How long we keep it" has no row that covers it. |
| **권고 문구** | Add to §1.4: "For a shop, we record when a customer last called without being answered, so the shop owner can see it. It stays on that customer's record until they call unanswered again." And to §4: "**A shop's record of unanswered calls** stays for as long as the customer's connection to that shop does." |

### 4.3 IP addresses — "We delete them once the call ends"

| | |
|---|---|
| **문장** | "Those addresses reach our servers … We delete them once the call ends." |
| **위치** | Privacy §1.4, and §4 "Call network addresses are deleted when the call ends" |
| **실제 구현** | Substantially true for 1:1. `CallSignalingService.deleteFinishedCall()` deletes the `callerCandidates` and `calleeCandidates` subcollections **before** deleting the call document — the ordering matters, because deleting a Firestore document does not delete its subcollections. **The client does the deleting**, and it can fail: the app is swiped away mid-call, the Flutter engine is gone, the write is refused. `sweepFinishedCalls` in `ring_timeout_sweep.ts` is the server-side backstop, and its own header calls itself "a BACKSTOP, not the primary mechanism". |
| **판정** | **정확, 단 불완전** — "we delete" reads as though the server does it promptly and unconditionally. It is the caller's phone that does it, and a failure leaves the addresses until a sweep runs. |
| **권고 문구** | "We delete them when the call ends. This normally happens as the call finishes; if a device fails to complete it — for example the app was closed mid-call — a routine server clean-up removes them shortly afterwards." |

### 4.4 ⚠ Relay wording does not cover group and shop calls

| | |
|---|---|
| **문장** | "Where the two devices can reach each other over the network, it passes between them without going through us. Where they cannot, a call may need to be carried by a relay server" |
| **위치** | Privacy §1.4 |
| **실제 구현** | That describes the **1:1** path only. **Every group call and every shop call goes through a media server, always** — `LIVEKIT_HOST = 'https://sackgram-0elowh08.livekit.cloud'` (`backend/signaling/src/group_call.ts`). There is no peer-to-peer path for those two. "may need to be" is not true of them. |
| **판정** | **부정확** |
| **권고 문구** | "How the audio travels depends on the kind of call. A one-to-one call passes directly between the two devices where the network allows it, and through a relay server where it does not. **A group call or a call to a shop always passes through a media server**, which is how calls with more than two people work. In every case the audio is encrypted on your device before it is sent — see section 3 for who operates that server." |

### 4.5 ⚠ LiveKit is an undisclosed service provider

| | |
|---|---|
| **문장** | "We use Google Cloud Platform and Firebase (Google LLC) … We do not share your information with anyone else, except where section 5 applies." |
| **위치** | Privacy §3 |
| **실제 구현** | Group and shop calls run on **LiveKit Cloud**, a third party, at `sackgram-0elowh08.livekit.cloud`. ⚠ **Audio content is protected from it**: both `GroupCallSession` and `CustomerCallSession` construct the room with `e2eeOptions: lk.E2EEOptions(keyProvider: …)`, so frames are encrypted with a key derived from the group key and LiveKit carries ciphertext. What LiveKit does receive is real, though: participant identities, room identifiers, connection metadata including **IP addresses**, and the participant metadata string — which, per `core/call/call_participant_metadata.dart`, carries the **speakerphone (`sp`) and Voice Privacy (`vp`) flags**. |
| **판정** | **부정확** — §3 as written is a closed list, and it is missing a provider that handles call traffic for two of the three call types. |
| **권고 문구** | Add to §3: "We use **LiveKit** (LiveKit, Inc.) to carry the audio of group calls and calls to shops. The audio is encrypted on your device before it reaches them and they cannot listen to it. They do handle the connection itself, which means they receive the network addresses of the devices on the call and which accounts are in the room." |
| **⚠ 후속** | §7's "call audio is end-to-end encrypted and travels between the two devices" is written for a two-party call and reads as false for a group. Suggest: "travels encrypted between the devices on the call". |
| **게시된 문안** | ⚠ **The 권고 문구 above is the record of what was recommended on the day of the audit, and is deliberately left as written. What actually shipped is different**: it names no call types at all. A processor disclosure needs the provider, its role and what it receives; which calls take that route is none of the three, and naming them dates the sentence. Settled in `e8ada52` on PR #4 — read `privacy/index.html` §3 for the live wording, not this row. |

---

## 5. Paid features

### 5.1 ⚠ "Voice Privacy is a paid feature"

| | |
|---|---|
| **문장** | "Voice Privacy is a paid feature that changes the pitch of your voice…" |
| **위치** | Terms §4 |
| **실제 구현** | Two separate problems. **(a) Against the confirmed pricing** — FREE 30 min / SILVER 300 min / GOLD unlimited — the feature is *not* paid: every user gets 30 minutes. **(b) Against the code**, neither the pricing nor any metering exists. `backend/signaling/src/usage_counters.ts` states in its own header that "Transfer volume and **Voice Privacy minutes** are stage 2 and are not here", and that file is marked `NOT deployed`. `FeatureEntitlementGate` (rewritten 2026-09-18) grants Voice Privacy at **silver or above** and refuses everyone below, with no minute allowance of any kind. |
| **판정** | **부정확** — against the intended pricing, and separately not implementable today. |
| **권고 문구** | ⚠ **Do not publish a minutes figure until the meter exists.** A published "30 minutes free" that the app does not count is a worse exposure than the current sentence. Two options: **(i) if the terms must be corrected now** — "Voice Privacy is a subscription feature." (accurate to the code as it stands, and does not promise a free allowance); **(ii) once metering ships** — "Voice Privacy is included in every account up to a monthly limit, and without limit on paid plans. Current limits are shown in the app." Naming the limits only in the app keeps the terms from going stale — the same reason §7 already refuses to print prices. |

### 5.2 Subscription, renewal, cancellation and refund terms

| | |
|---|---|
| **문장** | "Sackgram may offer paid subscriptions. If it does, purchases are made through the Apple App Store or Google Play … Refunds and cancellations are handled by the store you bought through, under its policy, not by us." |
| **위치** | Terms §7 |
| **실제 구현** | The clause exists and is conditional ("may offer"). It covers purchase channel, refunds and cancellation-by-store. |
| **판정** | **정확하나 불충분** — three things a subscription clause normally carries are **absent**: (a) that subscriptions **renew automatically** until cancelled; (b) **when** cancellation takes effect (end of the paid period, not immediately); (c) what happens to paid features **when a subscription lapses**. Apple and Google both require auto-renew disclosure in the terms, not only in the store listing. |
| **권고 문구** | Add to §7: "Subscriptions renew automatically at the end of each billing period until you cancel. You can cancel at any time in your App Store or Google Play account settings; cancelling stops the next renewal and you keep the subscription until the end of the period you have already paid for. When a subscription ends, paid features stop and your account returns to the free plan — your messages, contacts and groups are not affected." |
| **⚠ 참고** | The account-termination clause in Terms §1 ("any subscription attached to it ends with it") states a consequence without saying whether any refund follows. Under §7 that is the store's decision; saying so explicitly would remove the ambiguity. |

---

## 6. Automatic collection by SDKs

**What is in the build** (`apps/mobile/pubspec.yaml`): `firebase_core`,
`firebase_auth`, `firebase_messaging`, `firebase_storage`, `cloud_firestore`,
`cloud_functions`, `firebase_app_check`, `purchases_flutter` (RevenueCat),
`livekit_client`.

**Not in the build**: Firebase Analytics, Crashlytics, Performance Monitoring,
and any advertising or attribution SDK. ⚠ §1.7's "We do not use advertising or
tracking software development kits" is therefore **정확**, and §1.7's
"We do not build advertising or marketing profiles" is **정확**.

| Missing item | 실제 구현 | 판정 | 권고 문구 |
|---|---|---|---|
| **Firebase Authentication account record** | `firebase_auth` is the identity layer. Firebase Auth holds, per account, a uid, account creation time and last sign-in time — independent of the "randomly assigned account identifier" §1.1 describes. | **누락** | Add to §1.1: "When your account was created, and when it was last used to sign in." |
| **Firebase App Check** | `AppCheckService.activate()` runs in `main()`. App Check attests the app to Google's backend; on Android that is Play Integrity, which evaluates the device and the app install. | **누락** | Add to §1.6: "We use a Google service that checks requests genuinely come from the Sackgram app on an ordinary device. It reports a verdict about the app and the device to us; it does not tell us who you are." |
| **RevenueCat** | `purchases_flutter` is configured in `main()` and `Purchases.logIn(uid)` is called from both sign-in paths, so RevenueCat holds the Firebase uid alongside purchase state. | **누락 — ⚠ §3 은 Google 만 열거** | Add to §3: "If you buy a subscription we use **RevenueCat** (RevenueCat, Inc.) to keep track of whether it is active. They receive your account identifier and the subscription's status. They do not receive your payment card details, which stay with Apple or Google." |
| **LiveKit** | See 4.5. | **누락** | See 4.5. |
| **FCM token** | Disclosed in §1.5. | **정확** | — |
| **Infrastructure logs / IP** | Disclosed in §1.6, and unusually candidly. | **정확** | — |

⚠ **확인 불가** — whether Google Play Services' own telemetry (separate from
any SDK Sackgram ships) counts as collection attributable to Sackgram in a Play
Console declaration. That is a question for the Play policy text, not for this
repository, and it is not decidable from the code.

---

## 7. Play Console Data safety mapping

Each row is what the **implementation** supports. Rows marked ⚠ depend on a
finding above being fixed before the declaration would be truthful.

### Data collected (leaves the device to Sackgram or a processor)

| Play category | Data type | Collected? | Shared? | Purpose | Optional? | Source |
|---|---|---|---|---|---|---|
| App activity | Other user-generated content — message ciphertext | Yes | No | App functionality | Required | Firestore `messages.text` |
| Files and docs | Files and docs — attachment ciphertext | Yes | No | App functionality | Required | Cloud Storage `<uuid>.enc` |
| Files and docs | ⚠ **File names** | **Yes** | No | App functionality | Required | `messages.fileName`, plaintext (3.1) |
| Photos and videos | Photos, Videos — ciphertext | Yes | No | App functionality | Required | Cloud Storage |
| App info and performance | Other app performance data — App Check verdict | ⚠ **Yes** | Yes (Google) | Fraud prevention, security | Required | `AppCheckService` (§6) |
| Device or other IDs | Device or other IDs — FCM token | Yes | Yes (Google) | App functionality | Required | §1.5 |
| App activity | App interactions — call records, `joinedIdentities` | Yes | No | App functionality | Required | 4.1 |
| App activity | ⚠ App interactions — **`lastMissedCallAt`** | **Yes** | No | App functionality | Required | 4.2 |
| Personal info | User IDs — account identifier, SACKGRAM ID | Yes | ⚠ **Yes** (RevenueCat, LiveKit) | App functionality, Account management | Required | §1.1, 4.5, §6 |
| Contacts | — | **No** | — | — | — | No contacts permission; Friend List is app-local |
| Location | — | **No** | — | — | — | No location permission |
| Financial info | Purchase history | Yes | Yes (RevenueCat) | App functionality | Required | `purchases_flutter`; card details never reach Sackgram |
| Audio | Voice or sound recordings | **No** | — | — | — | Call audio is not recorded (§1.4, verified: no recording path) |

### Not "collected" under Play's definition (transient processing only)

| Play category | Data type | Note |
|---|---|---|
| Device or other IDs | IP address | ⚠ Play treats end-to-end-encrypted transient data as not collected only under narrow conditions. Call network addresses are **written to Firestore** and deleted afterwards (4.3), which is storage, not transit — declare as collected unless counsel says otherwise. |

### Security practices

| Question | Answer supported by the code |
|---|---|
| Data encrypted in transit | **Yes** — all Firebase/LiveKit traffic is TLS. |
| Users can request data deletion | **Yes** — in-app account deletion (`account_deletion_service.dart`) plus the email route in §6. |
| Committed to Play Families policy | N/A — 18+ only. |
| Independent security review | **No** — do not claim one. |

⚠ **Before submitting the form**, resolve 2.3 (recovery), 4.2
(`lastMissedCallAt`), 4.5 (LiveKit) and §6 (RevenueCat, App Check, Firebase
Auth). Three of those four are *undisclosed collection or sharing*, which is the
category Play rejects for.

---

## Summary of findings

| # | Item | 판정 | Priority |
|---|---|---|---|
| 2.3 | "We do not offer account recovery today" | 부정확 | **1 — the policy promises to say so first** |
| 4.5 | LiveKit absent from the provider list | 부정확 | **2 — undisclosed sharing** |
| 6 | RevenueCat, App Check, Firebase Auth record | 누락 | **2 — undisclosed collection** |
| 2.2 | "cannot reset it for you" | 부정확 | 3 |
| 4.2 | `lastMissedCallAt` undisclosed and never cleared | 누락 | 3 |
| 5.1 | "Voice Privacy is a paid feature" | 부정확 | 3 |
| 1.4 | Decrypted files survive contact removal on the peer's device | 부정확 | 4 |
| 4.4 | Relay wording misses the always-SFU group path | 부정확 | 4 |
| 1.2 | "for both people" is eventual, not immediate | 부정확(정도) | 4 |
| 3.1 | Message `type`, `fileExtension`, `expiresAt` undisclosed | 누락 | 5 |
| 5.2 | No auto-renewal / cancellation-effect clause | 불충분 | 5 |
| 4.1 | Speakerphone flags and `joinedIdentities` undisclosed | 누락 | 5 |
| 4.3 | "We delete them" — client deletes, sweep backstops | 정확하나 불완전 | 6 |
| 3.2 | "roughly how large" understates `fileSize` | 부정확(과소) | 6 |
| 1.1, 2.1, 3.3, 3.4, §1.7 | — | **정확** | — |

**No 과잉기재 was found.** Every error runs toward claiming less than the
implementation does, or toward describing a one-to-one call as though it were
the only kind. That is the better direction to be wrong in, and it is still
worth correcting: an under-description is what a regulator or a store reviewer
treats as undisclosed collection.

**Tone note.** Every suggested wording above keeps the documents' existing
habit of stating the limitation in the same sentence as the promise. None of
them introduces "zero-persistence", "RAM only", "unrecoverable" or
"anti-forensic" language, and none should: Sackgram runs on Firebase and
documents remain on servers.
