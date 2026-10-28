# 10. Managing definitions and dataset changes

A definition can be correct today and unsuitable tomorrow. A producer may add a field, a business team may change a measure, or responsibility may move to another team. Metadata should make the decision, its timing and its consequences visible to people using the data.

Chapter 7 raised a possible change to `promised_at`: replacing the original customer promise with the latest revised promise. This chapter develops that **separate, hypothetical scenario**. The records below illustrate a review and an approved alternative; they are not changes made to the book's database or additional incident results.

## Review meaning as well as structure

A parcel arriving at 12:20 is late against an original noon promise but on time against a revised 12:30 promise. Changing the promise can also change whether the parcel belongs among deliveries due by noon. Keeping the column's name and type would preserve its schema while breaking consumers' agreement about its meaning.

**Semantic compatibility** means existing consumers can still rely on the agreed meaning. A schema comparison cannot establish this. Even adding a field needs review if it changes row counts, required values or delivery commitments.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative change proposal</span><span class="record-source">Promise review · C17</span></figcaption>
<dl>
<div><dt>Dataset</dt><dd><code>prod/parcels/deliveries</code>; agreement <code>deliveries-v1</code></dd></div>
<div class="record-focus"><dt>Proposed change</dt><dd><strong>Replace the meaning of <code>promised_at</code> with the latest revised customer promise</strong></dd></div>
<div><dt>Status</dt><dd>Pending review; no permission to publish under the proposed meaning</dd></div>
<div><dt>Potential effects</dt><dd>On-time classification and membership of the all-due denominator</dd></div>
<div><dt>Required reviewers</dt><dd>Reporting engineer, Delivery Operations and Service Analytics</dd></div>
</dl>
</figure>

A pending proposal belongs beside the current agreement, with an explicit status. Editing the current definition immediately would make an unapproved intention look like the rule already in force.

## Give each decision an accountable owner

The reporting engineer, acting as producer, explains what can be supplied and checks implementation, retained inputs and publication. Delivery Operations and Service Analytics, as consumers, decide whether their measures still answer their questions and identify dependent reports. Each accepts a migration plan for its uses.

A metadata steward coordinates the review, checks that versions and evidence remain connected, and follows up unresolved consumers. The steward does not choose a business definition on a consumer's behalf. Here, Delivery Operations owns the all-due definition; Service Analytics owns the completed-delivery definition.

The dependency path through `build_delivery_summary`, `delivery_summary` and Delivery performance supplies a starting list. The review must record which systems and reporting periods were examined and who investigated spreadsheets or other unrecorded uses. A visible dependency is evidence of a use; an empty dependency list is not evidence that nobody uses the field.

## Approve a version with an effective date

The safer alternative preserves `promised_at` and adds `revised_promise_at`, explicitly defined as the latest accepted revision known at the snapshot cutoff, empty when no revision exists. Consumers must choose which promise their measures use. Adding the field does not automatically migrate them.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative approved decision</span><span class="record-source">C17 · Alternative accepted</span></figcaption>
<dl>
<div class="record-focus"><dt>Agreement</dt><dd><strong><code>deliveries-v2</code> adds <code>revised_promise_at</code>; <code>promised_at</code> retains its original-promise meaning</strong></dd></div>
<div><dt>Approval and effect</dt><dd>Producer and both consuming teams approve on 2 November 2026; effective for snapshots from 5 November 2026 at 13:00 UTC</dd></div>
<div><dt>Consumer evidence</dt><dd>Attach each team's reviewed query and report references, chosen promise rule (including whether an absent revision falls back to the original promise), acceptance and migration date</dd></div>
<div><dt>Release condition</dt><dd>Publish only after the steward confirms those attachments and the producer supplies validation results and a rollout plan</dd></div>
<div><dt>Current release status</dt><dd>Approved design; release pending the required evidence</dd></div>
</dl>
</figure>

Approval settles the design, while release remains conditional. The illustrated record supplies no validation results. After release, attach the actual run, input, output and report refresh references; a planned date alone cannot prove consumers received the change.

The dataset identifier continues to identify the production dataset. Contract versions describe successive agreements; definition versions identify particular measurement rules; publication identifiers identify particular outputs. They serve different purposes. Retaining a physical table does not make a changed meaning compatible, and creating a new table does not by itself explain that meaning.

## Preserve responsibility and history

If ownership transfers, retain the former owner, the new team's explicit acceptance and the effective date. Until acceptance, the transfer is pending. Deprecating an old meaning similarly needs a named replacement, affected consumers, notice and a retirement date agreed with those consumers. Keeping the original field available gives them time to migrate deliberately.

Whether to recalculate history is a policy decision for the definition owner and affected consumers. They may preserve reports under their original rules, or publish a restated series under an approved new definition. A restatement needs a new publication identifier linked to the superseded output, definition version, retained inputs, code and approval. Preserve the earlier report and explain the revision; overwriting it would remove the evidence needed to explain what readers saw at the time.

## Core points

- **Review meaning, not just schema.** An unchanged column can break an agreement.
- **Separate proposal, approval and release.** Record dates, responsible parties and consumer evidence.
- **Version agreements and publications explicitly.** Dataset identity does not describe every change.
- **Preserve accepted ownership and historical decisions.** Restatement requires a traceable revised publication.
