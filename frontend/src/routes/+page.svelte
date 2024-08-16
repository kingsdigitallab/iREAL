<script lang="ts">
	import { DataHandler, Pagination, RowCount } from '@vincjo/datatables';
	import FacetDistribution from '$lib/components/FacetDistribution.svelte';
	import _ from 'lodash';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import SummaryCard from '$lib/components/SummaryCard.svelte';
	import FacetMap from '$lib/components/FacetMap.svelte';
	import BaseLink from '$lib/components/BaseLink.svelte';

	export let data: PageData;

	let handler: DataHandler;
	let rows;

	onMount(async () => {
		const results = await data.results;
		const schools = await results.schools;

		handler = new DataHandler(schools, { rowsPerPage: 5 });
		rows = handler.getRows();
	});
</script>

<section>
	<hgroup>
		<h1>Dashboard</h1>
		<p>
			A dashboard for displaying and exploring school related data as exported by the AI/ML
			processes.
		</p>
	</hgroup>
</section>
<section>
	<h2>About the school records</h2>
	<p>The school records contain information about:</p>
	<ul>
		<li>school details and timeline</li>
		<li>relationshop between Deparment of Public Instruction and the Aboriginal Protection Board (APB)</li>
		<li>teacher's information</li>
		<li>conditions at the schools</li>
		<li>curriculum and resources</li>
		<li>community attitutes</li>
	</ul>
</section>

{#await data.results}
	<section aria-busy="true">Loading data...</section>
{:then results}
	<section>
		<hgroup>
			<h2>Summary</h2>
			<p>
				Overview of the data extracted from the school records. Shows counts for school records,
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
						<th>Places</th>
						<th>Topics</th>
					</tr>
				</thead>
				<tbody>
					{#each $rows as school}
						<tr>
							<td><BaseLink href="schools/{school.file}">{school.name}</BaseLink></td>
							<td>{school.keywords.join(', ')}</td>
							<td>{school.places.join(', ')}</td>
							<td>{school.topics.join(', ')}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="table-pagination">
				<section><RowCount {handler} /></section>
				<Pagination {handler} />
			</div>
		{/if}
	</section>
	<section>
		<hgroup>
			<h2>Distribution of the extracted keywords</h2>
			<p>Explore a visualisation of the distribution of extracted keywords.</p>
		</hgroup>
		<FacetDistribution data={results.keywords} label="keyword" />
	</section>
	<section>
		<hgroup>
			<h2>Distribution of the extracted topics</h2>
			<p>Explore a visualisation of the distribution of extracted topics.</p>
		</hgroup>
		<FacetDistribution data={results.topics} label="topic" />
	</section>
	<section>
		<hgroup>
			<h2>Map of the extracted places</h2>
			<p>Explore a visualisation of the geographical distribution of extracted places.</p>
		</hgroup>
		<FacetMap places={results.places} />
	</section>
{/await}

<style>
	tbody {
		font-size: 0.8rem;
	}

	.table-pagination {
		align-items: center;
		display: flex;
		color: var(--pico-color);
		justify-content: space-between;
	}
</style>
