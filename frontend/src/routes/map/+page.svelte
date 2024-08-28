<script lang="ts">
	import FacetMap from '$lib/components/FacetMap.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let { results } = data;
</script>

<section>
	<hgroup>
		<h1>Map of the extracted locations</h1>
		<p>Explore a visualisation of the geographical distribution of extracted locations.</p>
	</hgroup>
	<FacetMap places={results.places} />
</section>
