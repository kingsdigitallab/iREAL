<script lang="ts">
	import BaseLink from '$lib/components/BaseLink.svelte';
	import { entityFields } from '$lib/config';
	import type { PageData } from './$types';

	export let data: PageData;
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

{#await data.schools}
	<section aria-busy="true">Loading school records...</section>
{:then schools}
	<section>
		<table>
			<thead>
				<tr>
					<th>School</th>
					<th>Years</th>
					<th>Keywords</th>
					<th>Topics</th>
					{#each entityFields as field}
						<th>{field[0].toUpperCase()}{field.slice(1)}</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each schools as school}
					<tr>
						<td><BaseLink href="schools/{school.slug}">{school.name}</BaseLink></td>
						<td>{school.excerpt_keywords.length}</td>
						<td>{school.topics.length}</td>
						{#each entityFields as field}
							<td>{school[field].length}</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</section>
{/await}
