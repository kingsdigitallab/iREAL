<script lang="ts">
	import FacetDistribution from '$lib/components/FacetDistribution.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<section>
	<hgroup>
		<h1>Distribution of the extracted keywords</h1>
		<p>Explore a visualisation of the distribution of extracted keywords.</p>
	</hgroup>
	{#await data.schools}
		<section aria-busy="true">Loading data...</section>
	{:then schools}
		<FacetDistribution {schools} label="keyword" field="excerpt_keywords" />
	{/await}
</section>
