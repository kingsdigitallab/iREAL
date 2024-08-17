<script lang="ts">
	import BaseLink from '$lib/components/BaseLink.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let { results } = data;
</script>

<section>
	<hgroup>
		<h1>School records</h1>
		<p>The table below shows each school and an overview of the extracted data for each school.</p>
	</hgroup>
	<p>
		The school records contain information about school details and timeline; relationship between
		Department of Public Instruction and the Aboriginal Protection Board (APB); teacher's
		information; conditions at the schools; curriculum and resources; community attitudes.
	</p>
</section>

{#await results.schools}
	<section aria-busy="true">Loading school records...</section>
{:then schools}
	<section>
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
				{#each schools as school}
					<tr>
						<td><BaseLink href="schools/{school.slug}">{school.name}</BaseLink></td>
						<td>{school.keywords.join(', ')}</td>
						<td>{school.places.join(', ')}</td>
						<td>{school.topics.join(', ')}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</section>
{/await}

<style>
	tbody {
		font-size: 0.8rem;
	}
</style>
