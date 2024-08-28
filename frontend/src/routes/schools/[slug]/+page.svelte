<script lang="ts">
	import { entityFields } from '$lib/config';
	import type { Node } from '$lib/types';
	import _ from 'lodash';
	import type { PageData } from './$types';

	export let data: PageData;
	let { slug, md, nodes, school } = data;

	let schoolEntities: string[] = [];
	let schoolEntityFields = ['excerpt_keywords', ...entityFields];
	let schoolFields = [
		...schoolEntityFields,
		'questions_this_excerpt_can_answer',
		'section_summary',
		'topics'
	];

	let highlightFields: string[] = [];
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
			const entities = schoolEntityFields
				.map((field) => ({
					field,
					value: _.uniq(
						_(documents)
							.flatMap((doc) => (Array.isArray(doc[field]) ? doc[field] : doc[field]?.split(',')))
							.filter((value: string) => value)
							.map((value) => value.trim())
							.value()
					)
				}))
				.filter((entity) => entity.value.length > 0)
				.flatMap((entity) => entity.value.map((value) => ({ field: entity.field, value })));

			schoolEntities = _.uniq(entities.map((entity) => entity.field));

			entities.forEach(
				(entity) =>
					(node.innerHTML = node.innerHTML.replace(
						new RegExp(`\\b${entity.value}\\b`, 'gi'),
						`<mark class="${entity.field}"><span data-tooltip="${entity.field.replace('_', ' ')}">$&</span></mark>`
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
		<ul class="topics">
			<li>Topics:</li>
			{#each school.topics as topic}
				<li><em>{topic.name}</em></li>
			{/each}
		</ul>
	</hgroup>
	<div class="grid">
		{#await md}
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

{#if isRecordView}
	{#await md then content}
		<section>
			<form>
				<fieldset>
					<legend>Toggle content to highlight:</legend>
					{#each schoolEntityFields as field}
						<input
							type="checkbox"
							name="highlight"
							id="highlight"
							value={field}
							bind:group={highlightFields}
							disabled={!schoolEntities.includes(field)}
						/>
						<label class={field} for={field} aria-disabled={!schoolEntities.includes(field)}
							>{field[0].toLocaleUpperCase()}{field.slice(1).replace('_', ' ')}</label
						>
					{/each}
				</fieldset>
			</form>
			<article class={highlightFields.join(' ').trim()} use:highlightAction>
				<svelte:component this={content.default} />
			</article>
		</section>
	{/await}
{:else}
	<section>
		{#await nodes then documents}
			<h2>{documents[0].document_title}</h2>
			{#each documents as doc}
				<article>
					<dl>
						<dt>Text</dt>
						<dd>{getNodeText(doc)}</dd>
						{#each schoolFields as field}
							<dt>{getNodeFieldName(field)}</dt>
							<dd>{getNodeFieldValue(doc, field)}</dd>
						{/each}
					</dl>
				</article>
			{/each}
		{/await}
	</section>
{/if}

<style>
	.topics {
		padding-left: 0;
	}
	.topics > li {
		display: inline;
	}
	.topics > li + li + li::before {
		content: ', ';
	}

	:global(article mark) {
		background: none;
		color: inherit;
	}

	:global(.excerpt_keywords) {
		--highlight-color: var(--pico-mark-background-color);
		--text-color: var(--pico-mark-color);
	}

	:global(.diseases),
	:global(.events),
	:global(.locations),
	:global(.media),
	:global(.organizations),
	:global(.persons),
	:global(.times) {
		--highlight-color: var(--pico-primary-background);
		--text-color: var(--pico-primary-inverse);
	}

	label[class] {
		background-color: var(--highlight-color);
		color: var(--text-color);
		padding-inline: 0.3rem;
	}

	:global(article.diseases p:has(.diseases)),
	:global(article.events p:has(.events)),
	:global(article.excerpt_keywords p:has(.excerpt_keywords)),
	:global(article.locations p:has(.locations)),
	:global(article.media p:has(.media)),
	:global(article.organizations p:has(.organizations)),
	:global(article.persons p:has(.persons)),
	:global(article.times p:has(.times)) {
		border-left: 5px solid var(--highlight-color);
		padding-left: 0.5rem;
	}

	:global(article.diseases mark.diseases),
	:global(article.events mark.events),
	:global(article.excerpt_keywords mark.excerpt_keywords),
	:global(article.locations mark.locations),
	:global(article.media mark.media),
	:global(article.organizations mark.organizations),
	:global(article.persons mark.persons),
	:global(article.times mark.times) {
		background-color: var(--highlight-color);
		color: var(--text-color);
	}
</style>
