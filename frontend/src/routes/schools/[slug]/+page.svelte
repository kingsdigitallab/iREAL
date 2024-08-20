<script lang="ts">
	import type { Node } from '$lib/types';
	import _ from 'lodash';
	import type { PageData } from './$types';

	export let data: PageData;
	let { slug, school, nodes } = data;

	let entityFields = [
		'diseases',
		'events',
		'locations',
		'media',
		'organizations',
		'persons',
		'times'
	];
	let allFields = [
		...entityFields,
		'questions_this_excerpt_can_answer',
		'section_summary',
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

	function highlightAction(node: HTMLElement) {
		async function handleHighlightAction() {
			const documents = await nodes;
			const entities = entityFields
				.map((field) => ({
					field,
					value: _.uniq(
						_(documents)
							.flatMap(field)
							.filter((value) => value)
							.value()
					)
				}))
				.filter((entity) => entity.value.length > 0)
				.flatMap((entity) => entity.value.map((value) => ({ field: entity.field, value })));

			entities.forEach(
				(entity) =>
					(node.innerHTML = node.innerHTML.replace(
						new RegExp(`\\b${entity.value}\\b`, 'gi'),
						`<mark class="${entity.field}" data-tooltip="${entity.field}: ${entity.value}">$&</mark>`
					))
			);
		}

		handleHighlightAction();

		return {
			destroy() {}
		};
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
			<article use:highlightAction>
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
						{#each allFields as field}
							<dt>{getNodeFieldName(field)}</dt>
							<dd>{getNodeFieldValue(doc, field)}</dd>
						{/each}
					</dl>
				</article>
			{/each}
		{/await}
	{/if}
</section>

<style>
	:global(mark.diseases) {
		background: var(--mark-diseases);
		color: #000;
	}
	:global(mark.events) {
		background: var(--mark-events);
	}
	:global(mark.locations) {
		background: var(--mark-locations);
		color: #000;
	}
	:global(mark.media) {
		background: var(--mark-media);
	}
	:global(mark.organizations) {
		background: var(--mark-organizations);
		color: var(--pico-primary-inverse);
	}
	:global(mark.persons) {
		background: var(--mark-persons);
		color: var(--pico-primary-inverse);
	}
	:global(mark.times) {
		background: var(--mark-times);
	}
</style>
