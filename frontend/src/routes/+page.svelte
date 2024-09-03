<script lang="ts">
	import SummaryCard from '$lib/components/SummaryCard.svelte';
	import * as config from '$lib/config';
	import _ from 'lodash';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<section class="hero">
	<hgroup>
		<h1>{config.description}</h1>
		<p>
			This dashboard presents data from 49 Aboriginal schools in New South Wales, Australia,
			spanning the 19th to early 20th century. The information has been extracted from historical
			records using AI and machine learning techniques.
		</p>
	</hgroup>
</section>

{#await data.overview}
	<section aria-busy="true">Loading data...</section>
{:then overview}
	<section>
		<hgroup>
			<h2>Data overview</h2>
			<p>{overview.years[0]}—{overview.years.slice(-1)}</p>
		</hgroup>
		<div class="grid">
			<SummaryCard title="School records" value={overview.schoolsNames.length} link="schools" />
			<SummaryCard title="Keywords" value={overview.keywords.length} link="keywords" />
			<SummaryCard title="Topics" value={overview.topics.length} link="topics" />
		</div>
		<div class="grid">
			<SummaryCard title="People" value={overview.people.length} />
			<SummaryCard
				title="Organisations"
				value={overview.organisations.length}
				link="organisations"
			/>
			<SummaryCard title="Locations" value={overview.places.length} link="map" />
		</div>
	</section>
{/await}

<style>
	.hero {
		padding-block: calc(2 * var(--pico-block-spacing-vertical));
	}
</style>
