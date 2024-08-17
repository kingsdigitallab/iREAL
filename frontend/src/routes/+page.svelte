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
			spanning the late 19th to early 20th century. The information has been extracted from
			historical records using AI and machine learning techniques.
		</p>
	</hgroup>
</section>

{#await data.results}
	<section aria-busy="true">Loading data...</section>
{:then results}
	<section>
		<hgroup>
			<h2>Data overview</h2>
		</hgroup>
		<div class="grid">
			<SummaryCard title="School records" value={results.schoolsNames.length} link="schools" />
			<SummaryCard title="Keywords" value={results.keywords.length} link="keywords" />
			<SummaryCard title="Topics" value={results.topics.length} link="topics" />
		</div>
		<div class="grid">
			<SummaryCard title="People" value={results.people.length} />
			<SummaryCard title="Organisations" value={results.organisations.length} />
			<SummaryCard title="Places" value={results.places.length} link="map" />
		</div>
	</section>
{/await}

<style>
	.hero {
		padding-block: calc(2 * var(--pico-block-spacing-vertical));
	}
</style>
