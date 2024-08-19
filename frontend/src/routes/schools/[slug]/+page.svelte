<script lang="ts">
	import type { Node } from '$lib/types';
	import type { PageData } from './$types';

	export let data: PageData;

	let { slug, school, nodes } = data;
	let fields = [
		'excerpt_keywords',
		'diseases',
		'events',
		'excerpt_keywords',
		'locations',
		'media',
		'organizations',
		'persons',
		'questions_this_excerpt_can_answer',
		'section_summary',
		'times',
		'topics'
	];

	let isRecordView: boolean = true;

	function handleViewSwitch() {
		isRecordView = !isRecordView;
	}

	function getNodeText(node: Node) {
		return JSON.parse(node._node_content)?.text;
	}

	function getNodeFieldName(field: string) {
		return `${field[0].toUpperCase()}${field.slice(1).replace(/_/g, ' ')}`;
	}

	function getNodeFieldValue(node: Node, field: string) {
		const value = (node as any)[field];

		if (!value) return 'N/A';

		if (Array.isArray(value)) {
			return value.join(', ');
		}

		return value;
	}
</script>

<section>
	<hgroup>
		<h1>{slug}</h1>
	</hgroup>
	<div class="grid">
		{#await school}
			<button aria-busy="true" disabled>Loading school record...</button>
		{:then}
			<button on:click={handleViewSwitch} disabled={isRecordView}>School record</button>
		{/await}
		{#await nodes}
			<button aria-busy="true" disabled>Loading processed data...</button>
		{:then}
			<button on:click={handleViewSwitch} disabled={!isRecordView}>Processed data</button>
		{/await}
	</div>
</section>

<section>
	{#if isRecordView}
		{#await school then content}
			<article>
				<svelte:component this={content.default} />
			</article>
		{/await}
	{:else}
		{#await nodes then documents}
			<h2>{documents[0].document_title}</h2>
			{#each documents as doc}
				<article>
					<dl>
						<dt>Text</dt>
						<dd>{getNodeText(doc)}</dd>
						{#each fields as field}
							<dt>{getNodeFieldName(field)}</dt>
							<dd>{getNodeFieldValue(doc, field)}</dd>
						{/each}
					</dl>
				</article>
			{/each}
		{/await}
	{/if}
</section>
