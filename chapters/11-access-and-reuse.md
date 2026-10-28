# 11. Controlling access and enabling reuse

A reader can find the right delivery dataset and still lack permission to use it for a particular purpose. Metadata should explain that boundary, identify who decides, and connect the decision to controls that enforce it. The same records can help another reader reuse an approved dataset without guessing its meaning.

## Decide who may do what

Delivery Operations needs parcel records to investigate late arrivals. A request to use those records for an unrelated marketing analysis needs its own decision. Membership of a team does not settle every permitted use.

A **classification** describes the handling category, such as restricted. A **permitted purpose** states the approved use. Neither is a database permission. The following record is an illustrative policy decision, not a claim about controls tested in the incident simulation.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative access decision</span><span class="record-source">deliveries · operations investigation</span></figcaption>
<dl>
<div><dt>Classification</dt><dd>Restricted operational data; delivery identifiers and times can expose individual activity</dd></div>
<div class="record-focus"><dt>Permitted purpose</dt><dd><strong>Investigating delivery performance; approved Delivery Operations analysts may read necessary parcel records</strong></dd></div>
<div><dt>Approval</dt><dd>Delivery Operations data owner approves purpose and scope; privacy or security reviewers assess requests requiring their review</dd></div>
<div><dt>Implementation</dt><dd>Identity administrator assigns the approved group; database administrator grants scoped read access; catalogue operator applies metadata visibility rules</dd></div>
<div><dt>Export condition</dt><dd>Managed investigation workspace only; onward sharing needs a separate decision</dd></div>
<div><dt>Review trigger</dt><dd>Purpose change, role change or expiry of the investigation's approval</dd></div>
</dl>
</figure>
<p class="evidence-reading"><strong>What this establishes</strong> The record names the decision maker, approved use and people responsible for applying controls.</p>
<p class="evidence-limit"><strong>What still needs evidence</strong> A restricted label does not enforce access or establish compliance. Effective grants and tests with representative accounts show which paths are controlled.</p>

Identity controls establish who is connecting. Database grants, views and row or column restrictions determine which data that identity can read. Catalogue permissions govern discovery and descriptions. API credentials and service accounts need corresponding scopes. Export controls govern the destination and handling of downloaded copies. Revoking a database grant cannot retrieve a spreadsheet already downloaded.

Record the approval reference beside each implemented control. Check direct database access, catalogue search, API retrieval and exports with permitted and restricted identities. Recheck after role or interface changes. Technical access can limit available records; it rarely proves why an authorised person used them.

## Protect the evidence itself

The investigation's saved SQL might embed a delivery identifier in a filter. A sample attached to a quality result might reproduce a customer's details. Before collection, decide whether these fields are necessary: replace literals with parameters, use synthetic samples and restrict the original diagnostic material where it must be retained. Check search indexes and exported records for the transformed values too. Removing a sample from its catalogue page does not remove an indexed or downloaded copy.

## Keep evidence for an agreed period

Reproducing the 13:00 report could require its input snapshot, calculation version and publication records. Keeping everything indefinitely also preserves information whose approved purpose has ended. Define retention by artifact and purpose, including copies, rather than assigning one expiry date to a dataset's catalogue entry.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative retention policy</span><span class="record-source">Delivery investigation evidence</span></figcaption>
<dl>
<div><dt>Parcel snapshots</dt><dd>Delete 30 days after investigation closure</dd></div>
<div><dt>Managed exports</dt><dd>Expire after 7 days; remove related working copies at closure</dd></div>
<div><dt>Catalogue caches and indexes</dt><dd>Refresh or purge affected content within 24 hours of source deletion</dd></div>
<div class="record-focus"><dt>Audit metadata</dt><dd><strong>Keep approval reference, artifact identifier, action, actor reference and time for 180 days; exclude parcel values and query literals</strong></dd></div>
<div><dt>Calculation history</dt><dd>Keep code and non-sensitive measure definitions for one year</dd></div>
</dl>
</figure>

These periods are invented policy choices, not legal requirements. An organisation must determine appropriate periods and exceptions for its circumstances. The owner records the start event and deletion responsibility; operators include replicas and backups in the deletion procedure and document when remaining copies expire.

Once a snapshot is deleted, the retained metadata can explain which input was used without enabling an exact rerun. State that limitation. A deletion record supports an audit of the action; it does not prove that every unmanaged copy disappeared. Minimise audit fields and review their retention separately because actor references can themselves identify people.

## Describe a planned research release

Research publication introduces another audience. Consider a separately generated, wholly synthetic parcel dataset for demonstrating denominator choices. This example does not authorise publication of operational customer records.

The [FAIR principles](https://www.go-fair.org/fair-principles/) describe data that are **Findable, Accessible, Interoperable and Reusable**. Persistent identifiers and searchable descriptions support finding; documented retrieval and access conditions support access. Shared formats and vocabularies support interpretation across systems. Licensing, provenance and version information support reuse.

<figure class="metadata-record">
<figcaption><span class="record-kind">Illustrative research publication record</span><span class="record-source">Synthetic delivery measures · version 1.0</span></figcaption>
<dl>
<div><dt>Identifier status</dt><dd><code>https://example.org/datasets/synthetic-deliveries/v1</code> is an illustrative placeholder on a reserved domain, not a minted persistent identifier. A repository would assign the persistent identifier before publication.</dd></div>
<div><dt>Citation</dt><dd>Example Research Team (2026). <em>Synthetic delivery measures</em>, version 1.0. Example Repository. Persistent identifier pending.</dd></div>
<div><dt>License and access</dt><dd>Proposed CC BY 4.0 license for synthetic data and metadata; planned public HTTPS download. No release has occurred.</dd></div>
<div class="record-focus"><dt>Provenance and meaning</dt><dd><strong>Generated from invented parcels using generator version 1.0; no customer records. Population: all deliveries due by noon against their original promises. UTC timestamps; missing completion time means unfinished.</strong></dd></div>
<div><dt>Machine-readable description</dt><dd>Planned JSON metadata using DataCite property names; versioned field dictionary and controlled status terms <code>unfinished</code>, <code>on_time</code> and <code>late</code></dd></div>
</dl>
</figure>

The [DataCite metadata schema](https://schema.datacite.org/) provides properties for identifiers, versions, rights and related resources. Naming those properties does not demonstrate a valid deposit. Verify the repository's requirements and the release files before publishing; journals, funders and institutions may impose additional conditions.

FAIR does not require public access: authentication and a documented approval route can be appropriate. It also does not guarantee data quality or legal compliance. If data are withdrawn, retaining a minimal discovery record with the identifier, withdrawal status and reason may preserve citations, but only where appropriate under the applicable access and retention decisions.

## Core points

- **Record purpose, scope and approval.** Connect the decision to controls on every access path.
- **Protect metadata and copies.** Samples, queries, indexes and exports need deliberate handling.
- **Retain by purpose.** State what deletion prevents you from reproducing.
- **Make reuse explicit.** Identifiers, versions, licenses and provenance help; FAIR alone grants no permission.
