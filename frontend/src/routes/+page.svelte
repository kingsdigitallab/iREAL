<script lang="ts">
	import { DataHandler, Pagination, RowCount } from '@vincjo/datatables';
	import FacetDistribution from '$lib/components/FacetDistribution.svelte';
	import _ from 'lodash';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import SummaryCard from '$lib/components/SummaryCard.svelte';

	export let data: PageData;

	let handler: DataHandler;
	let rows;

	onMount(async () => {
		const results = await data.results;

		handler = new DataHandler(results.schools, { rowsPerPage: 5 });
		rows = handler.getRows();
	});
</script>

{#await data.results}
	<div aria-busy="true">Loading data...</div>
{:then results}
	<hgroup>
		<h2>Dashboard</h2>
		<p>
			A dashboard for displaying and exploring school related data as exported by the AI/ML
			processes.
		</p>
	</hgroup>
	<section>
		<hgroup>
			<h3>Summary</h3>
			<p>
				Overview of the data extracted from the school records. Shows couts for school records,
				keywords, topics, people, organisations and places.
			</p>
		</hgroup>
		<div class="grid">
			<SummaryCard title="School records" value={results.schoolsNames.length} />
			<SummaryCard title="Keywords" value={results.keywords.length} />
			<SummaryCard title="Topics" value={results.topics.length} />
		</div>
		<div class="grid">
			<SummaryCard title="People" value={results.people.length} />
			<SummaryCard title="Organisations" value={results.organisations.length} />
			<SummaryCard title="Places" value={results.places.length} />
		</div>
	</section>
	<section>
		{#if $rows}
			<hgroup>
				<h3>School records table</h3>
				<p>
					A paginated table of the school records. Each row shows the school name, associated
					keywords, and topics.
				</p>
			</hgroup>

			<table>
				<thead>
					<tr>
						<th>School</th>
						<th>Keywords</th>
						<th>Topics</th>
					</tr>
				</thead>
				<tbody>
					{#each $rows as school}
						<tr>
							<td>{school.name}</td>
							<td>{school.keywords.join(', ')}</td>
							<td>{school.topics.join(', ')}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="table-pagination">
				<RowCount {handler} />
				<Pagination {handler} />
			</div>
		{/if}
	</section>
	<section>
		<hgroup>
			<h3>Distribution of the extracted keywords</h3>
			<p>Explore a visualisation of the distribution of extracted keywords.</p>
		</hgroup>
		<FacetDistribution data={results.keywords} label="keyword" />
	</section>
	<section>
		<hgroup>
			<h3>Distribution of the extracted topics</h3>
			<p>Explore a visualisation of the distribution of extracted topics.</p>
		</hgroup>
		<FacetDistribution data={results.topics} label="topic" />
	</section>
{/await}

<style>
	.table-pagination {
		align-items: center;
		display: flex;
		justify-content: center;
	}
</style>
