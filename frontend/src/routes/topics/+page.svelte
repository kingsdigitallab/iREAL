<script lang="ts">
	import FacetDistribution from '$lib/components/FacetDistribution.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
	let { results } = data;
</script>

<section>
	<hgroup>
		<h1>Distribution of the extracted topics</h1>
		<p>Explore a visualisation of the distribution of extracted keywords.</p>
	</hgroup>
	<FacetDistribution data={results.topics} schools={results.schools} label="topic" field="topics" />
</section>
