<script lang="ts">
	import BaseLink from './BaseLink.svelte';

	export let title: string;
	export let value: number;
	export let link: string | null = null;
</script>

<article>
	<header>
		{#if link}
			<BaseLink href={link}>{title}</BaseLink>
		{:else}
			{title}
		{/if}
	</header>
	<strong>{value}</strong>
</article>
